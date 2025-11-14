import xml.etree.ElementTree as ET
from xml.dom import minidom

# ===== CONFIGURATION =====
input_file = "claims.txt"               # input file with claim numbers
output_file = "invoices.xml"            # output XML file
start_number = 588110                    # starting number for INV000XXXXX
prefix = "INV"                           # invoice prefix
# ==========================

def format_inv(n):
    return f"{prefix}{n:09d}"  # Produces INV000588110 format

# Load claim numbers
with open(input_file, "r") as f:
    claim_numbers = [line.strip() for line in f if line.strip()]

# XML root
root = ET.Element("Invoices")

current_num = start_number

for claim in claim_numbers:

    inv_id = format_inv(current_num)

    invoice = ET.SubElement(root, "Invoice")

    ET.SubElement(invoice, "VendorBillId").text = inv_id
    ET.SubElement(invoice, "PayeeTaxId").text = "833196914"
    ET.SubElement(invoice, "PayeeName").text = "Cadence Rx Inc."
    ET.SubElement(invoice, "ClaimNumber").text = claim
    ET.SubElement(invoice, "ClaimBusinessUnitCode").text = "sc"
    ET.SubElement(invoice, "InvoiceNumber").text = inv_id
    ET.SubElement(invoice, "ServiceFromDate").text = "2024-09-23"
    ET.SubElement(invoice, "ServiceToDate").text = "2024-09-23"
    ET.SubElement(invoice, "ExpenseCode").text = "519"
    ET.SubElement(invoice, "AmountDue").text = "10.00"

    # ---- Nested AdditionalDetail structure ----
    additional = ET.SubElement(invoice, "AdditionalDetail")
    med = ET.SubElement(additional, "MedicalDetail")

    patient = ET.SubElement(med, "Patient")
    ET.SubElement(patient, "FirstName").text = "WESLEY"
    ET.SubElement(patient, "LastName").text = "CLEMENT"
    ET.SubElement(patient, "DateOfInjury").text = "2024-09-09T00:00:00"

    diag = ET.SubElement(med, "DiagnosisCodes")
    ET.SubElement(diag, "PrimaryDiagnosticCode")

    ET.SubElement(med, "NDCNumber").text = "50228043301"
    ET.SubElement(med, "PrescriptionNumber").text = "0129754"
    ET.SubElement(med, "SupplyDays").text = "30"
    ET.SubElement(med, "PrescriberId").text = "1720245996"
    ET.SubElement(med, "DetailDescription").text = "Naproxen Sodium ORAL Tablet 55"
    ET.SubElement(med, "ServiceProviderTaxId").text = "274172156"
    ET.SubElement(med, "ServiceProviderName").text = "SIERRA PHARMACY"
    ET.SubElement(med, "ReferringProviderName").text = "SAEED NICK"

    current_num += 1  # increment

# Pretty print XML
rough = ET.tostring(root, "utf-8")
pretty = minidom.parseString(rough).toprettyxml(indent="    ")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(pretty)

print("✔ XML created:", output_file)

