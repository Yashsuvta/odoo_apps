{
    "name": "Project Task Timer",
    "version": "19.0",
    'summary': """This module allows users to start and stop tasks seamlessly, automatically logging timesheets. It enhances workflow efficiency by ensuring accurate time tracking without manual entries.""",
    'description': """Users can initiate and stop timers for tasks, with timesheets logged automatically upon task completion. Additionally, the module enables users to stop timers directly from the navbar, ensuring quick access and precise timesheet recording. Ideal for improving productivity and time management within Odoo.""",
    'author': "CodeFusion OdooWorks",
    'maintainers': ['yashsuvta1236@gmail.com, nitinupmanyu12@gmail.com'],
    'website': "https://codefusion-odooworks.odoo.com/",
    'license': "AGPL-3",
    "depends":['web','project','hr_timesheet'],
    "category": "Project Management",
    "data": [ 
        "security/ir.model.access.csv",
        "views/project_task.xml"
    ],
   'assets': {
        'web.assets_backend': [
            'project_timer/static/src/js/timer.js',
            'project_timer/static/src/js/navbar.js',
            'project_timer/static/src/xml/navbar.xml',
        ],
    },
    "installable": True,
    "application": False, 
    "auto_install": False,
    "price": 15.00,
    "currency": "USD",
    'images': ['static/description/banner.png'],
}
