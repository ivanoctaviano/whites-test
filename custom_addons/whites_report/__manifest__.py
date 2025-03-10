# -*- coding: utf-8 -*-
{
    "name" : "Whites Report",
    "version" : "1.0",
    "author": "Ivan Octaviano",
    "category": "Sales/Sales",
    "summary": "Unified Sales Report with SQL Pivot",
    "depends" : ["base", "point_of_sale", "sale", "sale_management"],
    "data": [
        "data/unified_sale_dataset.sql",
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
        "wizard/unified_sale_report.xml",
        "wizard/unified_sale_wizard.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}