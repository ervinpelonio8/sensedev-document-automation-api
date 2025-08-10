from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
from document_generator import DocumentGenerator

app = FastAPI(title="Document Generation API", version="1.0.0")

# Pydantic models for request validation
class InvoiceItem(BaseModel):
    qty: int
    unit: str
    description: str
    price: str
    amount: str

class InvoiceTotal(BaseModel):
    name: str
    amount: str

class InvoiceRequest(BaseModel):
    companyName: str
    invoiceNo: str
    tin: str
    date: str
    companyAddress: str
    poNumber: str
    items: List[InvoiceItem]
    totals: List[InvoiceTotal]

class DeliveryReceiptItem(BaseModel):
    index: int
    qty: int
    description: str

class DeliveryReceiptRequest(BaseModel):
    deliveryNo: str
    companyName: str
    date: str
    poNumber: str
    invoiceNo: str
    items: List[DeliveryReceiptItem]

# Initialize document generator
doc_generator = DocumentGenerator()

@app.get("/")
async def root():
    return {"message": "Document Generation API", "version": "1.0.0"}

@app.post("/generate-invoice")
async def generate_invoice(request: InvoiceRequest):
    """
    Generate an invoice document based on the provided data
    """
    try:
        # Convert request to dictionary format expected by template
        data = {
            "companyName": request.companyName,
            "invoiceNo": request.invoiceNo,
            "tin": request.tin,
            "date": request.date,
            "companyAddress": request.companyAddress,
            "poNumber": request.poNumber,
            "items": [item.model_dump() for item in request.items],
            "totals": [total.model_dump() for total in request.totals]
        }
        
        # Generate the document
        output_path = doc_generator.generate_invoice(data)
        
        # Return the generated file
        return FileResponse(
            path=output_path,
            filename=f"invoice_{request.invoiceNo}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating invoice: {str(e)}")

@app.post("/generate-delivery-receipt")
async def generate_delivery_receipt(request: DeliveryReceiptRequest):
    """
    Generate a delivery receipt document based on the provided data
    """
    try:
        # Convert request to dictionary format expected by template
        data = {
            "deliveryNo": request.deliveryNo,
            "companyName": request.companyName,
            "date": request.date,
            "poNumber": request.poNumber,
            "invoiceNo": request.invoiceNo,
            "items": [item.model_dump() for item in request.items]
        }
        
        # Generate the document
        output_path = doc_generator.generate_delivery_receipt(data)
        
        # Return the generated file
        return FileResponse(
            path=output_path,
            filename=f"delivery_receipt_{request.deliveryNo}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating delivery receipt: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 