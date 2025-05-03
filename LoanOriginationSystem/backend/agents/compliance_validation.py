import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

def get_compliance_report(document_content,document_rules):
    compliance_validation_prompt = f"""
    You are a compliance officer. Based on the following guidelines, please verify the uploaded documents for compliance.
    - Ensure that all required documents are present.
    - Ensure that the documents meet regulatory standards outlined in the guideline.

    For each uploaded document, check by referring the guidelines:
    - Does the document match the required format (e.g., PDF, signed)?
    - Are all fields in the document properly filled out (e.g., name, loan amount, income)?
    - Are there any discrepancies with the guideline?

    Return the validation results in structured JSON format with:
    - Summarized_Financial_Health : Mention the details about the applicant financial health by analyzing the document
    - Compliance_Assessment : Give a clear cut report by analyzing and validating the document against the guidelines provided
    - Risk_Analysis: If any risks found , mention in detail about what are the risks , if there isn't any then mention about that.
    - Compliance_score: Give an accurate compliance score by calculating it with the help of the analyzed compliance validation and risks
    - Decision: If the compliance score is above 85 the mark as "approved" or else "rejected"

    Ensure the response is **valid JSON** with **NO extra text** before or after.
    
    Regulatory Guideline: {document_rules}
    Uploaded Document: {document_content}
    """
    response = chat([HumanMessage(content=compliance_validation_prompt)])
    print(response.content[7:-3])
    return response.content[7:-3]