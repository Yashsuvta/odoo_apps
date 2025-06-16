{
    'name': "Toggle Developer Mode",
    'version': '18.0',
    'category': 'Tools',
    'author': "CodeFusion OdooWorks",
    'maintainers': ['yashsuvta1236@gmail.com, nitinupmanyu12@gmail.com'],
    'website': "https://codefusion-odooworks.odoo.com/",
    'license': "AGPL-3",
    'summary': """
        Effortlessly toggle Odoo debug mode directly from the top-right Navbar. Simplify development and troubleshooting with a single click.""",
    'description': """
        This module streamlines Odoo debugging, allowing users to enable or disable debug mode instantly from any view across all devices. Say goodbye to tedious steps—enhance your workflow with a seamless, integrated debug toggle option!
    """,
    'depends': [
        'base', 
        'web',
    ],
    'assets': {
        'web.assets_backend': [
            'toggle_developer_mode/static/src/css/app.css',
            'toggle_developer_mode/static/src/js/custom.js',
            'toggle_developer_mode/static/src/xml/base.xml',
        ],
    },
    'images': ["static/description/banner.png"],
    'installable': True,
    'application': True,
}
