/** @odoo-module **/


import { Component , xml} from "@odoo/owl";
export class OrderStatsTile extends Component {}

OrderStatsTile.template = xml`
<div class="order-stats-container p-3">
    <div class="row text-center">
        <!-- Total Orders -->
        <div class="col-md-3 col-sm-6 mb-3">
            <div class="stat-item bg-info text-white p-4 border rounded shadow-lg">
                <h5>Total Vehicle</h5>
                <p class="h4"><t t-esc="props.total"/></p>
            </div>
        </div>
        
        <!-- Pending Orders -->
        <div class="col-md-3 col-sm-6 mb-3">
            <div class="stat-item bg-warning-light text-dark p-4 border rounded shadow-lg">
                <h5>Available Vehicle</h5>
                <p class="h4"><t t-esc="props.pending"/></p>
            </div>
        </div>
        
        <!-- Delivered Orders -->
        <div class="col-md-3 col-sm-6 mb-3">
            <div class="stat-item bg-success-light text-dark p-4 border rounded shadow-lg">
                <h5>Total Drivers</h5>
                <p class="h4"><t t-esc="props.delivered"/></p>
            </div>
        </div>
        
        <!-- Cancelled Orders -->
        <div class="col-md-3 col-sm-6 mb-3">
            <div class="stat-item bg-danger-light text-dark p-4 border rounded shadow-lg">
                <h5>Available Drivers</h5>
                <p class="h4"><t t-esc="props.cancelled"/></p>
            </div>
        </div>
    </div>
</div>
` 
