# -*- coding: utf-8 -*-

{
    "name": "Contact Field Validation",
    "version": "17.0.1.0.0",
    "summary": "Frontend and backend validation for phone and email fields",
    "description": """
Contact Field Validation
========================

This module adds validation for phone and email fields in Odoo.

Features
--------
Phone Validation
~~~~~~~~~~~~~~~~
* Prevents alphabets and invalid characters in phone fields
* Allows only:
    - Digits (0-9)
    - Plus (+)
    - Minus (-)
    - Spaces
    - Parentheses ()
* Automatically cleans pasted values
* Works dynamically on notebook pages and lazy-loaded forms

Email Validation
~~~~~~~~~~~~~~~~
* Validates email format from backend
* Prevents saving invalid email addresses
* Example of valid email:
    - yash@example.com

Supported Phone Fields
----------------------
* phone
* mobile
* work_phone
* private_phone
* emergency_phone

Supported Models
----------------
* res.partner
* res.company
* hr.employee
* Any custom model using supported field names

Technical Details
-----------------
* Built using OWL patching
* Uses MutationObserver for dynamic DOM rendering
* Backend validation using Python constraints
* Compatible with Odoo 17 Web Framework

Company
-------
CodeFusion OdooWorks

Support
-------
Email: yashsuvta1236@gmail.com

License
-------
LGPL-3
    """,
    "author": "CodeFusion OdooWorks",
    "maintainer": "CodeFusion OdooWorks",
    "support": "yashsuvta1236@gmail.com",
    "website": "https://www.odoo.com",
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
    "price": 0,
    "currency": "USD",
}