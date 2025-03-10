from odoo import api, fields, models


class UnifiedSaleReport(models.TransientModel):
    _name = "unified.sale.report"
    _description = "Sales Analysis Report"
    _order = "date desc"

    date = fields.Date("Order Date", readonly=True)
    product_id = fields.Many2one("product.product", "Product Variant", readonly=True)
    product_qty = fields.Float("Qty Ordered", readonly=True)
    price_subtotal = fields.Float("Total Order Amount", readonly=True)

    def refresh_matview(self):
        """
        Cron function to refresh materialized view Unified Sale Dataset
        """
        self._cr.execute("REFRESH MATERIALIZED VIEW unified_sale_matview;")
