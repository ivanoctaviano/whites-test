from odoo import fields, models, _


class AccountAccount(models.Model):
    _inherit = "account.account"

    mandatory_analytic_account = fields.Boolean(help="If mandatory_analytic_account=True, the journal item must include an analytic account.")
    mandatory_partner = fields.Boolean(help="If mandatory_partner=True, the journal item must include a partner.")
    bypass_users_ids = fields.Many2many("res.users", help="If the logged-in user is listed in bypass_users_ids, they should be exempt from these validations.")