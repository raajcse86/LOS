from flask import Blueprint
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.loan_controller import (
    get_all_loans, get_loan, create_loan, update_employment_info,
    update_property_info, update_loan_pricing, update_closing_fees,
    update_consent, update_milestone, create_underwriter_report,
    create_closing_document_report
)

loan_bp = Blueprint('loan_bp', __name__)

# Get all loans
loan_bp.route('/', methods=['GET'])(get_all_loans)

# Get a loan by ID
loan_bp.route('/<loan_id>/', methods=['GET'])(get_loan)

# Create a new loan
loan_bp.route('/', methods=['POST'])(create_loan)

# Update employment information
loan_bp.route('/<loan_id>/employment/', methods=['PUT'])(update_employment_info)

# Update property information
loan_bp.route('/<loan_id>/property/', methods=['PUT'])(update_property_info)

# Update loan pricing
loan_bp.route('/<loan_id>/pricing/', methods=['PUT'])(update_loan_pricing)

# Update closing fees
loan_bp.route('/<loan_id>/closing-fees/', methods=['PUT'])(update_closing_fees)

# Update consent information
loan_bp.route('/<loan_id>/consent/', methods=['PUT'])(update_consent)

# Update milestone
loan_bp.route('/<loan_id>/milestone/', methods=['PUT'])(update_milestone)

# Create underwriter report
loan_bp.route('/<loan_id>/underwriter-report/', methods=['POST'])(create_underwriter_report)

# Create closing document report
loan_bp.route('/<loan_id>/closing-report/', methods=['POST'])(create_closing_document_report)
