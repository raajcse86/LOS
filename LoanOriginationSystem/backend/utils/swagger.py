from flask_swagger_ui import get_swaggerui_blueprint
from flask import jsonify

# Swagger documentation configuration
SWAGGER_URL = '/api/swagger'
API_URL = '/api/swagger.json'

def get_swagger_spec():
    """Return the Swagger API specification."""
    return {
        "swagger": "2.0",
        "info": {
            "title": "Loan Origination System API",
            "description": "API documentation for the Loan Origination System",
            "version": "1.0.0"
        },
        "basePath": "/api",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {
                "name": "loans",
                "description": "Loan management operations"
            },
            {
                "name": "documents",
                "description": "Document management operations"
            },
            {
                "name": "users",
                "description": "User management operations"
            }
        ],
        "paths": {
            "/loans": {
                "get": {
                    "tags": ["loans"],
                    "summary": "Get all loans",
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/Loan"}
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["loans"],
                    "summary": "Create a new loan",
                    "parameters": [
                        {
                            "name": "loan",
                            "in": "body",
                            "description": "Loan object",
                            "required": True,
                            "schema": {"$ref": "#/definitions/Loan"}
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Loan created",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        }
                    }
                }
            },
            "/loans/{loanId}": {
                "get": {
                    "tags": ["loans"],
                    "summary": "Get a loan by ID",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/loans/{loanId}/employment": {
                "put": {
                    "tags": ["loans"],
                    "summary": "Update employment information",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "employmentInfo",
                            "in": "body",
                            "description": "Employment information",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "employmentInfo": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/loans/{loanId}/property": {
                "put": {
                    "tags": ["loans"],
                    "summary": "Update property information",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "propertyInfo",
                            "in": "body",
                            "description": "Property information",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "propertyInfo": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/loans/{loanId}/pricing": {
                "put": {
                    "tags": ["loans"],
                    "summary": "Update loan pricing information",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "loanPricing",
                            "in": "body",
                            "description": "Loan pricing information",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "loanPricing": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/loans/{loanId}/closing-fees": {
                "put": {
                    "tags": ["loans"],
                    "summary": "Update closing fees information",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "closingFees",
                            "in": "body",
                            "description": "Closing fees information",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "closingFees": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/loans/{loanId}/consent": {
                "put": {
                    "tags": ["loans"],
                    "summary": "Update consent information",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "consentInfo",
                            "in": "body",
                            "description": "Consent information",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "consentInfo": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/loans/{loanId}/milestone": {
                "put": {
                    "tags": ["loans"],
                    "summary": "Update loan milestone",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "milestone",
                            "in": "body",
                            "description": "Milestone information",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "milestone": {
                                        "type": "string",
                                        "enum": ["PreApplication", "Submitted", "IRR", "FRR", "ClosingDocsGenerated", "FundsDisbursed"]
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/loans/{loanId}/underwriter-report": {
                "post": {
                    "tags": ["loans"],
                    "summary": "Create underwriter report",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "report",
                            "in": "body",
                            "description": "Underwriter report",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "report": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/loans/{loanId}/closing-report": {
                "post": {
                    "tags": ["loans"],
                    "summary": "Create closing document report",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "report",
                            "in": "body",
                            "description": "Closing document report",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "report": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Loan"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "Loan not found"
                        }
                    }
                }
            },
            "/documents": {
                "get": {
                    "tags": ["documents"],
                    "summary": "Get all documents",
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/Document"}
                            }
                        }
                    }
                }
            },
            "/documents/{documentId}": {
                "get": {
                    "tags": ["documents"],
                    "summary": "Get a document by ID",
                    "parameters": [
                        {
                            "name": "documentId",
                            "in": "path",
                            "description": "ID of the document",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/Document"}
                        },
                        "404": {
                            "description": "Document not found"
                        }
                    }
                },
                "delete": {
                    "tags": ["documents"],
                    "summary": "Delete a document",
                    "parameters": [
                        {
                            "name": "documentId",
                            "in": "path",
                            "description": "ID of the document",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Document deleted successfully"
                        },
                        "404": {
                            "description": "Document not found"
                        },
                        "500": {
                            "description": "Error deleting document"
                        }
                    }
                }
            },
            "/documents/loan/{loanId}": {
                "get": {
                    "tags": ["documents"],
                    "summary": "Get documents by loan ID",
                    "parameters": [
                        {
                            "name": "loanId",
                            "in": "path",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/Document"}
                            }
                        }
                    }
                }
            },
            "/documents/upload": {
                "post": {
                    "tags": ["documents"],
                    "summary": "Upload a document",
                    "consumes": ["multipart/form-data"],
                    "parameters": [
                        {
                            "name": "file",
                            "in": "formData",
                            "description": "Document file",
                            "required": True,
                            "type": "file"
                        },
                        {
                            "name": "loanId",
                            "in": "formData",
                            "description": "ID of the loan",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "documentType",
                            "in": "formData",
                            "description": "Type of document",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Document uploaded successfully",
                            "schema": {"$ref": "#/definitions/Document"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "500": {
                            "description": "Error uploading document"
                        }
                    }
                }
            },
            "/documents/{documentId}/download": {
                "get": {
                    "tags": ["documents"],
                    "summary": "Download a document",
                    "parameters": [
                        {
                            "name": "documentId",
                            "in": "path",
                            "description": "ID of the document",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "produces": ["application/octet-stream"],
                    "responses": {
                        "200": {
                            "description": "Document file",
                            "schema": {
                                "type": "file"
                            }
                        },
                        "404": {
                            "description": "Document not found"
                        }
                    }
                }
            },
            "/documents/{documentId}/extract": {
                "get": {
                    "tags": ["documents"],
                    "summary": "Extract content from a document",
                    "parameters": [
                        {
                            "name": "documentId",
                            "in": "path",
                            "description": "ID of the document",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Content extraction successful",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "document_id": {"type": "string"},
                                    "extractedContent": {"type": "string"},
                                    "status": {"type": "string"}
                                }
                            }
                        },
                        "404": {
                            "description": "Document not found"
                        },
                        "500": {
                            "description": "Error extracting content"
                        }
                    }
                }
            },
            "/documents/{documentId}/compliance": {
                "get": {
                    "tags": ["documents"],
                    "summary": "Check compliance score for a document",
                    "parameters": [
                        {
                            "name": "documentId",
                            "in": "path",
                            "description": "ID of the document",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Compliance check successful",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "document_id": {"type": "string"},
                                    "complianceScore": {"type": "number"},
                                    "score": {"type": "number"},
                                    "status": {"type": "string"},
                                    "passed": {"type": "boolean"}
                                }
                            }
                        },
                        "404": {
                            "description": "Document not found"
                        },
                        "500": {
                            "description": "Error checking compliance"
                        }
                    }
                }
            },
            "/users": {
                "get": {
                    "tags": ["users"],
                    "summary": "Get all users",
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/User"}
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["users"],
                    "summary": "Create a new user",
                    "parameters": [
                        {
                            "name": "user",
                            "in": "body",
                            "description": "User object",
                            "required": True,
                            "schema": {"$ref": "#/definitions/User"}
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "User created",
                            "schema": {"$ref": "#/definitions/User"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "500": {
                            "description": "Error creating user"
                        }
                    }
                }
            },
            "/users/{userId}": {
                "get": {
                    "tags": ["users"],
                    "summary": "Get a user by ID",
                    "parameters": [
                        {
                            "name": "userId",
                            "in": "path",
                            "description": "ID of the user",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {"$ref": "#/definitions/User"}
                        },
                        "404": {
                            "description": "User not found"
                        }
                    }
                },
                "put": {
                    "tags": ["users"],
                    "summary": "Update a user",
                    "parameters": [
                        {
                            "name": "userId",
                            "in": "path",
                            "description": "ID of the user",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "user",
                            "in": "body",
                            "description": "User object",
                            "required": True,
                            "schema": {"$ref": "#/definitions/User"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "User updated",
                            "schema": {"$ref": "#/definitions/User"}
                        },
                        "400": {
                            "description": "Invalid input"
                        },
                        "404": {
                            "description": "User not found"
                        }
                    }
                },
                "delete": {
                    "tags": ["users"],
                    "summary": "Delete a user",
                    "parameters": [
                        {
                            "name": "userId",
                            "in": "path",
                            "description": "ID of the user",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "User deleted successfully"
                        },
                        "404": {
                            "description": "User not found"
                        }
                    }
                }
            },
            "/users/role/{role}": {
                "get": {
                    "tags": ["users"],
                    "summary": "Get users by role",
                    "parameters": [
                        {
                            "name": "role",
                            "in": "path",
                            "description": "Role of the users",
                            "required": True,
                            "type": "string",
                            "enum": ["Sales", "Processor", "Underwriter", "Closer", "Manager"]
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/User"}
                            }
                        }
                    }
                }
            }
        },
        "definitions": {
            "Loan": {
                "type": "object",
                "properties": {
                    "_id": {"type": "string"},
                    "borrowerInfo": {
                        "type": "object",
                        "properties": {
                            "firstName": {"type": "string"},
                            "lastName": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"},
                            "dob": {"type": "string"},
                            "ssn": {"type": "string"},
                            "address": {
                                "type": "object",
                                "properties": {
                                    "street": {"type": "string"},
                                    "city": {"type": "string"},
                                    "state": {"type": "string"},
                                    "zipCode": {"type": "string"}
                                }
                            },
                            "creditScore": {"type": "number"}
                        }
                    },
                    "employmentInfo": {
                        "type": "object",
                        "properties": {
                            "employmentStatus": {"type": "string"},
                            "employerName": {"type": "string"},
                            "jobTitle": {"type": "string"},
                            "startDate": {"type": "string"},
                            "endDate": {"type": "string"},
                            "monthlyIncome": {"type": "number"},
                            "employmentAddress": {
                                "type": "object",
                                "properties": {
                                    "street": {"type": "string"},
                                    "city": {"type": "string"},
                                    "state": {"type": "string"},
                                    "zipCode": {"type": "string"}
                                }
                            },
                            "employerPhone": {"type": "string"},
                            "yearsInIndustry": {"type": "number"}
                        }
                    },
                    "propertyInfo": {
                        "type": "object",
                        "properties": {
                            "propertyType": {"type": "string"},
                            "propertyUse": {"type": "string"},
                            "estimatedValue": {"type": "number"},
                            "purchasePrice": {"type": "number"},
                            "downPayment": {"type": "number"},
                            "loanAmount": {"type": "number"},
                            "propertyAddress": {
                                "type": "object",
                                "properties": {
                                    "street": {"type": "string"},
                                    "city": {"type": "string"},
                                    "state": {"type": "string"},
                                    "zipCode": {"type": "string"}
                                }
                            },
                            "yearBuilt": {"type": "number"},
                            "squareFootage": {"type": "number"},
                            "lotSize": {"type": "number"},
                            "numBedrooms": {"type": "number"},
                            "numBathrooms": {"type": "number"}
                        }
                    },
                    "loanPricing": {
                        "type": "object",
                        "properties": {
                            "interestRate": {"type": "number"},
                            "loanTerm": {"type": "number"},
                            "loanType": {"type": "string"},
                            "monthlyPayment": {"type": "number"},
                            "totalInterest": {"type": "number"},
                            "apr": {"type": "number"}
                        }
                    },
                    "closingFees": {
                        "type": "object",
                        "properties": {
                            "originationFee": {"type": "number"},
                            "appraisalFee": {"type": "number"},
                            "creditReportFee": {"type": "number"},
                            "titleFee": {"type": "number"},
                            "recordingFee": {"type": "number"},
                            "taxServiceFee": {"type": "number"},
                            "floodCertificationFee": {"type": "number"},
                            "underwritingFee": {"type": "number"},
                            "processingFee": {"type": "number"},
                            "additionalFees": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "amount": {"type": "number"}
                                    }
                                }
                            },
                            "totalClosingCosts": {"type": "number"}
                        }
                    },
                    "consentInfo": {
                        "type": "object",
                        "properties": {
                            "privacyPolicyConsent": {"type": "boolean"},
                            "termsOfServiceConsent": {"type": "boolean"},
                            "creditCheckConsent": {"type": "boolean"},
                            "electronicCommunicationConsent": {"type": "boolean"},
                            "signatureDate": {"type": "string"},
                            "signatureText": {"type": "string"}
                        }
                    },
                    "milestone": {
                        "type": "string",
                        "enum": ["PreApplication", "Submitted", "IRR", "FRR", "ClosingDocsGenerated", "FundsDisbursed"]
                    },
                    "createdAt": {"type": "string"},
                    "updatedAt": {"type": "string"},
                    "underwriterReport": {
                        "type": "object",
                        "properties": {
                            "approvalStatus": {"type": "string"},
                            "notes": {"type": "string"},
                            "complianceScore": {"type": "number"},
                            "riskAssessment": {"type": "string"},
                            "conditions": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    },
                    "closingDocumentReport": {
                        "type": "object",
                        "properties": {
                            "generatedDate": {"type": "string"},
                            "documentList": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "notes": {"type": "string"}
                        }
                    }
                }
            },
            "Document": {
                "type": "object",
                "properties": {
                    "_id": {"type": "string"},
                    "loanId": {"type": "string"},
                    "documentType": {"type": "string"},
                    "filename": {"type": "string"},
                    "originalFilename": {"type": "string"},
                    "fileSize": {"type": "number"},
                    "mimeType": {"type": "string"},
                    "uploadDate": {"type": "string"},
                    "uploadedBy": {"type": "string"},
                    "contentExtracted": {"type": "boolean"},
                    "complianceScore": {"type": "number"},
                    "extractedContent": {"type": "string"}
                }
            },
            "User": {
                "type": "object",
                "properties": {
                    "_id": {"type": "string"},
                    "username": {"type": "string"},
                    "firstName": {"type": "string"},
                    "lastName": {"type": "string"},
                    "email": {"type": "string"},
                    "role": {
                        "type": "string",
                        "enum": ["Sales", "Processor", "Underwriter", "Closer", "Manager"]
                    },
                    "createdAt": {"type": "string"},
                    "updatedAt": {"type": "string"}
                }
            }
        }
    }

def swagger_route():
    """Route handler for Swagger JSON specification."""
    return jsonify(get_swagger_spec())

def init_swagger(app):
    """Initialize Swagger UI for the Flask app."""
    # Create Swagger blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Loan Origination System API"
        }
    )
    
    # Register blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Add route for Swagger JSON
    app.route(API_URL, methods=['GET'])(swagger_route)
