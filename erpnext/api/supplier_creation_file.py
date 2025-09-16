import frappe
from frappe.model.document import Document

def after_supplier_insert(self):
    # Get supplier email (assuming you have an email field)
    supplier_email = self.email_id  # replace with your actual fieldname
    print("supplier_email .....",supplier_email)
    if supplier_email:
        subject = "Welcome to Our System"
        message = f"""
            <p>Dear {self.supplier_name},</p>
            <p>Thank you for registering as a supplier with us.</p>
            <p>We look forward to working with you.</p>
        """

        # Send email
        frappe.sendmail(
            recipients=[supplier_email],
            subject=subject,
            message=message
        )
