# -*- coding: utf-8 -*-

import json
from lxml import etree

from odoo import models, api


class DynamicFieldMixin(models.AbstractModel):
    _inherit = 'base'

    # =========================================================
    # DYNAMIC VIEW MODIFICATION
    # =========================================================

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):

        res = super().get_view(
            view_id=view_id,
            view_type=view_type,
            **options
        )

        # only form views
        if view_type != 'form':
            return res

        # safety
        if not res.get('arch'):
            return res

        try:
            doc = etree.XML(res['arch'])
        except Exception:
            return res

        configs = self.env[
            'dynamic.field.config'
        ].sudo().search([
            ('model_id.model', '=', self._name),
            ('active', '=', True)
        ])

        if not configs:
            return res

        existing_fields = self._fields.keys()

        # safe field metadata
        res_fields = res.get('fields', {})

        for config in configs:

            field_name = config.field_id.name

            if field_name not in existing_fields:
                continue

            nodes = doc.xpath(
                "//field[@name='%s']" % field_name
            )

            if not nodes:
                continue

            for node in nodes:

                modifiers = json.loads(
                    node.get("modifiers") or "{}"
                )

                # =====================================
                # READONLY
                # =====================================

                if config.readonly:

                    modifiers['readonly'] = True

                    node.set('readonly', '1')

                    if field_name in res_fields:
                        res_fields[field_name]['readonly'] = True

                # =====================================
                # REQUIRED
                # =====================================

                if config.required:

                    modifiers['required'] = True

                    node.set('required', '1')

                    if field_name in res_fields:
                        res_fields[field_name]['required'] = True

                # =====================================
                # INVISIBLE
                # =====================================

                if config.invisible:

                    modifiers['invisible'] = True

                    node.set('invisible', '1')

                # =====================================
                # UPDATE MODIFIERS
                # =====================================

                node.set(
                    'modifiers',
                    json.dumps(modifiers)
                )

        res['arch'] = etree.tostring(
            doc,
            encoding='unicode'
        )

        return res
    # =========================================================
    # DISABLE EXISTING ODOO TRACKING
    # =========================================================

    def _mail_track(self, tracked_fields, initial):

        configs = self.env[
            'dynamic.field.config'
        ].sudo().search([
            ('model_id.model', '=', self._name),
            ('active', '=', True)
        ])

        # fields where tracking disabled
        disabled_tracking_fields = configs.filtered(
            lambda x: not x.tracking
        ).mapped('field_id.name')

        # remove tracking dynamically
        for field_name in disabled_tracking_fields:
            tracked_fields.pop(field_name, None)

        return super()._mail_track(
            tracked_fields,
            initial
        )

    # =========================================================
    # ENABLE CUSTOM TRACKING FOR BINARY TYPE FIELD
    # =========================================================
    
    def write(self, vals):

        tracking_configs = self.env[
            'dynamic.field.config'
        ].sudo().search([
            ('model_id.model', '=', self._name),
            ('tracking', '=', True),
            ('active', '=', True)
        ])

        binary_fields = tracking_configs.filtered(
            lambda x: x.field_id.ttype == 'binary'
        ).mapped('field_id.name')

        old_values = {}

        for rec in self:

            old_values[rec.id] = {}

            for field_name in binary_fields:

                if field_name in vals:

                    old_values[rec.id][field_name] = bool(
                        rec[field_name]
                    )

        result = super().write(vals)

        for rec in self:

            messages = []

            for field_name in binary_fields:

                if field_name not in vals:
                    continue

                field_obj = rec._fields[field_name]

                old_has_value = old_values[
                    rec.id
                ].get(field_name)

                new_has_value = bool(
                    rec[field_name]
                )

                # =====================================
                # IMAGE ADDED
                # =====================================

                if not old_has_value and new_has_value:

                    messages.append(
                        f"Image Added ({field_obj.name})"
                    )

                # =====================================
                # IMAGE REMOVED
                # =====================================

                elif old_has_value and not new_has_value:

                    messages.append(
                        f"Image Removed ({field_obj.name})"
                    )

                # =====================================
                # IMAGE UPDATED
                # =====================================

                elif old_has_value and new_has_value:

                    messages.append(
                        f"Image Updated ({field_obj.name})"
                    )

            if (
                messages
                and hasattr(rec, 'message_post')
            ):

                rec.message_post(
                    body="\n".join(messages),
                    subtype_xmlid="mail.mt_note"
                )

        return result