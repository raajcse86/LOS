from models.document import Document
from utils.db import get_db
from datetime import datetime
from bson.objectid import ObjectId
import os
import random
import base64
import uuid
import gridfs
import zipfile
import io
from flask import current_app
import mimetypes
import traceback

class DocumentService:
    def __init__(self):
        self.db = get_db()
        self.documents_collection = self.db['documents']
        # Initialize GridFS
        self.fs = gridfs.GridFS(self.db)
        
        # Keep the uploads_dir for backward compatibility
        self.uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
        if not os.path.exists(self.uploads_dir):
            os.makedirs(self.uploads_dir)
            
    # Helper method to convert MongoDB documents to JSON-serializable format
    def _convert_to_serializable(self, document):
        """Convert a MongoDB document to JSON serializable format."""
        if document is None:
            return None
            
        # Make a copy to avoid modifying the original
        result = document.copy()
        
        # Convert ObjectId fields to strings
        if '_id' in result:
            result['_id'] = str(result['_id'])
        
        if 'gridfs_id' in result and result['gridfs_id'] is not None:
            result['gridfs_id'] = str(result['gridfs_id'])
            
        if 'loanId' in result and isinstance(result['loanId'], ObjectId):
            result['loanId'] = str(result['loanId'])
            
        if 'uploadedBy' in result and isinstance(result['uploadedBy'], ObjectId):
            result['uploadedBy'] = str(result['uploadedBy'])
            
        return result
    
    def get_all_documents(self):
        """Get all documents from database."""
        documents = list(self.documents_collection.find())
        # Convert all documents to JSON serializable format
        return [self._convert_to_serializable(doc) for doc in documents]
    
    def get_document_by_id(self, document_id):
        """Get a document by its ID."""
        try:
            document = self.documents_collection.find_one({'_id': ObjectId(document_id)})
            return self._convert_to_serializable(document)
        except Exception as e:
            print(f"Error fetching document: {e}")
            return None
    
    def get_documents_by_loan_id(self, loan_id):
        """Get all documents for a specific loan."""
        try:
            # if isinstance(loan_id, str) and ObjectId.is_valid(loan_id):
            #     loan_id = ObjectId(loan_id)
                
            documents = list(self.documents_collection.find({'loanId': loan_id}))
            # Convert all documents to JSON serializable format
            return [self._convert_to_serializable(doc) for doc in documents]
        except Exception as e:
            print(f"Error fetching documents by loan ID: {e}")
            return []
    
    def upload_document(self, loan_id, document_type, file, user_id=None):
        """Upload a document for a loan using GridFS."""
        try:
            # Generate a unique filename
            original_filename = file.filename
            file_extension = original_filename.split('.')[-1] if '.' in original_filename else ''
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            
            # Get file data
            file_data = file.read()
            file_size = len(file_data)
            
            # Create a zip file in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                zip_file.writestr(original_filename, file_data)
            
            # Get the zip data
            zip_buffer.seek(0)
            zip_data = zip_buffer.read()
            zip_size = len(zip_data)
            
            # Generate a unique filename for the zip
            zip_filename = f"{uuid.uuid4().hex}.zip"
            
            # Store the zip file in GridFS
            file_id = self.fs.put(
                zip_data,
                filename=zip_filename,
                content_type='application/zip',
                original_filename=original_filename,
                loan_id=loan_id,
                document_type=document_type
            )
            
            # Create document record
            now = datetime.utcnow().isoformat()
            document_data = {
                'loanId': loan_id,
                'documentType': document_type,
                'filename': zip_filename,
                'originalFilename': original_filename,
                'fileSize': zip_size,
                'originalFileSize': file_size,
                'mimeType': file.content_type,
                'gridfs_id': file_id,
                'uploadDate': now,
                'uploadedBy': user_id,
                'contentExtracted': False,
                'status': 'Pending',  # Add status field
                'complianceScore': None  # Add score field
            }
            
            # Insert into database
            result = self.documents_collection.insert_one(document_data)
            
            # Return the created document with all ObjectIds converted to strings
            created_document = self.get_document_by_id(result.inserted_id)
            return self._convert_to_serializable(created_document)
        except Exception as e:
            print(f"Error uploading document: {e}")
            return None

    def download_document(self, document_id):
        """
        Get file data for downloading a document from GridFS.
        
        Args:
            document_id (str): The ID of the document to download
            
        Returns:
            dict: Dictionary containing file_data, filename, and mime_type
                  or None if document not found or error occurs
        """
        try:
            # Convert string ID to ObjectId if needed
            doc_id = ObjectId(document_id) if isinstance(document_id, str) else document_id
            
            # Get document metadata from collection
            document = self.documents_collection.find_one({'_id': doc_id})
            if not document:
                current_app.logger.warning(f"Document not found in database: {document_id}")
                return None

            try:
                # If document was stored in GridFS
                if 'gridfs_id' in document:
                    # Verify GridFS file exists
                    if not self.fs.exists(document['gridfs_id']):
                        current_app.logger.error(f"GridFS file missing for document: {document_id}")
                        return None
                    
                    # Get the file from GridFS
                    grid_out = self.fs.get(document['gridfs_id'])
                    file_data = grid_out.read()

                    # If it's a zip file, extract the original file
                    if (document.get('mimeType') == 'application/zip' or 
                        document['filename'].endswith('.zip')):
                        try:
                            # Extract the original file from the zip
                            with zipfile.ZipFile(io.BytesIO(file_data)) as zip_file:
                                # Validate zip file contents
                                if zip_file.testzip() is not None:
                                    current_app.logger.error(f"Corrupted zip file for document: {document_id}")
                                    return None
                                    
                                # Get the first file in the zip (should be the only one)
                                file_list = zip_file.namelist()
                                if not file_list:
                                    current_app.logger.error(f"Empty zip file for document: {document_id}")
                                    return None
                                    
                                first_file = file_list[0]
                                file_data = zip_file.read(first_file)
                        except zipfile.BadZipFile as e:
                            current_app.logger.error(f"Invalid zip file for document {document_id}: {str(e)}")
                            return None
                else:
                    # Legacy support for files stored on disk
                    file_path = os.path.join(self.uploads_dir, document['filename'])
                    if not os.path.exists(file_path):
                        current_app.logger.error(f"File not found on disk: {file_path}")
                        return None

                    # Validate file path (prevent directory traversal)
                    if not os.path.normpath(file_path).startswith(os.path.normpath(self.uploads_dir)):
                        current_app.logger.error(f"Invalid file path detected: {file_path}")
                        return None

                    with open(file_path, 'rb') as file:
                        file_data = file.read()

                # Verify we have valid file data
                if not file_data:
                    current_app.logger.error(f"Empty file data for document: {document_id}")
                    return None

                # Get correct mime type
                mime_type = document.get('mimeType')
                if not mime_type:
                    # Try to guess mime type from filename
                    mime_type, _ = mimetypes.guess_type(document['originalFilename'])
                    if not mime_type:
                        mime_type = 'application/octet-stream'

                # Log successful retrieval
                current_app.logger.info(
                    f"Successfully retrieved document: {document_id}, "
                    f"size: {len(file_data)} bytes, "
                    f"type: {mime_type}"
                )

                return {
                    'file_data': file_data,
                    'filename': document['originalFilename'],
                    'mime_type': mime_type,
                    'file_size': len(file_data)
                }

            except gridfs.errors.CorruptGridFile as e:
                current_app.logger.error(f"Corrupt GridFS file for document {document_id}: {str(e)}")
                return None
            
        except Exception as e:
            current_app.logger.error(
                f"Error downloading document {document_id}: {str(e)}\n"
                f"Traceback: {traceback.format_exc()}"
            )
            return None

    def extract_document_content(self, document_id):
        """Extract content from a document using the actual file content."""
        try:
            document = self.documents_collection.find_one({'_id': ObjectId(document_id)})
            if not document:
                return None

            # Convert document to serializable format for consistent handling
            document = self._convert_to_serializable(document)

            # Get the actual document content
            doc_data = self.download_document(document_id)
            if not doc_data:
                return None

            file_data = doc_data['file_data']
            mime_type = doc_data['mime_type']
            filename = doc_data['filename']

            # Extract text based on the file type
            extracted_content = ""

            # For plain text files
            if mime_type.startswith('text/'):
                try:
                    extracted_content = file_data.decode('utf-8')
                except UnicodeDecodeError:
                    # If UTF-8 fails, try different encodings
                    try:
                        extracted_content = file_data.decode('latin-1')
                    except:
                        extracted_content = "Unable to decode text content."

            # For PDF files
            elif mime_type == 'application/pdf' or filename.lower().endswith('.pdf'):
                # Enhanced PDF text extraction approach
                try:
                    # Convert binary data to string (ignoring errors)
                    text_content = file_data.decode('latin-1', errors='ignore')

                    import re

                    # Step 1: Remove PDF structure markers that aren't actual content
                    common_pdf_markers = [
                        r'obj', r'endobj', r'stream', r'endstream', r'xref', r'trailer', r'startxref',
                        r'BT', r'ET', r'Tj', r'TJ', r'Td', r'TD', r'pdf', r'PDF', r'BDC', r'EMC',
                        r'endobj', r'BBox', r'Filter', r'DecodeParms', r'Length', r'ProcSet', r'Resources'
                    ]

                    # Create a pattern to match common PDF internal syntax
                    pdf_syntax_pattern = '|'.join([r'\b' + marker + r'\b' for marker in common_pdf_markers])
                    cleaned_content = re.sub(pdf_syntax_pattern, ' ', text_content)

                    # Step 2: Extract only text ranges with printable ASCII characters and spaces
                    # with at least 5 characters in a row to avoid noise
                    text_chunks = re.findall(r'[\x20-\x7E\s]{5,}', cleaned_content)

                    # Step 3: Filter chunks to remove those that are mostly numbers or short words
                    # as they're likely PDF coordinates or other non-content markers
                    filtered_chunks = []
                    for chunk in text_chunks:
                        # Skip chunks that are primarily numbers, PDF operators, or very short tokens
                        if not re.match(r'^[\d\s\/\(\)\[\]\{\}]+$', chunk):
                            # Find all words with 3+ chars (likely actual content words)
                            words = re.findall(r'\b[a-zA-Z]{3,}\b', chunk)
                            if len(words) >= 2:  # At least two real words
                                filtered_chunks.append(chunk.strip())

                    # Step 4: Join the filtered chunks with newlines for readability
                    if filtered_chunks:
                        # Remove duplicate chunks (PDF often repeats content in different sections)
                        unique_chunks = []
                        for chunk in filtered_chunks:
                            if chunk not in unique_chunks:
                                unique_chunks.append(chunk)

                        # Join unique chunks with newlines
                        extracted_content = '\n\n'.join(unique_chunks)

                        # Final cleaning - remove multiple spaces/newlines and common PDF artifacts
                        extracted_content = re.sub(r'\s{2,}', ' ', extracted_content)
                        extracted_content = re.sub(r'\n{3,}', '\n\n', extracted_content)
                    else:
                        extracted_content = "No readable text content found in the PDF document.\n" + \
                                            "The PDF may contain only images or scanned content."
                except Exception as pdf_err:
                    print(f"Error in enhanced PDF extraction: {pdf_err}")
                    extracted_content = f"Could not extract text from PDF: {pdf_err}\n" + \
                                        "The document appears to be a PDF but text extraction failed."

            # For other file types (images, etc.)
            else:
                extracted_content = f"""
                Document Details:
                Filename: {filename}
                MIME Type: {mime_type}
                Size: {len(file_data)} bytes
                Document Type: {document['documentType']}
                Upload Date: {document['uploadDate']}

                [This document requires specialized processing to extract content.
                For images and complex PDFs, OCR software would be needed.]
                """

            # Update the document record with extracted content
            now = datetime.utcnow().isoformat()
            self.documents_collection.update_one(
                {'_id': ObjectId(document_id)},
                {
                    '$set': {
                        'contentExtracted': True,
                        'extractedContent': extracted_content
                    }
                }
            )

            return {
                'document_id': document['_id'],  # Already converted to string
                'extractedContent': extracted_content,
                'status': 'success'
            }
        except Exception as e:
            print(f"Error extracting document content: {e}")
            return None
    
    def update_document(self, document_id, update_data):
        """Update a document with the provided data."""
        try:
            document = self.documents_collection.find_one({'_id': ObjectId(document_id)})
            if not document:
                return False
            
            # Create an update object with only the fields that are provided
            update_fields = {}
            
            # Status update
            if 'status' in update_data:
                update_fields['status'] = update_data['status']
            
            # Compliance score update if provided
            if 'complianceScore' in update_data:
                update_fields['complianceScore'] = update_data['complianceScore']
            
            # Update the document record with the new data
            self.documents_collection.update_one(
                {'_id': ObjectId(document_id)},
                {
                    '$set': update_fields
                }
            )
            
            return True
        except Exception as e:
            print(f"Error updating document: {e}")
            return False


            
    def check_compliance_score(self, document_id):
        """Check compliance score for a document (simulated for this application)."""
        try:
            document = self.documents_collection.find_one({'_id': ObjectId(document_id)})
            if not document:
                return None
                
            # Convert document to serializable format for consistent handling
            document = self._convert_to_serializable(document)
            
            # For this demo, we'll generate a random compliance score
            # In a real application, this would use document verification services
            
            # Generate a score between a valid range to sometimes pass and sometimes fail
            compliance_score = round(random.uniform(85, 100), 1)
            
            # Determine document status based on score
            status = 'Approved' if compliance_score >= 90 else 'Rejected'
            
            # Update the document record with compliance score and status
            self.documents_collection.update_one(
                {'_id': ObjectId(document_id)},
                {
                    '$set': {
                        'complianceScore': compliance_score,
                        'status': status
                    }
                }
            )
            
            return {
                'document_id': document['_id'],  # Already converted to string
                'complianceScore': compliance_score,
                'score': compliance_score,  # Duplicated for frontend compatibility
                'status': status,
                'passed': compliance_score >= 90
            }
        except Exception as e:
            print(f"Error checking compliance score: {e}")
            return None
    
    def delete_document(self, document_id):
        """Delete a document from GridFS and database."""
        try:
            document = self.documents_collection.find_one({'_id': ObjectId(document_id)})
            if not document:
                return False
            
            # If the document was stored in GridFS
            if 'gridfs_id' in document:
                # Delete the file from GridFS
                self.fs.delete(document['gridfs_id'])
            else:
                # Legacy support for files stored on disk
                file_path = os.path.join(self.uploads_dir, document['filename'])
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Delete from database
            result = self.documents_collection.delete_one({'_id': ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
