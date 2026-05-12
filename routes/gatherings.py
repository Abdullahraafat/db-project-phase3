from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from services.gathering_db import (
    get_all_gatherings, add_gathering,
    update_gathering, get_gathering_by_id,
)
from services.venue_db import get_all_venues

gatherings_bp = Blueprint('gatherings', __name__)


def parse_datetime_field(value):
    if not value:
        return None
    return datetime.fromisoformat(value)


@gatherings_bp.route('/gatherings')
def list_gatherings():
    gatherings = get_all_gatherings()
    return render_template('gatherings/list_gatherings.html', gatherings=gatherings)


@gatherings_bp.route('/gatherings/add', methods=['GET', 'POST'])
def add_gathering_route():
    venues = get_all_venues()
    if request.method == 'POST':
        add_gathering(
            request.form['gathering_name'],
            request.form['category'],
            parse_datetime_field(request.form['start_datetime']),
            parse_datetime_field(request.form['end_datetime']),
            int(request.form['venue_id']),
        )
        return redirect(url_for('gatherings.list_gatherings'))
    return render_template('gatherings/add_gathering.html', venues=venues)


@gatherings_bp.route('/gatherings/edit/<int:gathering_id>', methods=['GET', 'POST'])
def edit_gathering_route(gathering_id):
    gathering = get_gathering_by_id(gathering_id)
    venues    = get_all_venues()
    if request.method == 'POST':
        update_gathering(
            gathering_id,
            request.form['gathering_name'],
            request.form['category'],
            parse_datetime_field(request.form['start_datetime']),
            parse_datetime_field(request.form['end_datetime']),
            int(request.form['venue_id']),
        )
        return redirect(url_for('gatherings.list_gatherings'))
    return render_template('gatherings/edit_gathering.html', gathering=gathering, venues=venues)