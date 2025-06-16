================================================================
Vehicle Rental System
================================================================

The **Vehicle Rental System** is a custom Odoo module that enables comprehensive management of vehicle rental operations. This module allows businesses to manage rental contracts, assign vehicles and drivers, track rental durations, invoice customers, and automate email notifications during the rental lifecycle. It is designed to streamline vehicle allocation, ensure proper contract handling, and integrate with Odoo’s native accounting and CRM systems.

.. role:: raw-html(raw)
    :format: html

**Table of contents**

.. contents::
   :local:

Installation
================================================================

**To install this module, follow these steps:**

* Place the module folder inside your Odoo `addons` directory.
* Restart the Odoo server.
* Go to **Apps**, update the app list, and search for "Vehicle Rental System".
* Click **Install** to add it to your instance.

Usage
================================================================

**How to use this module:**

Create a Vehicle Rental Contract
To create a rental contract, go to the Vehicle Rental menu and click on Create. Fill in the necessary customer details, rental period, and select the desired vehicle.

Screenshot:
.. image:: vehicle_rental_system/static/description/rental_contract_draft.png
:alt: Rental Contract Form
:width: 300px

Assign Drivers
Drivers are assigned during the Processing stage of the rental contract. The system ensures no double-booking by making sure only available drivers are assigned.

Screenshot:
.. image:: vehicle_rental_system/static/description/rental_contract_confirmation.png
:alt: Assign Driver
:width: 300px

Rental Lifecycle
Rental contracts progress through several states: Draft, Processing, Confirmed, Done, and Cancelled. Each state triggers different validations and email notifications.

Screenshot:
.. image:: vehicle_rental_system/static/description/rental_contract_confirmation.png
:alt: Contract Stages
:width: 300px

Vehicle Availability
Vehicles are marked as Available or Rented based on their current usage. The system automatically tracks availability and prevents double-booking.

Screenshot:
.. image:: vehicle_rental_system/static/description/vehicle.png
:alt: Vehicle Status
:width: 300px

Drivers Status
Drivers are marked as Available or Engaged based on their current contract. The system automatically tracks availability and prevents double-booking.

Screenshot:
.. image:: vehicle_rental_system/static/description/Drivers_status.png
:alt: Invoice Generation
:width: 300px


Reporting & Dashboard
Track key metrics such as vehicle usage, rental performance, and customer history through built-in reports and dashboards. These insights help with operational planning and performance analysis.

Screenshot:
.. image:: vehicle_rental_system/static/description/vehicle_rental_dashboard_view.png
:alt: Rental Dashboard
:width: 300px

Change Logs
================================================================

18.0.1.0.0
*****************
* ``Added`` Initial release of Vehicle Rental System.
* ``Added`` Rental contract creation and management.
* ``Added`` Vehicle and driver assignment.
* ``Added`` Invoice generation and integration with accounting.
* ``Added`` Email notifications for key stages.
* ``Added`` Vehicle availability tracking.

Support
================================================================

`yashsuvta1236@gmail.com,nitinupmanyu12@gmail.com`_

Author & Maintainer
-------------------

This module is maintained by the CodeFusion Odooworks
