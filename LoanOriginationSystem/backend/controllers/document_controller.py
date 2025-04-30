from flask import jsonify, request, send_file
from services.document_service import DocumentService
from werkzeug.utils import secure_filename
import os
import io

document_service = DocumentService()

def get_all_documents():
    """Get all documents."""
    documents = document_service.get_all_documents()
    return jsonify(documents)

def get_document(document_id):
    """Get a document by ID."""
    document = document_service.get_document_by_id(document_id)
    if not document:
        return jsonify({"error": "Document not found"}), 404
    return jsonify(document)

def update_document(document_id):
    """Update a document's status (approve/reject)."""
    if not request.json:
        return jsonify({"error": "No update data provided"}), 400
    
    # Get update data
    update_data = request.json
    
    # Validate status if provided
    status = update_data.get('status')
    if status and status not in ['Approved', 'Rejected', 'Pending Review']:
        return jsonify({"error": "Invalid status value"}), 400
    
    # Call service to update document
    success = document_service.update_document(document_id, update_data)
    if not success:
        return jsonify({"error": "Failed to update document"}), 500
    
    # Get updated document
    updated_document = document_service.get_document_by_id(document_id)
    return jsonify(updated_document)

def get_documents_by_loan(loan_id):
    """Get all documents for a specific loan."""
    documents = document_service.get_documents_by_loan_id(loan_id)
    return jsonify(documents)

def upload_document(loan_id):
    """Upload a document for a loan."""
    # Check if the request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Validate file type (allow .docx and .pdf)
    allowed_extensions = {'.docx', '.pdf'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        return jsonify({"error": f"File type not allowed. Only {', '.join(allowed_extensions)} are supported"}), 400
    
    # Get document type from form data
    document_type = request.form.get('documentType')
    
    # Validate required fields
    if not document_type:
        return jsonify({"error": "documentType is required"}), 400
    
    # Upload document
    document = document_service.upload_document(loan_id, document_type, file)
    if not document:
        return jsonify({"error": "Failed to upload document"}), 500
    
    # Make sure document has string ID (already handled in service)
    # This is redundant but ensures we don't have ObjectId serialization issues
    if document and '_id' in document and not isinstance(document['_id'], str):
        document['_id'] = str(document['_id'])
    
    return jsonify(document), 201

def download_document(document_id):
    """Download a document."""
    result = document_service.download_document(document_id)
    if not result:
        return jsonify({"error": "Document not found"}), 404
    
    return send_file(
        io.BytesIO(result['file_data']),
        download_name=result['filename'],
        mimetype=result['mime_type']
    )

def extract_document_content(document_id):
    """Extract content from a document."""
    result = document_service.extract_document_content(document_id)
    if not result:
        return jsonify({"error": "Failed to extract document content"}), 500
    
    return jsonify(result)

def check_compliance_score(document_id):
    """Check compliance score for a document."""
    result = document_service.check_compliance_score(document_id)
    if not result:
        return jsonify({"error": "Failed to check compliance score"}), 500
    
    return jsonify(result)

def delete_document(document_id):
    """Delete a document."""
    success = document_service.delete_document(document_id)
    if not success:
        return jsonify({"error": "Failed to delete document"}), 500
    
    return jsonify({"message": "Document deleted successfully"})
