================================================================
Vehicle Rental System (Odoo 19)
================================================================

The **Vehicle Rental System** is a custom Odoo 19 module designed to efficiently manage end-to-end vehicle rental operations. It enables businesses to handle rental contracts, assign vehicles and drivers, track rental durations, generate invoices, and automate communication throughout the rental lifecycle.

This module is fully integrated with Odoo’s core applications such as Accounting and CRM, ensuring a seamless workflow and improved operational efficiency.

.. role:: raw-html(raw)
   :format: html

**Table of Contents**

.. contents::
   :local:

Installation
================================================================

To install this module, follow these steps:

* Copy the module folder into your Odoo `addons` directory.
* Restart the Odoo server.
* Navigate to **Apps**.
* Click on **Update Apps List**.
* Search for **Vehicle Rental System**.
* Click **Install**.

Usage
================================================================

Create a Vehicle Rental Contract
------------------------------------------------

* Go to the **Vehicle Rental** menu.
* Click on **Create**.
* Enter customer details, rental duration, and select a vehicle.
* Save the contract in Draft state.

Screenshot:

.. image:: vehicle_rental_system/static/description/rental_contract_draft.png
   :alt: Rental Contract Form
   :width: 300px

Assign Drivers
------------------------------------------------

* Drivers are assigned during the **Processing** stage.
* The system ensures only available drivers can be selected.
* Prevents driver double-booking automatically.

Screenshot:

.. image:: vehicle_rental_system/static/description/rental_contract_confirmation.png
   :alt: Assign Driver
   :width: 300px

Rental Lifecycle
------------------------------------------------

The rental contract flows through the following stages:

* Draft
* Processing
* Confirmed
* Done
* Cancelled

Each stage includes validations and triggers automated email notifications.

Screenshot:

.. image:: vehicle_rental_system/static/description/rental_contract_confirmation.png
   :alt: Contract Stages
   :width: 300px

Vehicle Availability
------------------------------------------------

* Vehicles are automatically marked as:
  - Available
  - Rented
* The system prevents double-booking of vehicles.
* Availability updates dynamically based on active contracts.

Screenshot:

.. image:: vehicle_rental_system/static/description/vehicle.png
   :alt: Vehicle Status
   :width: 300px

Driver Status Management
------------------------------------------------

* Drivers are categorized as:
  - Available
  - Engaged
* Status updates automatically based on assigned contracts.
* Ensures efficient driver allocation without conflicts.

Screenshot:

.. image:: vehicle_rental_system/static/description/Drivers_status.png
   :alt: Driver Status
   :width: 300px

Reporting & Dashboard
------------------------------------------------

* Access detailed reports on:
  - Vehicle utilization
  - Rental performance
  - Customer rental history
* Interactive dashboard for quick insights and decision-making.

Screenshot:

.. image:: vehicle_rental_system/static/description/vehicle_rental_dashboard_view.png
   :alt: Rental Dashboard
   :width: 300px

Key Features
================================================================

* Rental contract lifecycle management
* Vehicle and driver allocation
* Automatic availability tracking
* Invoice generation with Accounting integration
* Email notifications for contract stages
* Reporting and dashboard insights
* Prevention of double-booking

Changelog
================================================================

19.0.1.0.0
*****************

* ``Improved`` Compatibility with Odoo 19.
* ``Enhanced`` User interface and workflow experience.
* ``Optimized`` Rental contract lifecycle handling.
* ``Improved`` Vehicle and driver availability logic.
* ``Enhanced`` reporting and dashboard performance.
* ``Fixed`` Minor bugs and stability issues.

18.0.1.0.0
*****************

* ``Added`` Initial release of Vehicle Rental System.
* ``Added`` Rental contract creation and management.
* ``Added`` Vehicle and driver assignment.
* ``Added`` Invoice generation and Accounting integration.
* ``Added`` Email notifications for key stages.
* ``Added`` Vehicle availability tracking.

Support
================================================================

For support, please contact:

* yashsuvta1236@gmail.com
* nitinupmanyu12@gmail.com

Author & Maintainer
================================================================

This module is developed and maintained by **CodeFusion Odooworks**.