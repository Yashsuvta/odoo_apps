from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    always_debug_mode = fields.Boolean(string='Always Enable Debug Mode')

    def has_always_debug_mode(self, uid):
        user = self.sudo().browse(uid)
        return user.always_debug_mode


