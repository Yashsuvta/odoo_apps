from odoo import models, fields

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    custom_field = fields.Char()
    isdriver = fields.Boolean(string="Is Driver",default=False)
    status = fields.Boolean(string="status",default=False)