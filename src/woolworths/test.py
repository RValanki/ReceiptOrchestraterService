import os
import sys
import json
import requests

# Config
RECEIPT_API_URL = "http://127.0.0.1:8000/parse-receipt/woolworths/"
BATCH_NUTRITION_URL = "http://127.0.0.1:8001/woolworths/nutrition/batch/"

# Get receipt PDF path from command line or use default
default_path = "/Users/rohitvalanki/ReceiptProcessingService/test/test-receipts/woolworths/e-receipts/eReceipt_3168_Endeavour%20Hills_03Feb2025__xjifb.pdf"
receipt_path = sys.argv[1] if len(sys.argv) > 1 else default_path

# Step 1: Send PDF to receipt parsing API
with open(receipt_path, "rb") as f:
    files = {"file": (os.path.basename(receipt_path), f, "application/pdf")}
    response = requests.post(RECEIPT_API_URL, files=files)

if response.status_code != 200:
    print("Error parsing receipt:", response.text)
    sys.exit(1)

receipt_data = response.json()
print("=== Parsed Receipt ===")
print(json.dumps(receipt_data, indent=2))

# Step 2: Extract product names
product_names = [item["name"] for item in receipt_data.get("items", [])]
print("Product Names:", product_names)

# Step 3: Call batch nutrition API
# Prepare params: multiple products as ?products=name1&products=name2
params = [("products", name) for name in product_names]
nutrition_response = requests.get(BATCH_NUTRITION_URL, params=params)

if nutrition_response.status_code != 200:
    print("Error fetching nutrition info:", nutrition_response.text)
    sys.exit(1)

nutrition_data = nutrition_response.json()
print("=== Nutrition Info ===")
print(json.dumps(nutrition_data, indent=2))
