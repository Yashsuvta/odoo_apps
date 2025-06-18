{
    "name": "Advanced List View",
    "version": "17.0.1.0.0",
    "summary": """Odoo Advanced List View – Advanced List Filtering & Data Management
    Odoo Advanced List View is a powerful module that transforms the standard list view into a dynamic, user-friendly interface. With advanced filtering options directly from column headers, it enables seamless record management and real-time data control.""",
    "description": """Odoo Advanced List View – Advanced List Filtering & Data Management
    Odoo Advanced List View is a powerful module that transforms the standard list view into a dynamic, user-friendly interface. With advanced filtering options directly from column headers, it enables seamless record management and real-time data control.""",
    'author': "CodeFusion OdooWorks",
    'maintainers': ['yashsuvta1236@gmail.com, nitinupmanyu12@gmail.com'],
    'website': "https://codefusion-odooworks.odoo.com/",
    "depends": [
        "web",
        "account",
        "crm",
        "crm_iap_mine",
        "purchase"
    ],
    "data": [
            'data/export_paper_format.xml',
            'report/export_pdf_group_by_template.xml',
            'report/export_pdf_template.xml',
            'report/ir_exports_report.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "advanced_list_view/static/src/xml/dynamic_filter.xml",
            "advanced_list_view/static/src/css/dynamic_filters.css",
            "advanced_list_view/static/src/js/dynamic_filter.js",
            "advanced_list_view/static/src/js/copy_button.js",
            "advanced_list_view/static/src/js/pdf_export.js",
            "advanced_list_view/static/src/js/csv_export.js",
            "advanced_list_view/static/src/js/export_dialog.js",
            "advanced_list_view/static/src/xml/list_button_view.xml",
            "advanced_list_view/static/src/xml/export_dialog.xml",
            "advanced_list_view/static/src/xml/export_csv.xml",
            "advanced_list_view/static/src/xml/copy_button.xml",
            "advanced_list_view/static/src/xml/export_pdf_dropdown.xml",
        ]
    },
    "images": [
        "static/description/banner.png",
    ],
    "license": "OPL-1",
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 39.00,
    "currency": "USD",
}