from flask import jsonify, request
from services.loan_service import LoanService
from bson import ObjectId
import json

loan_service = LoanService()

def get_all_loans():
    """Get all loans."""
    loans = loan_service.get_all_loans()
    return jsonify(loans)

def get_loan(loan_id):
    """Get a loan by ID."""
    loan = loan_service.get_loan_by_id(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    return jsonify(loan)

def create_loan():
    """Create a new loan."""
    data = request.json
    
    # Validate required fields
    if 'borrowerInfo' not in data:
        return jsonify({"error": "borrowerInfo is required"}), 400
    
    # Set initial milestone if not provided
    if 'milestone' not in data:
        data['milestone'] = 'PreApplication'
    
    # Create loan
    loan = loan_service.create_loan(data)
    if not loan:
        return jsonify({"error": "Failed to create loan"}), 500
    
    return jsonify(loan), 201

def update_employment_info(loan_id):
    """Update employment information for a loan."""
    data = request.json
    
    # Validate required fields
    if 'employmentInfo' not in data:
        return jsonify({"error": "employmentInfo is required"}), 400
    
    # Update loan
    loan = loan_service.update_employment_info(loan_id, data['employmentInfo'])
    if not loan:
        return jsonify({"error": "Failed to update employment information"}), 500
    
    return jsonify(loan)

def update_property_info(loan_id):
    """Update property information for a loan."""
    data = request.json
    
    # Validate required fields
    if 'propertyInfo' not in data:
        return jsonify({"error": "propertyInfo is required"}), 400
    
    # Update loan
    loan = loan_service.update_property_info(loan_id, data['propertyInfo'])
    if not loan:
        return jsonify({"error": "Failed to update property information"}), 500
    
    return jsonify(loan)

def update_loan_pricing(loan_id):
    """Update loan pricing information."""
    data = request.json
    
    # Validate required fields
    if 'loanPricing' not in data:
        return jsonify({"error": "loanPricing is required"}), 400
    
    # Update loan
    loan = loan_service.update_loan_pricing(loan_id, data['loanPricing'])
    if not loan:
        return jsonify({"error": "Failed to update loan pricing"}), 500
    
    return jsonify(loan)

def update_closing_fees(loan_id):
    """Update closing fees information."""
    data = request.json
    
    # Validate required fields
    if 'closingFees' not in data:
        return jsonify({"error": "closingFees is required"}), 400
    
    # Update loan
    loan = loan_service.update_closing_fees(loan_id, data['closingFees'])
    if not loan:
        return jsonify({"error": "Failed to update closing fees"}), 500
    
    return jsonify(loan)

def update_consent(loan_id):
    """Update consent information."""
    data = request.json
    
    # Validate required fields
    if 'consentInfo' not in data:
        return jsonify({"error": "consentInfo is required"}), 400
    
    # Update loan
    loan = loan_service.update_consent_info(loan_id, data['consentInfo'])
    if not loan:
        return jsonify({"error": "Failed to update consent information"}), 500
    
    return jsonify(loan)

def update_milestone(loan_id):
    """Update the milestone status of a loan."""
    data = request.json
    
    # Validate required fields
    if 'milestone' not in data:
        return jsonify({"error": "milestone is required"}), 400
    
    # Update loan
    loan = loan_service.update_milestone(loan_id, data['milestone'])
    if not loan:
        return jsonify({"error": "Failed to update milestone"}), 500
    
    return jsonify(loan)

def create_underwriter_report(loan_id):
    """Create an underwriter report for a loan."""
    data = request.json
    
    # Validate required fields
    if 'report' not in data:
        return jsonify({"error": "report is required"}), 400
    
    # Create report
    loan = loan_service.create_underwriter_report(loan_id, data['report'])
    if not loan:
        return jsonify({"error": "Failed to create underwriter report"}), 500
    
    return jsonify(loan)

def create_closing_document_report(loan_id):
    """Create a closing document report for a loan."""
    data = request.json
    
    # Validate required fields
    if 'report' not in data:
        return jsonify({"error": "report is required"}), 400
    
    # Create report
    loan = loan_service.create_closing_document_report(loan_id, data['report'])
    if not loan:
        return jsonify({"error": "Failed to create closing document report"}), 500
    
    return jsonify(loan)
