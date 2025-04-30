from flask import Blueprint
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.document_controller import (
    get_all_documents, get_document, get_documents_by_loan,
    upload_document, download_document, extract_document_content,
    check_compliance_score, delete_document, update_document
)

document_bp = Blueprint('document_bp', __name__)

# Get all documents
document_bp.route('/', methods=['GET'])(get_all_documents)

# Get a document by ID
document_bp.route('/<document_id>/', methods=['GET'])(get_document)

# Update a document by ID (for approving/rejecting)
document_bp.route('/<document_id>/', methods=['PUT'])(update_document)

# Get documents by loan ID
document_bp.route('/loan/<loan_id>/', methods=['GET'])(get_documents_by_loan)

# Upload document
document_bp.route('/upload/<loan_id>/', methods=['POST'])(upload_document)

# Download document
document_bp.route('/<document_id>/download/', methods=['GET'])(download_document)

# Extract document content
document_bp.route('/<document_id>/extract/', methods=['GET'])(extract_document_content)

# Check compliance score
document_bp.route('/<document_id>/compliance/', methods=['GET'])(check_compliance_score)

# Delete document
document_bp.route('/<document_id>/', methods=['DELETE'])(delete_document)
