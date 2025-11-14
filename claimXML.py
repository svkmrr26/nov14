import xml.etree.ElementTree as ET
from xml.dom import minidom

# ===== CONFIGURATION =====
input_file = "claims.txt"
output_file = "invoices.xml"
starting_invoice_number = 141702754
# ==========================

# Read claim numbers
with open(input_file, "r") as f:
    claim_numbers = [line.strip() for line in f if line.strip()]

# Create root element
root = ET.Element("Invoices")

invoice_number = starting_invoice_number

for claim in claim_numbers:
    invoice = ET.SubElement(root, "Invoice")

    ET.SubElement(invoice, "VendorBillId").text = "573321"
    ET.SubElement(invoice, "PayeeTaxId").text = "453641748"
    ET.SubElement(invoice, "PayeeName").text = "Acrometis"
    ET.SubElement(invoice, "ClaimNumber").text = claim
    ET.SubElement(invoice, "ClaimBusinessUnitCode").text = "sc"
    ET.SubElement(invoice, "InvoiceNumber").text = str(invoice_number)
    ET.SubElement(invoice, "OriginalInvoiceDate").text = "2023-01-16"
    ET.SubElement(invoice, "ServiceFromDate").text = "2020-06-22"
    ET.SubElement(invoice, "ServiceToDate").text = "2020-06-22"
    ET.SubElement(invoice, "ExpenseCode").text = "543"
    ET.SubElement(invoice, "AmountDue").text = "10.00"

    invoice_number += 1

# Pretty-print XML
rough_string = ET.tostring(root, 'utf-8')
reparsed = minidom.parseString(rough_string)
pretty_xml = reparsed.toprettyxml(indent="    ")

# Write to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(pretty_xml)

print("✔ XML generated successfully:", output_file)
