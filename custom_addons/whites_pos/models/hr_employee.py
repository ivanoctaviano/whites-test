from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HREmployee(models.Model):
    _inherit = "hr.employee"

    refund_password = fields.Char(help="Used to store password for PoS Refund ")

    @api.model
    def get_password_refund(self, user_id):
        """
        Function to get Password Refund by User ID
        """
        emp_id = self.search([("user_id", "=", user_id)])
        return emp_id.refund_password
    
    @api.constrains("refund_password")
    def _verify_refund_password(self):
        """
        Function to check if the password only contain digit number
        """
        for employee in self:
            if employee.refund_password and not employee.refund_password.isdigit():
                raise ValidationError(_("The Refund Password must be a sequence of digits."))