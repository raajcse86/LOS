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
            if isinstance(loan_id, str) and ObjectId.is_valid(loan_id):
                loan_id = ObjectId(loan_id)
                
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
        """Get file data for downloading a document from GridFS."""
        try:
            document = self.documents_collection.find_one({'_id': ObjectId(document_id)})
            if not document:
                return None
            
            # If document was stored in GridFS
            if 'gridfs_id' in document:
                # Get the file from GridFS
                grid_out = self.fs.get(document['gridfs_id'])
                file_data = grid_out.read()
                
                # If it's a zip file, extract the original file
                if document.get('mimeType') == 'application/zip' or document['filename'].endswith('.zip'):
                    # Extract the original file from the zip
                    with zipfile.ZipFile(io.BytesIO(file_data)) as zip_file:
                        # Get the first file in the zip (should be the only one)
                        first_file = zip_file.namelist()[0]
                        file_data = zip_file.read(first_file)
            else:
                # Legacy support for files stored on disk
                file_path = os.path.join(self.uploads_dir, document['filename'])
                if not os.path.exists(file_path):
                    return None
                
                with open(file_path, 'rb') as file:
                    file_data = file.read()
            
            return {
                'file_data': file_data,
                'filename': document['originalFilename'],
                'mime_type': document['mimeType']
            }
        except Exception as e:
            print(f"Error downloading document: {e}")
            return None
    
    def extract_document_content(self, document_id):
        """Extract content from a document (simulated for this application)."""
        try:
            document = self.documents_collection.find_one({'_id': ObjectId(document_id)})
            if not document:
                return None
            
            # Convert document to serializable format for consistent handling
            document = self._convert_to_serializable(document)
            
            # For this demo, we'll simulate content extraction
            # In a real application, this would use OCR or document parsing services
            
            extracted_content = f"""
            This is simulated extracted content from document: {document['originalFilename']}
            Document Type: {document['documentType']}
            Upload Date: {document['uploadDate']}
            
            The document contains information relevant to the loan application process.
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
