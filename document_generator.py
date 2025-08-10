import os
import tempfile
from docxtpl import DocxTemplate
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentGenerator:
    def __init__(self):
        self.templates_dir = "templates"
        self.invoice_template = os.path.join(self.templates_dir, "Billing Invoice.docx")
        self.delivery_receipt_template = os.path.join(self.templates_dir, "Delivery Receipt.docx")
        
        # Verify templates exist
        if not os.path.exists(self.invoice_template):
            logger.warning(f"Invoice template not found: {self.invoice_template}")
        if not os.path.exists(self.delivery_receipt_template):
            logger.warning(f"Delivery receipt template not found: {self.delivery_receipt_template}")
    
    def generate_invoice(self, data):
        """
        Generate an invoice document from template using docxtpl
        """
        try:
            logger.info(f"Generating invoice with data: {data}")
            
            # Load the template document
            if not os.path.exists(self.invoice_template):
                raise Exception(f"Invoice template not found: {self.invoice_template}")
            
            # Create DocxTemplate object
            doc = DocxTemplate(self.invoice_template)
            logger.info("Invoice template loaded successfully")
            
            # Render the template with the provided data
            doc.render(data)
            logger.info("Invoice template rendered successfully")
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
            doc.save(temp_file.name)
            logger.info(f"Invoice saved to: {temp_file.name}")
            
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Error generating invoice: {str(e)}")
            raise Exception(f"Error generating invoice: {str(e)}")
    
    def generate_delivery_receipt(self, data):
        """
        Generate a delivery receipt document from template using docxtpl
        """
        try:
            logger.info(f"Generating delivery receipt with data: {data}")
            
            # Load the template document
            if not os.path.exists(self.delivery_receipt_template):
                raise Exception(f"Delivery receipt template not found: {self.delivery_receipt_template}")
            
            # Create DocxTemplate object
            doc = DocxTemplate(self.delivery_receipt_template)
            logger.info("Delivery receipt template loaded successfully")
            
            # Render the template with the provided data
            doc.render(data)
            logger.info("Delivery receipt template rendered successfully")
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
            doc.save(temp_file.name)
            logger.info(f"Delivery receipt saved to: {temp_file.name}")
            
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Error generating delivery receipt: {str(e)}")
            raise Exception(f"Error generating delivery receipt: {str(e)}") 