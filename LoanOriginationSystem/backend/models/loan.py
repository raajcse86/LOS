class Loan:
    """
    Loan model representing the structure of loan data.
    This is used for documentation and validation.
    """
    
    def __init__(
        self,
        borrower_info=None,
        employment_info=None,
        property_info=None,
        loan_pricing=None,
        closing_fees=None,
        consent_info=None,
        milestone="PreApplication",
        underwriter_report=None,
        closing_document_report=None
    ):
        self.borrower_info = borrower_info
        self.employment_info = employment_info
        self.property_info = property_info
        self.loan_pricing = loan_pricing
        self.closing_fees = closing_fees
        self.consent_info = consent_info
        self.milestone = milestone
        self.underwriter_report = underwriter_report
        self.closing_document_report = closing_document_report
    
    def to_dict(self):
        """Convert loan object to dictionary."""
        return {
            "borrowerInfo": self.borrower_info,
            "employmentInfo": self.employment_info,
            "propertyInfo": self.property_info,
            "loanPricing": self.loan_pricing,
            "closingFees": self.closing_fees,
            "consentInfo": self.consent_info,
            "milestone": self.milestone,
            "underwriterReport": self.underwriter_report,
            "closingDocumentReport": self.closing_document_report
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create loan object from dictionary."""
        return cls(
            borrower_info=data.get("borrowerInfo"),
            employment_info=data.get("employmentInfo"),
            property_info=data.get("propertyInfo"),
            loan_pricing=data.get("loanPricing"),
            closing_fees=data.get("closingFees"),
            consent_info=data.get("consentInfo"),
            milestone=data.get("milestone", "PreApplication"),
            underwriter_report=data.get("underwriterReport"),
            closing_document_report=data.get("closingDocumentReport")
        )
