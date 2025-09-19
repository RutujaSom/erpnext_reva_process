import frappe
from frappe.model.document import Document
import string
import random

"""Send mail o supplier for at the time od creatiion"""
def after_supplier_insert(self):
    print('after_supplier_insert .....',self.workflow_state)
    # Get supplier email (assuming you have an email field)
    supplier_email = self.email_id  # replace with your actual fieldname
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



def after_supplier_approved(self):
    """
        Trigger custom logic after Supplier document is updated post submission.
        Handles creation of User accounts and notification emails based on workflow state.
    """
    # APPROVED SUPPLIER
    if self.workflow_state == "Approved":
        # Check if user already exists
        existing_user = frappe.db.exists("User", self.email_id)
        if not existing_user:
            # Generate random 10-char password
            characters = string.ascii_letters + string.digits
            password = ''.join(random.choices(characters, k=10))

            # Create new User
            user = frappe.get_doc({
                "doctype": "User",
                "email": self.email_id,
                "first_name": self.supplier_name,
                "enabled": 1,
                "send_welcome_email": 0,
                "roles": [{"role": "Supplier"}]
            })
            user.insert(ignore_permissions=True)

            # Set password for the new user
            frappe.utils.password.update_password(user.name, password)

            # Email message with login details
            message = f"""
            <p>Dear <b>{self.supplier_name}</b>,</p>
            <p>Congratulations! Your supplier registration has been <b>approved</b>.</p>
            <p>Your supplier portal account has been created. Please use the following credentials to log in:</p>
            <table style="border:1px solid #ddd; padding:10px;">
            <tr>
                <td><b>Username (Email)</b></td>
                <td>{self.email_id}</td>
            </tr>
            <tr>
                <td><b>Password</b></td>
                <td>{password}</td>
            </tr>
            </table>
            <p>You can log in here: <a href="{frappe.utils.get_url('/login')}">{frappe.utils.get_url('/login')}</a></p>
            <p style="margin-top:20px;">Best regards,<br>[Your Company Name]</p>
            """

            frappe.sendmail(
                recipients=[self.email_id],
                subject="Supplier Registration Approved",
                message=message
            )

    # REJECTED SUPPLIER
    elif self.workflow_state == "Rejected":
        message = f"""
        <p>Dear <b>{self.supplier_name}</b>,</p>
        <p>We regret to inform you that your supplier registration has been <b>rejected</b>.</p>
        <p>For further details, please contact us.</p>
        <p style="margin-top:20px;">Best regards,<br>[Your Company Name]</p>
        """
        frappe.sendmail(
            recipients=[self.email_id],
            subject="Supplier Registration Rejected",
            message=message
        )

