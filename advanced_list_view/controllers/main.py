from odoo import http
from odoo.http import request
import re

class ExportData(http.Controller):
    @http.route('/get_data', auth="user", type='json')
    def get_export_data(self, **kw):
        """
        controller to fetch required details
        """
        fields = kw['fields']
        model = kw['model']
        Model = request.env[model]
        field_names = [f['name'] for f in fields]
        columns_headers = [val['label'].strip() for val in fields]
        domain = [('id', 'in', kw['res_ids'])] \
            if kw['res_ids'] else kw['domain']
        groupby = kw['grouped_by']
        records = Model.browse(kw['res_ids']) \
            if kw['res_ids'] \
            else Model.search(domain, offset=0, limit=False, order=False)
        if groupby:
            field_names = [f['name'] for f in fields]
            groupby_type = [Model._fields[x.split(':')[0]].type for x in
                            kw['grouped_by']]
            domain = kw['domain']
            groups_data = Model.read_group(domain,
                                           [x if x != '.id' else 'id' for x in
                                            field_names], groupby, lazy=False)
            group_by = []
            for rec in groups_data:
                ids = Model.search(rec['__domain'])
                list_key = [x for x in rec.keys() if
                            x in field_names and x not in kw['grouped_by']]
                export_data = [ids.export_data(field_names).get('datas', [])]
                group_tuple = (
                    {'count': rec['__count']}, rec.get(kw['grouped_by'][0]),
                    export_data,
                    [(rec[x], field_names.index(x)) for x in list_key])
                group_by.append(group_tuple)
            return {'header': columns_headers, 'data': export_data,
                    'type': groupby_type, 'other': group_by}
        else:
            export_data = records.export_data(field_names).get('datas', [])
            pdf_report = request.env.ref('advanced_list_view.ir_exports_pdf_report')
            if pdf_report:
                pdf_report.name = Model._description
            return {'data': export_data,'filename':Model._description, 'header': columns_headers}



    @http.route('/create_search_view', type='json', auth='user')
    def create_search_view(self, extra_elements, model):
        resmodel = str(model)
        search_view = request.env['ir.ui.view'].search([('type','=', 'search'),('model','=', resmodel),('mode','=', 'primary')])
        if search_view:
            original_string = search_view[0].arch
            if len(extra_elements) > 1:
                for element in extra_elements:
                    new_line = f'<filter string="{element.upper()}" name="filter_{element}_date" date="{element}"/>\n'
                    original_string = re.sub(r'</search>', f'{new_line}</search>', original_string)
                    # Break out of the loop after processing one element
                    if original_string:
                        search_view[0].arch =  original_string
                    break
            else:
                new_line = f'<filter string="{extra_elements[0].upper()}" name="filter_{extra_elements[0]}_date" date="{extra_elements[0]}"/>\n'
                original_string = re.sub(r'</search>', f'{new_line}</search>', original_string)
                if original_string:
                    search_view[0].arch =  original_string
        else:
            resmodel = resmodel.replace('_', '.')
            model = request.env['ir.model'].search([('model','=', resmodel)])
            filters = '\n'.join([f'\t<filter string="{element.upper()}" name="filter_{element}_date" date="{element}"/>' for element in extra_elements])
            new_view_arch = f'<search>\n{filters}\n</search>'
            new_record_values = {
                'name': f'{resmodel}.search.view',
                'type': 'search',
                'model_id': model.id,
                'mode': 'primary',
                'active': True,
                'priority': 16,
                'arch_base': new_view_arch
            }
            new_record = request.env['ir.ui.view'].create(new_record_values)