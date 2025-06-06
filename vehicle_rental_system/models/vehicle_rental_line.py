from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round


class CarRentalLine(models.Model):
    _name = 'vehicle.rental.line'
    _description = 'vehicle Rental Line'

    contract_id = fields.Many2one('vehicle.rental.contract',readonly=True)
    vehicle_id = fields.Many2one('vehicle.rental', string="Vehicle",readonly=True)
    last_reading = fields.Float(string="Last Odometer", store=True,readonly=True)
    current_reading = fields.Float(string="Current Odometer")
    payable_reading = fields.Float(string="Payable Reading", compute="_compute_payable_reading", store=True)
    rent_uom = fields.Char(
    string='UOM', 
    required=True,
    compute="_compute_rent_uom_id"
    )
    rent_price = fields.Float(string='Rent Price')
    duration = fields.Float(string="Duration", compute="_compute_duration", store=True)
    tax = fields.Float(string="Tax")
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)

    @api.depends('contract_id.pickup_date', 'contract_id.drop_date', 'vehicle_id.rent_uom_id')
    def _compute_duration(self):
        for line in self:
            contract = line.contract_id
            vehicle = line.vehicle_id
            if contract.pickup_date and contract.drop_date and vehicle and vehicle.rent_uom_id:
                delta = (contract.drop_date - contract.pickup_date).days
                duration = delta
                time_unit = vehicle.rent_uom_id.name.lower()
                if 'hour' in time_unit:
                    duration = delta * 24
                elif 'week' in time_unit:
                    duration = delta / 7
                elif 'month' in time_unit:
                    duration = delta / 30
                # default: assume day
                line.duration = float_round(duration, precision_digits=2)
            else:
                line.duration = 0

    def _compute_rent_uom_id(self   ):
        self.rent_uom = self.vehicle_id.rent_uom_id.name

    @api.depends('current_reading')
    def _compute_payable_reading(self):
        """Calculate payable reading as the difference between current and last odometer."""
        for record in self:
            record.payable_reading = max(0, record.current_reading - record.last_reading)


    @api.depends('contract_id.car_rental_lines.payable_reading', 'contract_id.car_rental_lines.rent_price', 'contract_id.car_rental_lines.tax')
    def _compute_total_amount(self):
        """Compute total amount considering multiple cars in the contract."""
        for record in self:
            if record.contract_id:
                total_rent = sum(line.payable_reading * (line.rent_price + line.tax) for line in record.contract_id.car_rental_lines)
                record.total_amount = total_rent
            else:
                record.total_amount = record.payable_reading * (record.rent_price + record.tax)
    @api.model
    def create(self, vals):
        record = super(CarRentalLine, self).create(vals)
        if record.last_reading == 0.0:
            rental_record = self.env['vehicle.rental'].search([('id', '=', record.contract_id.vehicle_ids.id)], limit=1) 
            last_reading  =   rental_record.last_odometer
            rent_price = rental_record.rent_price
            record.last_reading = last_reading
            record.rent_price = rent_price
            record.vehicle_id = rental_record.id
        return record
