class Document:
    """
    Document model representing the structure of document data.
    This is used for documentation and validation.
    """
    
    def __init__(
        self,
        loan_id,
        document_type,
        filename,
        original_filename,
        file_size,
        mime_type,
        upload_date=None,
        uploaded_by=None,
        content_extracted=False,
        compliance_score=None,
        extracted_content=None
    ):
        self.loan_id = loan_id
        self.document_type = document_type
        self.filename = filename
        self.original_filename = original_filename
        self.file_size = file_size
        self.mime_type = mime_type
        self.upload_date = upload_date
        self.uploaded_by = uploaded_by
        self.content_extracted = content_extracted
        self.compliance_score = compliance_score
        self.extracted_content = extracted_content
    
    def to_dict(self):
        """Convert document object to dictionary."""
        return {
            "loanId": self.loan_id,
            "documentType": self.document_type,
            "filename": self.filename,
            "originalFilename": self.original_filename,
            "fileSize": self.file_size,
            "mimeType": self.mime_type,
            "uploadDate": self.upload_date,
            "uploadedBy": self.uploaded_by,
            "contentExtracted": self.content_extracted,
            "complianceScore": self.compliance_score,
            "extractedContent": self.extracted_content
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create document object from dictionary."""
        return cls(
            loan_id=data.get("loanId"),
            document_type=data.get("documentType"),
            filename=data.get("filename"),
            original_filename=data.get("originalFilename"),
            file_size=data.get("fileSize"),
            mime_type=data.get("mimeType"),
            upload_date=data.get("uploadDate"),
            uploaded_by=data.get("uploadedBy"),
            content_extracted=data.get("contentExtracted", False),
            compliance_score=data.get("complianceScore"),
            extracted_content=data.get("extractedContent")
        )
