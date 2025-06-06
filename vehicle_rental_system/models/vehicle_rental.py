from odoo import models, fields,api

class Vehicle(models.Model):
    _name = 'vehicle.rental'
    _description = 'vehicle Rental'
    _inherit = 'mail.thread'

    name = fields.Char(string='vehicle Name', required=True)
    image = fields.Image()
    last_odometer = fields.Float(string='Last Odometer')
    rent_uom_id = fields.Many2one(
    'uom.uom', 
    string='Rent Unit of Measure', 
    domain="[('category_id.name', '=', 'Time')]",
    required=True
    )
    rent_price = fields.Float(string='Rent Price', required=True)
    immatriculation_date = fields.Date(string='Immatriculation Date')
    chassis_number = fields.Char(string='Chassis Number')
    catalog_value = fields.Float(string='Catalog Value (VAT)')
    purchase_value = fields.Float(string='Purchase Value')
    residual_value = fields.Float(string='Residual Value')
    seat_number = fields.Integer(string='Seat Number')
    door_number = fields.Integer(string='Door Number')
    fuel_level = fields.Float(string="Fuel Level")
    color = fields.Char(string='Color')
    model_year = fields.Integer(string='Model Year')
    car_status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
        ('sold', 'Sold')
    ], string='vehicle Status', default='available')
    car_type = fields.Selection([
        ('sedan', 'Sedan'),
        ('hatchback', 'Hatchback'),
        ('suv', 'SUV'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('wagon', 'Wagon'),
        ('pickup', 'Pickup')
    ], string='vehicle Type')
    used_for = fields.Char(string='Used For')
    occupancy = fields.Integer(string='Occupancy')

    def set_status_rented(self):
        for rec in self:
            if rec.car_status != 'rented':
                rec.car_status = 'rented'

    def set_status_sold(self):
        for rec in self:
            if rec.car_status != 'sold':
                rec.car_status = 'sold'

    def set_status_maintenance(self):
        for rec in self:
            if rec.car_status != 'maintenance':
                rec.car_status = 'maintenance'

    def set_status_available(self):
        for rec in self:
            if rec.car_status !='available':
                rec.car_status = 'available'


    def get_dashboard_data(self):
        CarRental = self.env['vehicle.rental']
        Partner = self.env['res.partner']
        Contract = self.env['vehicle.rental.contract']

        # Vehicles
        total_cars = CarRental.search_count([])
        available_cars = CarRental.search_count([('car_status', '=', 'available')])

        # Drivers
        total_drivers = Partner.search_count([('isdriver', '=', True)])
        engaged_drivers = Partner.search_count([('isdriver', '=', True), ('status', '=', True)])
        available_drivers = Partner.search_count([('isdriver', '=', True), ('status', '=', False)])

        # Customers
        total_customers = Partner.search_count([('isdriver', '=', False)])

        # Contracts by state
        contract_states = ['draft', 'send contract', 'confirmation', 'done']
        contract_state_counts = {
            state: Contract.search_count([('state', '=', state)]) for state in contract_states
        }

        return {
            'total_cars': total_cars,
            'available_cars': available_cars,
            'total_drivers': total_drivers,
            'engaged_drivers': engaged_drivers,
            'available_drivers': available_drivers,
            'total_customers': total_customers,
            'contract_state_counts': contract_state_counts,
        }
