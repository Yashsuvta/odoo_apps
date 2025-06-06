from odoo import models, fields, api
class AccountMove(models.Model):
    _inherit = 'account.move'

    car_rental_contract_id = fields.Many2one('vehicle.rental.contract', string="vehicle Rental Contract")
