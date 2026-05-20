# -*- coding: utf-8 -*-

{
    "name": "Contact Field Validation",
    "version": "17.0.1.0.0",
    "summary": "Frontend and backend validation for phone and email fields",
    "description": """
Frontend and backend validation for phone and email fields.
    """,
    "author": "CodeFusion OdooWorks",
    "maintainer": "CodeFusion OdooWorks",
    "support": "yashsuvta1236@gmail.com",
    "website": "https://codefusion-odooworks.odoo.com",
    "category": "Tools",
    "license": "LGPL-3",
    "depends": [
        "web",
        "contacts",
        "hr",
    ],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "contact_field_validation/static/src/js/form_renderer_patch.js",
        ],
    },
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
