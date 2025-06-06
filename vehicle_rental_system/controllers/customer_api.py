from odoo import http
from odoo.http import request,json

class CustomerApi(http.Controller):

    @http.route('/api/customers', auth='public', methods=['GET'], type='http', csrf=False)
    def get_all_customers(self, **kwargs):
        customers = request.env['res.partner'].sudo().search([('isdriver', '=', False)])  # Ensure the partner is a customer
        customer_data = [{
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'company': customer.company_name,
            'address': customer.contact_address,
            'customer_type': customer.customer_rank,
            'status': customer.active and 'Active' or 'Inactive'
        } for customer in customers]

        return request.make_response(json.dumps(customer_data), headers=[('Content-Type', 'application/json')])
    

    @http.route('/api/customers/<int:customer_id>', auth='public', methods=['GET'], type='http', csrf=False)
    def get_customer(self, customer_id):
        customer = request.env['res.partner'].sudo().browse(customer_id)
        if customer.isdriver == False:
            if not customer.exists():
                return request.make_response(json.dumps({
                    'error': 'Customer not found'
                }), headers=[('Content-Type', 'application/json')], status=404)
            
            customer_data = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'company': customer.company_name,
                'address': customer.contact_address,
                'customer_type': customer.customer_rank,
                'status': customer.active and 'Active' or 'Inactive'
            }
            return request.make_response(json.dumps(customer_data), headers=[('Content-Type', 'application/json')])
        else:
                # If customer is a driver, just return an empty JSON or a specific message
            return request.make_response(json.dumps({
                'message': 'Customer is a driver, no data available'
            }), headers=[('Content-Type', 'application/json')])

        
    @http.route('/api/customers', auth='public', methods=['POST'], type='http', csrf=False)
    def create_customer(self, **kwargs):
        try:
            # Parse JSON body from request
            data = json.loads(request.httprequest.data)

            # Create the customer
            customer = request.env['res.partner'].sudo().create({
                'name': data.get('name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'company_name': data.get('company'),
                'contact_address': data.get('address'),
                'customer_rank': data.get('customer_type', 1),  # Default to customer type "1"
                'active': data.get('active', True)  # Default to Active customer
            })

            return request.make_response(json.dumps({
                'success': True,
                'id': customer.id
            }), headers=[('Content-Type', 'application/json')])

        except Exception as e:
            return request.make_response(json.dumps({
                'success': False,
                'error': str(e)
            }), headers=[('Content-Type', 'application/json')])

    @http.route('/api/customers/<int:customer_id>', auth='public', methods=['PUT'], type='http', csrf=False)
    def update_customer(self, customer_id, **kwargs):
        data = json.loads(request.httprequest.data)
        customer = request.env['res.partner'].sudo().browse(customer_id)
        if customer.isdriver == False:
            if not customer.exists():
                return request.make_response(json.dumps({
                    'error': 'Customer not found'
                }), headers=[('Content-Type', 'application/json')], status=404)

            customer.write({
                'name': data.get('name', customer.name),
                'email': data.get('email', customer.email),
                'phone': data.get('phone', customer.phone),
                'company_name': data.get('company', customer.company_name),
                'contact_address': data.get('address', customer.contact_address),
                'customer_rank': data.get('customer_type', customer.customer_rank),
                'active': data.get('active', customer.active)
            })

            return request.make_response(json.dumps({
                'success': True,
                'id': customer.id
            }), headers=[('Content-Type', 'application/json')])
        else:
            return request.make_response(json.dumps({
                'message': 'Customer is a driver, no data available'
            }), headers=[('Content-Type', 'application/json')])
    

    @http.route('/api/customers/<int:customer_id>', auth='public', methods=['DELETE'], type='http', csrf=False)
    def delete_customer(self, customer_id, **kwargs):
        customer = request.env['res.partner'].sudo().browse(customer_id)
        if customer.isdriver == False:
            if not customer.exists():
                return request.make_response(json.dumps({
                    'success': False,
                    'error': 'Customer not found'
                }), headers=[('Content-Type', 'application/json')], status=404)

            customer.unlink()  # Soft delete the customer
            return request.make_response(json.dumps({
                'success': True,
                'message': f'Customer with ID {customer_id} has been deleted.'
            }), headers=[('Content-Type', 'application/json')])
        
        else:
            return request.make_response(json.dumps({
                'message': 'Customer is a driver, no Customer not deleted'
            }), headers=[('Content-Type', 'application/json')])




