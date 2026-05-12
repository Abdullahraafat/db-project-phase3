from flask import Blueprint, render_template, request, redirect, url_for
from services.venue_db import (
    get_all_venues, add_venue, update_venue,
    get_venue_by_id, get_venues_no_passes_last_month,
)

venues_bp = Blueprint('venues', __name__)


@venues_bp.route('/venues')
def list_venues():
    venues = get_all_venues()
    return render_template('venues/list_venues.html', venues=venues)


@venues_bp.route('/venues/add', methods=['GET', 'POST'])
def add_venue_route():
    if request.method == 'POST':
        venue_name   = request.form['venue_name']
        location     = request.form['location']
        max_capacity = int(request.form['max_capacity'])
        add_venue(venue_name, location, max_capacity)
        return redirect(url_for('venues.list_venues'))
    return render_template('venues/add_venue.html')


@venues_bp.route('/venues/edit/<int:venue_id>', methods=['GET', 'POST'])
def edit_venue_route(venue_id):
    venue = get_venue_by_id(venue_id)
    if request.method == 'POST':
        venue_name   = request.form['venue_name']
        location     = request.form['location']
        max_capacity = int(request.form['max_capacity'])
        update_venue(venue_id, venue_name, location, max_capacity)
        return redirect(url_for('venues.list_venues'))
    return render_template('venues/edit_venue.html', venue=venue)


@venues_bp.route('/venues/inquiry2')
def inquiry2():
    results = get_venues_no_passes_last_month()
    return render_template('venues/inquiry2.html', results=results)
