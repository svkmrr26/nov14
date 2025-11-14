import xml.etree.ElementTree as ET
from xml.dom import minidom

# ===== CONFIGURATION =====
input_file = "claims.txt"        # Insurer IDs, one per line
output_file = "claims.xml"

start_rquid = "93e28f7a-693a-43ff-be14-72d570625310"  # starting UUID
start_firm_invoice = 57637
start_invoice_id = 92770
start_matter_id = 92740
# ==========================

def increment_uuid(uuid_str, increment=1):
    """
    Treat UUID as a hex number, increment, and format back as UUID.
    """
    hex_str = uuid_str.replace("-", "")
    num = int(hex_str, 16) + increment
    new_hex = f"{num:032x}"
    # re-insert dashes
    return f"{new_hex[:8]}-{new_hex[8:12]}-{new_hex[12:16]}-{new_hex[16:20]}-{new_hex[20:32]}"

# Load Insurer IDs
with open(input_file, "r") as f:
    insurer_ids = [line.strip() for line in f if line.strip()]

# Root element
root = ET.Element("ClaimsSubsequentRptSubmitRqs")

# Initialize counters
rquid = start_rquid
firm_invoice = start_firm_invoice
invoice_id = start_invoice_id
matter_id = start_matter_id

for insurer in insurer_ids:

    rq = ET.SubElement(root, "ClaimsSubsequentRptSubmitRq")
    ET.SubElement(rq, "RqUID").text = rquid
    ET.SubElement(rq, "TransactionRequestDt").text = "202507286032025"
    ET.SubElement(rq, "CurCd").text = "USD"

    # ClaimsParty
    claims_party = ET.SubElement(rq, "ClaimsParty")
    general_info = ET.SubElement(claims_party, "GeneralPartyInfo")
    name_info = ET.SubElement(general_info, "NameInfo")
    comml_name = ET.SubElement(name_info, "CommlName")
    ET.SubElement(comml_name, "CommercialName").text = "GREAT AMERICAN INSURANCE COMPANY"
    tax_identity = ET.SubElement(name_info, "TaxIdentity")
    ET.SubElement(tax_identity, "TaxIdTypeCd").text = "FEIN"
    ET.SubElement(tax_identity, "TaxId").text = "310501234"

    addr = ET.SubElement(general_info, "Addr")
    ET.SubElement(addr, "Addr1").text = "301 E 4TH ST 19S"
    ET.SubElement(addr, "Addr2").text = "Claims Litigation Services"
    ET.SubElement(addr, "City").text = "Cincinnati"
    ET.SubElement(addr, "StateProvCd").text = "OH"
    ET.SubElement(addr, "PostalCode").text = "45202-4245"
    ET.SubElement(addr, "CountryCd").text = "USA"

    claims_party_info = ET.SubElement(claims_party, "ClaimsPartyInfo")
    ET.SubElement(claims_party_info, "ClaimsPartyRoleCd").text = "csc:FirmOffice"

    # ClaimsPayment
    claims_payment = ET.SubElement(rq, "ClaimsPayment")
    ET.SubElement(claims_payment, "FirmInvoiceNumber").text = str(firm_invoice)

    insured = ET.SubElement(claims_payment, "InsuredOrPrincipal")
    item = ET.SubElement(insured, "ItemIdInfo")

    ET.SubElement(item, "InsurerId").text = insurer

    # InvoiceId
    other1 = ET.SubElement(item, "OtherIdentifier")
    ET.SubElement(other1, "OtherIdTypeCd").text = "csc:InvoiceId"
    ET.SubElement(other1, "OtherId").text = str(invoice_id)

    # MatterId
    other2 = ET.SubElement(item, "OtherIdentifier")
    ET.SubElement(other2, "OtherIdTypeCd").text = "csc:MatterId"
    ET.SubElement(other2, "OtherId").text = str(matter_id)

    # PaymentSequence
    other3 = ET.SubElement(item, "OtherIdentifier")
    ET.SubElement(other3, "OtherIdTypeCd").text = "csc:PaymentSequence"
    ET.SubElement(other3, "OtherId").text = "1"

    # DivisionOfficeId
    other4 = ET.SubElement(item, "OtherIdentifier")
    ET.SubElement(other4, "OtherIdTypeCd").text = "csc:DivisionOfficeId"
    ET.SubElement(other4, "OtherId").text = "543"

    # Amounts
    invoice_amt = ET.SubElement(claims_payment, "InvoiceAmt")
    ET.SubElement(invoice_amt, "Amt").text = "100.00"

    final_amt = ET.SubElement(claims_payment, "FinalInvoiceAmt")
    ET.SubElement(final_amt, "Amt").text = "245.00"

    # EventInfo
    events = [
        ("csc:InvoiceDate", "2020-04-30"),
        ("csc:FinalDate", "2020-05-27"),
        ("csc:MinTaskDate", "2020-04-01"),
        ("csc:MaxTaskDate", "2020-04-30")
    ]

    for code, dt in events:
        event = ET.SubElement(claims_payment, "EventInfo")
        ET.SubElement(event, "EventCd").text = code
        ET.SubElement(event, "EventDt").text = dt

    # ClaimsPaymentDetail
    payment_detail = ET.SubElement(claims_payment, "ClaimsPaymentDetail")
    ET.SubElement(payment_detail, "PaymentTypeCd").text = "995"
    amt_node = ET.SubElement(payment_detail, "PaymentTypeAmt")
    ET.SubElement(amt_node, "Amt").text = "245.00"

    # Increment all counters
    rquid = increment_uuid(rquid)
    firm_invoice += 1
    invoice_id += 1
    matter_id += 1

# Pretty-print XML
rough = ET.tostring(root, "utf-8")
pretty = minidom.parseString(rough).toprettyxml(indent="    ")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(pretty)

print("✔ XML successfully created:", output_file)
