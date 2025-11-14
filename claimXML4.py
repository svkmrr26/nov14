import xml.etree.ElementTree as ET
from xml.dom import minidom

# ===== CONFIGURATION =====
input_file = "claims.txt"        # file containing ClaimIDs, one per line
output_file = "provider_recommendations.xml"
# ==========================

# Load Claim IDs
with open(input_file, "r") as f:
    claim_ids = [line.strip() for line in f if line.strip()]

# Root element
root = ET.Element("ProviderRecommendationsList")  # wrapper root

for claim in claim_ids:
    provider_rec = ET.SubElement(root, "ProviderRecommendations")

    # ProviderRef
    ET.SubElement(provider_rec, "ProviderRef").text = "FIC-GAIC-1043075"

    # ClaimRecommendations
    claim_rec = ET.SubElement(provider_rec, "ClaimRecommendations")
    ET.SubElement(claim_rec, "ClaimRef").text = "FIC-GAIC-491336"

    bill_recs = ET.SubElement(claim_rec, "BillRecommendations")
    ET.SubElement(bill_recs, "BillRef").text = "FIC-48AZ-12679"

    bill = ET.SubElement(bill_recs, "Bill")

    bill_header = ET.SubElement(bill, "BillHeader")
    ET.SubElement(bill_header, "GlobalBillID").text = "FIC-48AZ-12679"
    ET.SubElement(bill_header, "GlobalProviderID").text = "FIC-GAIC-1043075"
    ET.SubElement(bill_header, "GlobalClaimID").text = "FIC-GAIC-491336"
    ET.SubElement(bill_header, "GlobalBranchID").text = "FIC-GAIC-16"
    ET.SubElement(bill_header, "GlobalAdjusterID").text = "FIC-GAIC-cci2u9:10003"
    ET.SubElement(bill_header, "ExternalProviderID").text = "2216350"

    # Only change ClaimID
    ET.SubElement(bill_header, "ClaimID").text = claim

    # Copy the rest as static values
    static_fields = {
        "PolicyID": "715340100WC 04",
        "BranchID": "group:11000",
        "Adjuster": "cci2u9:10003",
        "StateDisclaimerID": "AZ",
        "DateOfInjury": "2018-04-12",
        "NetworkServiceCode": "N",
        "BillingProvTaxonomyCode": "225100000X",
        "ProvType": "PT",
        "TIN": "943355101",
        "RenderingProvLastName": "X",
        "ProvZip": "85086",
        "Region": "0",
        "StateTypeOfBill": "M",
        "ClientTypeOfBill": "501",
        "ServiceLineCount": "1",
        "ProductCode": "F",
        "SubProductCode": "B",
        "DOSFirst": "2021-05-01",
        "DOSLast": "2021-05-01",
        "ProvConsultDate": "1900-01-01",
        "AdmissionDate": "1900-01-01",
        "DischargeDate": "1900-01-01",
        "SubmitDate": "1900-01-01",
        "CarrierReceiveDate": "2021-05-25",
        "BRReceiveDate": "2021-05-25",
        "ReviewDate": "2021-05-25",
        "PostDate": "2021-05-25",
        "DueDate": "1900-01-01",
        "AdjusterVerifReqDate": "1900-01-01",
        "AdjusterVerifRecDate": "1900-01-01",
        "PaidDate": "1900-01-01",
        "PmtAuth": "PP",
        "Status": "B",
        "CreateUserID": "M8",
        "ModUserID": "M8",
        "DRGValue": "0.00",
        "Jurisdiction": "AZ",
        "NYSurchargeTimelyFilingRate": "0.00",
        "NYSurchargeLateFilingRate": "0.00",
        "BillCharge": "100.00",
        "ICDVersion": "10",
        "DocCtrlID": "54488771",
        "TotalBillCharge": "100.00",
        "CAInpatientMultiplier": "0.0000",
        "CompositeFactor": "0.00",
        "DRGWeight": "0.0000",
        "GlobalDRGFee": "0.00",
        "RetailSalesTaxZip": "45202",
        "BillableLines": "1",
        "GeoState": "AZ",
        "ProvState": "AZ",
        "ReevalAllow": "0.00",
        "CreateDate": "2021-05-25",
        "ModDate": "2021-05-25",
        "PPONetworkJurInsurerSeq": "0",
        "ContactEmail": "ML_Irvine_Teamleads@Mitchell.com",
        "ContactPhoneNum": "800-732-0153",
        "PlaceOfService": "11",
        "DRGDischargeFraction": "0.00",
        "TotalPayable": "100.00",
        "AlternatePaytoProviderIndicator": "N"
    }

    for k, v in static_fields.items():
        ET.SubElement(bill_header, k).text = v

# Pretty-print XML
rough = ET.tostring(root, "utf-8")
pretty = minidom.parseString(rough).toprettyxml(indent="    ")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(pretty)

print("✔ XML created:", output_file)
