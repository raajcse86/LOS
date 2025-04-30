from models.loan import Loan
from utils.db import get_db
from datetime import datetime
from bson.objectid import ObjectId

class LoanService:
    def __init__(self):
        self.db = get_db()
        self.loans_collection = self.db['loans']
    
    def get_all_loans(self):
        """Get all loans from database."""
        loans = list(self.loans_collection.find())
        # Convert ObjectId to string to make it JSON serializable
        for loan in loans:
            loan['_id'] = str(loan['_id'])
        return loans
    
    def get_loan_by_id(self, loan_id):
        """Get a loan by its ID."""
        try:
            loan = self.loans_collection.find_one({'_id': ObjectId(loan_id)})
            if loan:
                loan['_id'] = str(loan['_id'])
            return loan
        except Exception as e:
            print(f"Error fetching loan: {e}")
            return None
    
    def create_loan(self, loan_data):
        """Create a new loan application."""
        try:
            # Add timestamps
            now = datetime.utcnow().isoformat()
            loan_data['createdAt'] = now
            loan_data['updatedAt'] = now
            
            # Insert into database
            result = self.loans_collection.insert_one(loan_data)
            
            # Return the created loan with string ID
            created_loan = self.get_loan_by_id(result.inserted_id)
            return created_loan
        except Exception as e:
            print(f"Error creating loan: {e}")
            return None
    
    def update_employment_info(self, loan_id, employment_info):
        """Update employment information for a loan."""
        try:
            # Update timestamp
            now = datetime.utcnow().isoformat()
            
            # Update in database
            result = self.loans_collection.update_one(
                {'_id': ObjectId(loan_id)},
                {
                    '$set': {
                        'employmentInfo': employment_info,
                        'updatedAt': now
                    }
                }
            )
            
            if result.modified_count > 0:
                return self.get_loan_by_id(loan_id)
            return None
        except Exception as e:
            print(f"Error updating employment info: {e}")
            return None
    
    def update_property_info(self, loan_id, property_info):
        """Update property information for a loan."""
        try:
            # Update timestamp
            now = datetime.utcnow().isoformat()
            
            # Update in database
            result = self.loans_collection.update_one(
                {'_id': ObjectId(loan_id)},
                {
                    '$set': {
                        'propertyInfo': property_info,
                        'updatedAt': now
                    }
                }
            )
            
            if result.modified_count > 0:
                return self.get_loan_by_id(loan_id)
            return None
        except Exception as e:
            print(f"Error updating property info: {e}")
            return None
    
    def update_loan_pricing(self, loan_id, loan_pricing):
        """Update loan pricing information."""
        try:
            # Update timestamp
            now = datetime.utcnow().isoformat()
            
            # Update in database
            result = self.loans_collection.update_one(
                {'_id': ObjectId(loan_id)},
                {
                    '$set': {
                        'loanPricing': loan_pricing,
                        'updatedAt': now
                    }
                }
            )
            
            if result.modified_count > 0:
                return self.get_loan_by_id(loan_id)
            return None
        except Exception as e:
            print(f"Error updating loan pricing: {e}")
            return None
    
    def update_closing_fees(self, loan_id, closing_fees):
        """Update closing fees information."""
        try:
            # Update timestamp
            now = datetime.utcnow().isoformat()
            
            # Update in database
            result = self.loans_collection.update_one(
                {'_id': ObjectId(loan_id)},
                {
                    '$set': {
                        'closingFees': closing_fees,
                        'updatedAt': now
                    }
                }
            )
            
            if result.modified_count > 0:
                return self.get_loan_by_id(loan_id)
            return None
        except Exception as e:
            print(f"Error updating closing fees: {e}")
            return None
    
    def update_consent_info(self, loan_id, consent_info):
        """Update consent information."""
        try:
            # Update timestamp
            now = datetime.utcnow().isoformat()
            
            # Update in database
            result = self.loans_collection.update_one(
                {'_id': ObjectId(loan_id)},
                {
                    '$set': {
                        'consentInfo': consent_info,
                        'updatedAt': now
                    }
                }
            )
            
            if result.modified_count > 0:
                return self.get_loan_by_id(loan_id)
            return None
        except Exception as e:
            print(f"Error updating consent info: {e}")
            return None
    
    def update_milestone(self, loan_id, milestone):
        """Update the milestone status of a loan."""
        try:
            # Validate milestone
            valid_milestones = [
                'PreApplication', 'Application', 'Processing', 
                'Underwriting', 'Approval', 'Closing', 'Funded'
            ]
            
            if milestone not in valid_milestones:
                return None
            
            # Update timestamp
            now = datetime.utcnow().isoformat()
            
            # Update in database
            result = self.loans_collection.update_one(
                {'_id': ObjectId(loan_id)},
                {
                    '$set': {
                        'milestone': milestone,
                        'updatedAt': now
                    }
                }
            )
            
            if result.modified_count > 0:
                return self.get_loan_by_id(loan_id)
            return None
        except Exception as e:
            print(f"Error updating milestone: {e}")
            return None
    
    def create_underwriter_report(self, loan_id, report_data):
        """Create an underwriter report for a loan."""
        try:
            # Update timestamp
            now = datetime.utcnow().isoformat()
            
            # Update in database
            result = self.loans_collection.update_one(
                {'_id': ObjectId(loan_id)},
                {
                    '$set': {
                        'underwriterReport': report_data,
                        'updatedAt': now
                    }
                }
            )
            
            if result.modified_count > 0:
                return self.get_loan_by_id(loan_id)
            return None
        except Exception as e:
            print(f"Error creating underwriter report: {e}")
            return None
    
    def create_closing_document_report(self, loan_id, report_data):
        """Create a closing document report for a loan."""
        try:
            # Update timestamp
            now = datetime.utcnow().isoformat()
            
            # Update in database
            result = self.loans_collection.update_one(
                {'_id': ObjectId(loan_id)},
                {
                    '$set': {
                        'closingDocumentReport': report_data,
                        'updatedAt': now
                    }
                }
            )
            
            if result.modified_count > 0:
                return self.get_loan_by_id(loan_id)
            return None
        except Exception as e:
            print(f"Error creating closing document report: {e}")
            return None
