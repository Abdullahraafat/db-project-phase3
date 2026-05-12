from flask import Blueprint, render_template, request, redirect, url_for
from services.staff_db import (
    get_all_staff, add_staff, assign_staff_to_gathering,
    remove_assignment, get_all_assignments, get_top_coordinator_last_month,
)
from services.gathering_db import get_all_gatherings

staff_bp = Blueprint('staff', __name__)


@staff_bp.route('/staff')
def manage_staff():
    staff      = get_all_staff()
    gatherings = get_all_gatherings()
    schedule   = get_all_assignments()
    top_coord  = get_top_coordinator_last_month()
    return render_template(
        'staff/staff_list.html',
        staff=staff,
        gatherings=gatherings,
        schedule=schedule,
        top_coord=top_coord,
    )


@staff_bp.route('/add-staff', methods=['POST'])
def add_new_staff():
    add_staff(
        request.form['first_name'],
        request.form['last_name'],
        request.form['email'],
    )
    return redirect(url_for('staff.manage_staff'))


@staff_bp.route('/assign-staff', methods=['POST'])
def assign_staff():
    assign_staff_to_gathering(
        request.form['staff_id'],
        request.form['gathering_id'],
    )
    return redirect(url_for('staff.manage_staff'))


@staff_bp.route('/remove-assignment/<int:assignment_id>', methods=['POST'])
def remove_assignment_route(assignment_id):
    remove_assignment(assignment_id)
    return redirect(url_for('staff.manage_staff'))