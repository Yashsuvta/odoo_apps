# -*- coding: utf-8 -*-

from odoo import models, fields , api


class DynamicFieldConfig(models.Model):
    _name = 'dynamic.field.config'
    _description = 'Dynamic Field Configuration'
    _rec_name = 'field_id'

    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade'
    )

    field_id = fields.Many2one(
        'ir.model.fields',
        string='Field',
        required=True,
        domain="[('model_id', '=', model_id)]",
        ondelete='cascade'
    )

    readonly = fields.Boolean()

    required = fields.Boolean()

    invisible = fields.Boolean()

    tracking = fields.Boolean(
        string='Enable Tracking'
    )

    active = fields.Boolean(
        default=True
    )
    
    # =====================================================
    # AUTO LOAD FIELD CONFIGURATION
    # =====================================================

    @api.onchange('field_id')
    def _onchange_field_id(self):

        for rec in self:

            field = rec.field_id

            if not field:
                continue

            # =========================================
            # REQUIRED
            # =========================================

            rec.required = field.required

            # =========================================
            # READONLY
            # =========================================

            try:
                model = self.env[field.model]

                field_obj = model._fields.get(
                    field.name
                )

                if field_obj:

                    rec.readonly = bool(
                        getattr(
                            field_obj,
                            'readonly',
                            False
                        )
                    )

                    rec.tracking = bool(
                        getattr(
                            field_obj,
                            'tracking',
                            False
                        )
                    )

            except Exception:
                pass

            # invisible cannot be detected reliably
            rec.invisible = False