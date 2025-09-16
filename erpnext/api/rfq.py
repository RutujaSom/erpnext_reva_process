import frappe

@frappe.whitelist()
def unlock_rfq(rfq_name):
    print(rfq_name,'...////')
    rfq = frappe.get_doc("Request for Quotation", rfq_name)
    if rfq.docstatus != 1:
        frappe.throw("Only submitted RFQs can be unlocked.")

    # Instead of a new field → downgrade docstatus temporarily
    rfq.db_set("docstatus", 0)
    return True





@frappe.whitelist()
def get_suppliers_by_group(supplier_group):
    print("supplier_group .....",supplier_group)
    suppliers = frappe.get_all(
        "Supplier",
        filters={"supplier_group": supplier_group},
        fields=["name", "supplier_name"]
    )
    return suppliers
