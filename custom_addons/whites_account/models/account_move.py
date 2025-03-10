from odoo import models, api, _
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.constrains("account_id", "analytic_account_id", "partner_id", "parent_state")
    def _check_constrains_mandatory_analytic_account_partner(self):
        """
        Function constraint to check mandatory Analytic Account & Partner in Journal Items
        """
        for line in self.filtered(lambda x: x.display_type not in ("line_section", "line_note")):
            account = line.account_id
            mandatory_analytic_account = account.mandatory_analytic_account
            mandatory_partner = account.mandatory_partner
            if mandatory_analytic_account or mandatory_partner:
                if self.env.user.id not in account.bypass_users_ids.ids:
                    if mandatory_analytic_account and not line.analytic_account_id:
                        raise UserError(_("The account %s forces to fill the analytic account.") % (account.code + " " + account.name))
                    if mandatory_partner and not line.partner_id:
                        raise UserError(_("The account %s forces to fill the partner.") % (account.code + " " + account.name))