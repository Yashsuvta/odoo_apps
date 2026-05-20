from odoo import models, api, _
from odoo.exceptions import ValidationError

import re


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("email")
    def _check_valid_email(self):

        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        for rec in self:

            if rec.email:

                email = rec.email.strip()

                if not re.match(email_regex, email):

                    raise ValidationError(
                        _(
                            "Please enter a valid email address.\n"
                            "Example: test@example.com"
                        )
                    )
                    
class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.constrains("private_email, work_email")
    def _check_valid_email(self):

        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        for rec in self:

            if rec.email:

                email = rec.email.strip()

                if not re.match(email_regex, email):

                    raise ValidationError(
                        _(
                            "Please enter a valid email address.\n"
                            "Example: test@example.com"
                        )
                    )
                    
class Rescompany(models.Model):
    _inherit = "res.company"

    @api.constrains("email")
    def _check_valid_email(self):

        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        for rec in self:

            if rec.email:

                email = rec.email.strip()

                if not re.match(email_regex, email):

                    raise ValidationError(
                        _(
                            "Please enter a valid email address.\n"
                            "Example: test@example.com"
                        )
                    )