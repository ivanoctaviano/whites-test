# -*- coding: utf-8 -*-
{
    "name" : "Whites PoS",
    "version" : "1.0",
    "author": "Ivan Octaviano",
    "category": "Sales/Point of Sale",
    "summary": "PoS Refund Authorization",
    "depends" : ["web", "base", "hr", "point_of_sale"],
    "data": [
        "views/hr_employee.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "whites_pos/static/src/js/refund_password.js"
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}