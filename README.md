# Document Generation API

A FastAPI-based Python application for generating invoice and delivery receipt documents from Word templates using [python-docx-template (docxtpl)](https://docxtpl.readthedocs.io/en/latest/).

## Features

- Generate invoice documents from templates
- Generate delivery receipt documents from templates
- RESTful API endpoints
- Deployable on Vercel
- Uses docxtpl for professional Word document templating with Jinja2
- Automatic handling of complex Jinja2 syntax in Word documents

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy to Vercel:
```bash
vercel
```

## API Endpoints

### Generate Invoice

**POST** `/generate-invoice`

Generates an invoice document based on the provided data.

**Request Body:**
```json
{
  "companyName": "string",
  "invoiceNo": "string",
  "tin": "string",
  "date": "string",
  "companyAddress": "string",
  "poNumber": "string",
  "items": [
    {
      "qty": 1,
      "unit": "piece",
      "description": "Product description",
      "price": "100.00",
      "amount": "100.00"
    }
  ],
  "totals": [
    {
      "name": "Subtotal",
      "amount": "100.00"
    },
    {
      "name": "Total",
      "amount": "100.00"
    }
  ]
}
```

**Response:** Returns the generated Word document file.

### Generate Delivery Receipt

**POST** `/generate-delivery-receipt`

Generates a delivery receipt document based on the provided data.

**Request Body:**
```json
{
  "deliveryNo": "string",
  "companyName": "string",
  "date": "string",
  "poNumber": "string",
  "invoiceNo": "string",
  "items": [
    {
      "index": 1,
      "qty": 1,
      "description": "Product description"
    }
  ]
}
```

**Response:** Returns the generated Word document file.

## Template Structure

The application expects Word document templates in the `templates/` folder:

- `Billing Invoice.docx` - Invoice template
- `Delivery Receipt.docx` - Delivery receipt template

### Jinja2 Template Variables

**docxtpl** automatically handles all Jinja2 syntax in your Word documents. Here are the supported syntax patterns:

#### Basic Variables:
- `{{ companyName }}` - Company name
- `{{ invoiceNo }}` - Invoice number
- `{{ tin }}` - TIN number
- `{{ date }}` - Invoice date
- `{{ companyAddress }}` - Company address
- `{{ poNumber }}` - Purchase order number

#### Loop Variables:
- `{{ item.qty }}` - Item quantity
- `{{ item.unit }}` - Item unit
- `{{ item.description }}` - Item description
- `{{ item.price }}` - Item price
- `{{ item.amount }}` - Item amount
- `{{ total.name }}` - Total line name
- `{{ total.amount }}` - Total line amount

#### Advanced Jinja2 Features:
- **Conditionals**: `{% if condition %}...{% endif %}`
- **Loops**: `{% for item in items %}...{% endfor %}`
- **Comments**: `{# This is a comment #}`
- **Special Tags**:
  - `{%p ... %}` for paragraph-level operations
  - `{%tr ... %}` for table row operations
  - `{%tc ... %}` for table column operations
  - `{%r ... %}` for run-level operations

#### Template Example:
```
Company: {{ companyName }}
Invoice: {{ invoiceNo }}
Date: {{ date }}

Items:
{% for item in items %}
{{ item.qty }} {{ item.unit }} - {{ item.description }} - {{ item.price }} - {{ item.amount }}
{% endfor %}

Totals:
{% for total in totals %}
{{ total.name }}: {{ total.amount }}
{% endfor %}
```

## Example Usage

### Using curl

```bash
# Generate invoice
curl -X POST "http://localhost:8000/generate-invoice" \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "Sample Company",
    "invoiceNo": "INV-001",
    "tin": "123456789",
    "date": "2024-01-15",
    "companyAddress": "123 Main St, City, Country",
    "poNumber": "PO-001",
    "items": [
      {
        "qty": 2,
        "unit": "pieces",
        "description": "Sample Product",
        "price": "50.00",
        "amount": "100.00"
      }
    ],
    "totals": [
      {
        "name": "Subtotal",
        "amount": "100.00"
      },
      {
        "name": "Total",
        "amount": "100.00"
      }
    ]
  }' \
  --output invoice_INV-001.docx

# Generate delivery receipt
curl -X POST "http://localhost:8000/generate-delivery-receipt" \
  -H "Content-Type: application/json" \
  -d '{
    "deliveryNo": "DR-001",
    "companyName": "Sample Company",
    "date": "2024-01-15",
    "poNumber": "PO-001",
    "invoiceNo": "INV-001",
    "items": [
      {
        "index": 1,
        "qty": 2,
        "description": "Sample Product"
      }
    ]
  }' \
  --output delivery_receipt_DR-001.docx
```

### Using JavaScript/Fetch

```javascript
// Generate invoice
const invoiceData = {
  companyName: "Sample Company",
  invoiceNo: "INV-001",
  tin: "123456789",
  date: "2024-01-15",
  companyAddress: "123 Main St, City, Country",
  poNumber: "PO-001",
  items: [
    {
      qty: 2,
      unit: "pieces",
      description: "Sample Product",
      price: "50.00",
      amount: "100.00"
    }
  ],
  totals: [
    {
      name: "Subtotal",
      amount: "100.00"
    },
    {
      name: "Total",
      amount: "100.00"
    }
  ]
};

fetch('/generate-invoice', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(invoiceData)
})
.then(response => response.blob())
.then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'invoice_INV-001.docx';
  a.click();
});
```

## Project Structure

```
├── main.py                 # FastAPI application
├── document_generator.py   # Document generation logic using docxtpl
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
├── runtime.txt            # Python runtime version
├── templates/             # Word document templates
│   ├── Billing Invoice.docx
│   └── Delivery Receipt.docx
├── test_api.py            # Test script for API verification
└── README.md              # This file
```

## Dependencies

- **FastAPI** - Web framework
- **docxtpl** - Professional Word document templating with Jinja2 support
- **Pydantic** - Data validation
- **uvicorn** - ASGI server

## Template Best Practices

1. **Use proper spacing**: Always put spaces after starting tags and before ending tags
   - ✅ `{{ companyName }}`
   - ❌ `{{companyName}}`

2. **Handle loops properly**: Use the special tags for table operations
   - `{%tr for item in items %}` for table rows
   - `{%tc for item in items %}` for table columns

3. **Test your templates**: Create simple test documents first before complex ones

4. **Use comments**: Add `{# comment #}` to document your template logic

## Troubleshooting

- **Template not found**: Ensure your Word documents are in the `templates/` folder
- **Syntax errors**: Check that Jinja2 syntax follows the spacing rules
- **Complex tables**: Use the special table tags (`{%tr`, `{%tc`) for better control

## License

MIT License 