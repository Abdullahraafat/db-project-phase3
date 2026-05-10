from flask import Blueprint, render_template, request, redirect, url_for
from services.gathering_db import (
    get_all_gatherings, add_gathering, update_gathering, get_gathering_by_id
)
from services.venue_db import get_all_venues

gatherings_bp = Blueprint('gatherings', __name__)


# ── List all gatherings ──────────────────────────────────────────────────────
@gatherings_bp.route('/gatherings', strict_slashes=True)
def list_gatherings():
    gatherings = get_all_gatherings()
    return render_template('gatherings/list_gatherings.html', gatherings=gatherings)


# ── Add gathering ────────────────────────────────────────────────────────────
@gatherings_bp.route('/gatherings/add', methods=['GET', 'POST'], strict_slashes=True)
def add_gathering_route():
    venues = get_all_venues()
    if request.method == 'POST':
        gathering_name = request.form['gathering_name']
        category       = request.form['category']
        start_datetime = request.form['start_datetime']
        end_datetime   = request.form['end_datetime']
        venue_id       = int(request.form['venue_id'])
        add_gathering(gathering_name, category, start_datetime, end_datetime, venue_id)
        return redirect(url_for('gatherings.list_gatherings'))
    return render_template('gatherings/add_gathering.html', venues=venues)


# ── Edit gathering ───────────────────────────────────────────────────────────
@gatherings_bp.route('/gatherings/edit/<int:gathering_id>', methods=['GET', 'POST'], strict_slashes=True)
def edit_gathering_route(gathering_id):
    gathering = get_gathering_by_id(gathering_id)
    venues    = get_all_venues()
    if request.method == 'POST':
        gathering_name = request.form['gathering_name']
        category       = request.form['category']
        start_datetime = request.form['start_datetime']
        end_datetime   = request.form['end_datetime']
        venue_id       = int(request.form['venue_id'])
        update_gathering(gathering_id, gathering_name, category,
                         start_datetime, end_datetime, venue_id)
        return redirect(url_for('gatherings.list_gatherings'))
    return render_template('gatherings/edit_gathering.html',
                           gathering=gathering, venues=venues)
