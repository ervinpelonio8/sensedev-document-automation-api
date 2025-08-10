import requests
import json
import os

# API base URL (change this to your deployed URL when testing)
BASE_URL = "http://localhost:8000"

def test_invoice_generation():
    """Test invoice generation endpoint"""
    print("Testing invoice generation...")
    
    invoice_data = {
        "companyName": "Sample Company Inc.",
        "invoiceNo": "INV-2024-001",
        "tin": "123456789",
        "date": "2024-01-15",
        "companyAddress": "123 Main Street, City, Country 12345",
        "poNumber": "PO-2024-001",
        "items": [
            {
                "qty": 2,
                "unit": "pieces",
                "description": "Laptop Computer",
                "price": "1500.00",
                "amount": "3000.00"
            },
            {
                "qty": 1,
                "unit": "piece",
                "description": "Wireless Mouse",
                "price": "25.00",
                "amount": "25.00"
            },
            {
                "qty": 3,
                "unit": "pieces",
                "description": "USB Flash Drive 32GB",
                "price": "15.00",
                "amount": "45.00"
            }
        ],
        "totals": [
            {
                "name": "Subtotal",
                "amount": "3070.00"
            },
            {
                "name": "Tax (10%)",
                "amount": "307.00"
            },
            {
                "name": "Total",
                "amount": "3377.00"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-invoice",
            json=invoice_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # Save the generated file
            filename = f"test_invoice_{invoice_data['invoiceNo']}.docx"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Invoice generated successfully: {filename}")
            return True
        else:
            print(f"❌ Error generating invoice: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False

def test_delivery_receipt_generation():
    """Test delivery receipt generation endpoint"""
    print("\nTesting delivery receipt generation...")
    
    delivery_data = {
        "deliveryNo": "DR-2024-001",
        "companyName": "Sample Company Inc.",
        "date": "2024-01-15",
        "poNumber": "PO-2024-001",
        "invoiceNo": "INV-2024-001",
        "items": [
            {
                "index": 1,
                "qty": 2,
                "description": "Laptop Computer"
            },
            {
                "index": 2,
                "qty": 1,
                "description": "Wireless Mouse"
            },
            {
                "index": 3,
                "qty": 3,
                "description": "USB Flash Drive 32GB"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-delivery-receipt",
            json=delivery_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # Save the generated file
            filename = f"test_delivery_receipt_{delivery_data['deliveryNo']}.docx"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Delivery receipt generated successfully: {filename}")
            return True
        else:
            print(f"❌ Error generating delivery receipt: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False

def test_api_health():
    """Test API health endpoint"""
    print("Testing API health...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            print("✅ API is healthy")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API tests...\n")
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API health check failed. Make sure the server is running.")
        return
    
    # Test invoice generation
    invoice_success = test_invoice_generation()
    
    # Test delivery receipt generation
    delivery_success = test_delivery_receipt_generation()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"API Health: {'✅ PASS' if True else '❌ FAIL'}")
    print(f"Invoice Generation: {'✅ PASS' if invoice_success else '❌ FAIL'}")
    print(f"Delivery Receipt Generation: {'✅ PASS' if delivery_success else '❌ FAIL'}")
    
    if invoice_success and delivery_success:
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main() 