from odoo import http
from odoo.http import request,json

class CarRentalApi(http.Controller):


    # Created the api to fetch data of all cars

    @http.route('/api/car_rentals', auth='public', methods=['GET'], type='http', csrf=False)
    def get_all_cars(self, **kwargs):
        cars = request.env['car.rental'].sudo().search([])
        car_data =  [{
            'id': car.id,
            'name': car.name,
            'rent': car.rent,
            'car_status': car.car_status,
            'car_type': car.car_type,
            'color': car.color,
            'model_year': car.model_year,
            'occupancy': car.occupancy
        } for car in cars]
    
        return request.make_response(json.dumps(car_data), headers=[('Content-Type', 'application/json')])
    
    # Created the api to fetch data of specific car 

    @http.route('/api/car_rentals/<int:car_id>', auth='public', methods=['GET'], type='http', csrf=False)
    def get_car(self, car_id):
        car = request.env['car.rental'].sudo().browse(car_id)
        if not car.exists():
            return {'error': 'Car not found'}
        car_data=  {
            'id': car.id,
            'name': car.name,
            'rent': car.rent,
            'car_status': car.car_status,
            'car_type': car.car_type,
            'color': car.color,
            'model_year': car.model_year,
            'occupancy': car.occupancy
        }
        return request.make_response(json.dumps(car_data), headers=[('Content-Type', 'application/json')])
    
    # Created the api to create the new car 
    
    @http.route('/api/car_rentals', auth='public', methods=['POST'], type='http', csrf=False)
    def create_car(self, **kwargs):
        try:
            # Parse JSON body from request
            data = json.loads(request.httprequest.data)

            # Create the car
            car = request.env['car.rental'].sudo().create({
                'name': data.get('name'),
                'last_odometer': data.get('last_odometer'),
                'rent': data.get('rent'),
                'color': data.get('color'),
                'model_year': data.get('model_year'),
                'car_status': data.get('car_status', 'available'),
                'car_type': data.get('car_type'),
                'occupancy': data.get('occupancy'),
                # Add other fields as needed...
            })

            return request.make_response(json.dumps({
                'success': True,
                'id': car.id
            }), headers=[('Content-Type', 'application/json')])

        except Exception as e:
            return request.make_response(json.dumps({
                'success': False,
                'error': str(e)
            }), headers=[('Content-Type', 'application/json')])

    @http.route('/api/car_rentals/<int:car_id>', auth='public', methods=['PUT'], type='http', csrf=False)
    def update_car(self, car_id, **kwargs):
        data = json.loads(request.httprequest.data)
        car = request.env['car.rental'].sudo().browse(car_id)
        if not car.exists():
            return {'error': 'Car not found'}
        car.write(data)
        return request.make_response(json.dumps({
                'success': True,
                'id': car.id
            }), headers=[('Content-Type', 'application/json')])
    

    # Created the API to delete a specific car by ID
    @http.route('/api/car_rentals/<int:car_id>', auth='public', methods=['DELETE'], type='http', csrf=False)
    def delete_car(self, car_id, **kwargs):
        car = request.env['car.rental'].sudo().browse(car_id)
        if not car.exists():
            return request.make_response(json.dumps({
                'success': False,
                'error': 'Car not found'
            }), headers=[('Content-Type', 'application/json')], status=404)

        car.unlink()
        return request.make_response(json.dumps({
            'success': True,
            'message': f'Car with ID {car_id} has been deleted.'
        }), headers=[('Content-Type', 'application/json')])

    
    


    