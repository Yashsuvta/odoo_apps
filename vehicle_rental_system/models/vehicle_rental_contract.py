from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CarRentalContract(models.Model):
    _name = "vehicle.rental.contract"
    _description = "vehicle Rental Contract"
    _inherit = 'mail.thread'

    customer = fields.Many2one('res.partner', string="Customer", required=True ,domain=[("isdriver", "=", False)])
    vehicle_ids = fields.Many2one('vehicle.rental', string="Vehicles", required=True, domain=[('car_status', '=', 'available')])
    car_rental_lines = fields.One2many('vehicle.rental.line', 'contract_id')
    deposit = fields.Float(string="Deposit")
    driver = fields.Many2one('res.partner', string="Driver", domain=[("isdriver", "=", True),("status", "=", False)])
    address = fields.Char(string="Pick/Drop Address")
    pickup_date = fields.Date(string="Pickup Date", required=True)
    drop_date = fields.Date(string="Drop Date", required=True)
    total_days = fields.Integer(string="Total Days", compute="_compute_total_days", store=True)
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('send contract','Send Contract'),
        ('confirmation', 'Confirmation'),
        ('done', 'Done'),
    ], string="Status", default='draft', tracking=True)

    remaining_amount = fields.Float(string="Remaining Amount", compute="_compute_remaining_amount", store=True)

    invoice_ids = fields.One2many('account.move', 'car_rental_contract_id', string="Invoices")
    invoice_count = fields.Integer(string="Invoice Count", compute="_compute_invoice_count")
    
    @api.depends('total_amount', 'deposit')
    def _compute_remaining_amount(self):
        for record in self:
            if record.total_amount >= record.deposit:
                record.remaining_amount = record.total_amount - record.deposit
            else:
                raise ValidationError("Deposit amount cannot be greater than the Total Amount.")



    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def _send_rental_email(self, subject, body):
        """Helper function to send formatted rental emails."""
        email_to = self.customer.email or ''
        email_cc = self.driver.email if self.driver and self.driver.email else ''

        mail_values = {
            'subject': subject,
            'body_html': f"""
                <p>Dear {self.customer.name},</p>
                {body}
                <p>Thank you,<br/>{self.env.user.name}</p>
            """,
            'email_to': email_to,
            'model': self._name,
            'res_id': self.id,
        }

        email = self.env['mail.mail'].create(mail_values)
        if email:
            email.send()

    def action_send_contract(self):
        self.state = 'send contract'
    
        vehicle_name = self.car_rental_lines[0].vehicle_id.name if self.car_rental_lines else 'N/A'

        total_amount = self.total_amount  
        Deposite_amount = self.deposit
        remaining_amount = self.remaining_amount

        subject = f"Confirmation Required: vehicle Rental Booking for {vehicle_name}"

        body = f"""
            <p>Thank you for choosing our vehicle rental service. Your rental request has been processed and is currently awaiting your confirmation.</p>

            <p><strong>Rental Summary:</strong></p>
            <ul>
                <li><strong>Vehicle:</strong> {vehicle_name}</li>
                <li><strong>Pickup Date:</strong> {self.pickup_date.strftime('%Y-%m-%d')}</li>
                <li><strong>Drop Date:</strong> {self.drop_date.strftime('%Y-%m-%d')}</li>
                <li><strong>Total Days:</strong> {self.total_days}</li>
                <li><strong>Total Amount:</strong> ${total_amount:.2f}</li>
                <li><strong>Deposite_amount:</strong> ${Deposite_amount:.2f}</li>
                <li><strong>remaining_amount:</strong> ${remaining_amount:.2f}</li>
                <li><strong>Pickup/Drop Address:</strong> {self.address or 'Not Provided'}</li>
            </ul>

            <p>Please confirm your booking by replying to this email or contacting us directly. Once confirmed, we will proceed with final arrangements and provide additional details.</p>

            <p>We look forward to serving you!</p>
        """

        self._send_rental_email(subject, body)


    def action_process(self):
        """Move contract from Draft to send contract and send confirmation email to customer."""
        self.state = 'confirmation'

        if  self.driver:
            self.driver.status = True

        if self.vehicle_ids:
            self.vehicle_ids.car_status = 'rented'
        
        driver_name = self.driver.name if self.driver else 'Not Assigned'
        driver_email = self.driver.email if self.driver and self.driver.email else 'N/A'
        driver_phone = self.driver.phone if self.driver and self.driver.phone else 'N/A'
        vehicle_name = self.car_rental_lines[0].vehicle_id.name if self.car_rental_lines else 'N/A'

        subject = f"Rental Completed: {vehicle_name}"

        body = f"""
            <p>Your vehicle rental has been confirmed successfully. Please find the details of driver and other information given below!</p>
            <p><strong>Rental Summary:</strong></p>
            <ul>
                <li><strong>Vehicle:</strong> {vehicle_name}</li>
                <li><strong>Pickup Date:</strong> {self.pickup_date.strftime('%Y-%m-%d')}</li>
                <li><strong>Drop Date:</strong> {self.drop_date.strftime('%Y-%m-%d')}</li>
                <li><strong>Total Days:</strong> {self.total_days}</li>
                <li><strong>Pickup/Drop Address:</strong> {self.address or 'Not Provided'}</li>
            </ul>
            <p><strong>Driver Details:</strong></p>
            <ul>
                <li><strong>Name:</strong> {driver_name}</li>
                <li><strong>Email:</strong> {driver_email}</li>
                <li><strong>Phone:</strong> {driver_phone}</li>
            </ul>
            <p><strong>Billing:</strong></p>
            <ul>
                <li><strong>Total Amount:</strong> ${self.total_amount:.2f}</li>
                <li><strong>Deposit Paid:</strong> ${self.deposit:.2f}</li>
            </ul>
            <p>Thank you for choosing our service!</p>
        """

        self._send_rental_email(subject, body)

        customer_name = self.customer.name
        customer_email = self.customer.email or 'N/A'
        customer_phone = self.customer.phone or 'N/A'

        if driver_email:
            subject_driver = f"Rental Contract Assign: {vehicle_name}"
            body_driver = f"""
                <p>You have been assigned a new vehicle rental booking. Please find the customer and rental details below:</p>

                <p><strong>Customer Info:</strong></p>
                <ul>
                    <li><strong>Name:</strong> {customer_name}</li>
                    <li><strong>Email:</strong> {customer_email}</li>
                    <li><strong>Phone:</strong> {customer_phone}</li>
                </ul>

                <p><strong>Rental Info:</strong></p>
                <ul>
                    <li><strong>Vehicle:</strong> {vehicle_name}</li>
                    <li><strong>Pickup Date:</strong> {self.pickup_date.strftime('%Y-%m-%d')}</li>
                    <li><strong>Drop Date:</strong> {self.drop_date.strftime('%Y-%m-%d')}</li>
                    <li><strong>Total Days:</strong> {self.total_days}</li>
                    <li><strong>Pickup/Drop Address:</strong> {self.address or 'Not Provided'}</li>
                </ul>

                <p><strong>Billing:</strong></p>
                <ul>
                    <li><strong>Total Amount:</strong> ${self.total_amount:.2f}</li>
                    <li><strong>Deposit Paid:</strong> ${self.deposit:.2f}</li>
                </ul>

                <p>Please prepare accordingly and reach out to the customer if needed.</p>
            """
        mail_values = {
            'subject': subject_driver,
            'body_html': f"""
                <p>Dear {driver_name},</p>
                {body_driver}
                <p>Thank you,<br/>{self.env.user.name}</p>
            """,
            'email_to': driver_email,
            'model': self._name,
            'res_id': self.id,
        }

        driver_email_obj = self.env['mail.mail'].create(mail_values)
        if driver_email_obj:
            driver_email_obj.send()



    def action_done(self):
        """Move contract from Process to Done and send completion email."""
        self.state = 'done'

        if self.driver:
            self.driver.status = False

        if self.vehicle_ids:
            self.vehicle_ids.car_status = 'available'


        for line in self.car_rental_lines:
            if line.vehicle_id and line.vehicle_id.car_status != 'available':
                line.vehicle_id.car_status = 'available'

        vehicle_name = self.car_rental_lines[0].vehicle_id.name if self.car_rental_lines else 'N/A'

        subject = f"Rental Completed: {vehicle_name}"

        body = f"""

            <p>We are pleased to inform you that your vehicle rental experience with us has been successfully completed.</p>
            <p><strong>We’d love your feedback!</strong></p>
            <p>Your opinion helps us improve our service. Please take a moment to let us know how your experience was.</p>

            <p><a href="https://example.com/feedback-form" target="_blank" style="padding:10px 15px;background:#2A9D8F;color:white;border-radius:5px;text-decoration:none;">Leave Feedback</a></p>

            <p>Thank you for choosing our service. We hope to see you again soon!</p>
        """

        self._send_rental_email(subject, body)


    @api.depends('pickup_date', 'drop_date')
    def _compute_total_days(self):
        for record in self:
            if record.pickup_date and record.drop_date:
                if record.drop_date < record.pickup_date:
                    raise ValidationError("Drop Date cannot be earlier than Pickup Date.")
                record.total_days = max(1, (record.drop_date - record.pickup_date).days)
            else:
                record.total_days = 0

    @api.onchange('vehicle_ids')
    def _onchange_vehicle_ids(self):
        self.car_rental_lines = [(5, 0, 0)]
        rental_lines = []
        for vehicle in self.vehicle_ids:
            rental_lines.append((0, 0, {
                'vehicle_id': vehicle.id,
                'last_reading': vehicle.last_odometer,
                'rent_price': vehicle.rent_price,   
            }))
        self.car_rental_lines = rental_lines

    @api.depends('car_rental_lines.total_amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.car_rental_lines.mapped('total_amount'))


    def action_view_invoices(self):
        self.ensure_one()
        if not self.invoice_ids:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.customer.id,
                'invoice_date': fields.Date.today(),
                'car_rental_contract_id': self.id,
                'invoice_line_ids': [(0, 0, {
                    'name': f'vehicle Rental for {self.total_days} days',
                    'quantity': 1,
                    'price_unit': self.total_amount,
                    'tax_ids': [(6, 0, [])],
                })],
            })
            self.invoice_ids = [(4, invoice.id)]
            return invoice
        return self.invoice_ids[0]
