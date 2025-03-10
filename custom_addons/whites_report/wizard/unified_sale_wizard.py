from odoo import fields, models, _


class UnifedSaleWizard(models.TransientModel):
    _name = "unified.sale.wizard"
    _description = "Unified Sale Report Wizard"

    date_start = fields.Date(help="Filter the date range to generate unified sale report")
    date_end = fields.Date()

    def _get_distinct_months(self):
        """
        Function to get distinct month from date filter
        """
        query = """
SELECT DISTINCT TO_CHAR(DATE_TRUNC('month', date_order), 'YYYY-MM-01') AS sales_month
FROM unified_sale_matview
WHERE date_order BETWEEN %(date_start)s AND %(date_end)s
"""
        
        self._cr.execute(query, {
            "date_start": self.date_start,
            "date_end": self.date_end,
        })

        months = self._cr.fetchall()
        return months
    
    def _convert_months(self, months):
        """
        Convert months to dynamic column for pivot view
        """
        month_qty = " NUMERIC, ".join("qty" + str(month[0]).replace("-", "_") for month in months) + " NUMERIC"
        month_sales = " NUMERIC, ".join("sales" + str(month[0]).replace("-", "_") for month in months) + " NUMERIC"
        processing_categ = " , ".join("qty" + str(month[0]).replace("-", "_") + ", sales" + str(month[0]).replace("-", "_") for month in months)
        return month_qty, month_sales, processing_categ
    
    def _create_pivot(self, month_qty, month_sales):
        """
        Create Pivot View using SQL Pivot crosstab
        """
        query = """
-- Drop the view if it exists
DROP VIEW IF EXISTS product_sale_pivot_qty CASCADE;
DROP VIEW IF EXISTS product_sale_pivot_amount CASCADE;

-- Create view storing qty data per month
CREATE VIEW product_sale_pivot_qty AS
SELECT * FROM crosstab(
	'SELECT 
		product_id,
		TO_CHAR(DATE_TRUNC(''month'', date_order), ''YYYY-MM-01'') AS month_qty,
		COALESCE(SUM(total_quantity), 0) AS total_quantity
	FROM unified_sale_matview
    WHERE date_order BETWEEN '%(date_start)s' AND '%(date_end)s'
	GROUP BY product_id, month_qty
    ORDER BY product_id, month_qty',
	'SELECT DISTINCT TO_CHAR(DATE_TRUNC(''month'', date_order), ''YYYY-MM-01'') AS month_qty 
     FROM unified_sale_matview
     WHERE date_order BETWEEN '%(date_start)s' AND '%(date_end)s'
     ORDER BY 1'
) AS pivot_table (
	product_id INTEGER,
	{month_qty}
);

-- Create view storing amount data per month                         
CREATE VIEW product_sale_pivot_amount AS
SELECT * FROM crosstab(
	'SELECT 
		product_id,
		TO_CHAR(DATE_TRUNC(''month'', date_order), ''YYYY-MM-01'') AS month_qty,
		COALESCE(SUM(total_sales), 0) AS total_quantity
	FROM unified_sale_matview
    WHERE date_order BETWEEN '%(date_start)s' AND '%(date_end)s'
	GROUP BY product_id, month_qty
    ORDER BY product_id, month_qty',
	'SELECT DISTINCT TO_CHAR(DATE_TRUNC(''month'', date_order), ''YYYY-MM-01'') AS month_qty
     FROM unified_sale_matview
     WHERE date_order BETWEEN '%(date_start)s' AND '%(date_end)s'
     ORDER BY 1'
) AS pivot_table (
	product_id INTEGER,
	{month_sales}
);
""".format(month_qty=month_qty, month_sales=month_sales)
        
        self._cr.execute(query, {
            "date_start": str(self.date_start),
            "date_end": str(self.date_end),
        })

    def _processing_pivot(self, processing_categ):
        """
        Processing Pivot view to generate report in Odoo
        """
        query = """
SELECT qty.product_id, {processing_categ} FROM product_sale_pivot_qty qty
LEFT JOIN product_sale_pivot_amount sale ON qty.product_id = sale.product_id;
""".format(processing_categ=processing_categ)
        
        self._cr.execute(query)
        
        records = self._cr.dictfetchall()
        return records
    
    def generate_report(self):
        """
        Function to generate report (pivot & graph) from date filter
        """
        report_obj = self.env["unified.sale.report"]
        months = self._get_distinct_months()
        self._cr.execute("DELETE FROM unified_sale_report")

        if months:
            month_qty, month_sales, processing_categ = self._convert_months(months)
            self._create_pivot(month_qty, month_sales)
            records = self._processing_pivot(processing_categ)
            
            for rec in records:
                vals = {}
                for key, value in rec.items():
                    if key == "product_id":
                        vals["product_id"] = value
                    else:
                        date = key.replace("qty", "").replace("sales", "").replace("_", "-")
                        vals["date"] = date
                        if "qty" in key:
                            vals["product_qty"] = value or 0
                        elif "sales" in key:
                            vals["price_subtotal"] = value or 0
                            report_obj.create(vals)
        
        return {
            "name": _("Unified Sale Report"),
            "view_mode": "pivot,graph",
            "res_model": "unified.sale.report",
            "type": "ir.actions.act_window",
        }

