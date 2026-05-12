from flask import Blueprint, render_template, request, redirect, url_for
from services.entry_class_db import (
    get_all_entry_classes, get_all_gec_records,
    add_gathering_entry_class, update_gathering_entry_class,
    get_most_popular_category, get_entry_classes_per_gathering,
)
from services.gathering_db import get_all_gatherings

entry_bp = Blueprint('entry_bp', __name__)


@entry_bp.route('/add_entry_class', methods=['GET', 'POST'])
def add_entry_class():
    if request.method == 'POST':
        add_gathering_entry_class(
            request.form['gathering_id'],
            request.form['entry_class_id'],
            request.form['price'],
            request.form['allocated_seats'],
        )
        return redirect(url_for('entry_bp.add_entry_class'))

    gatherings    = get_all_gatherings()
    entry_classes = get_all_entry_classes()
    return render_template(
        'entries/add_entry_class.html',
        gatherings=gatherings,
        entry_classes=entry_classes,
    )


@entry_bp.route('/update_entry_class', methods=['GET', 'POST'])
def update_entry_class():
    if request.method == 'POST':
        update_gathering_entry_class(
            request.form['gec_id'],
            request.form['price'],
            request.form['allocated_seats'],
        )
        return redirect(url_for('entry_bp.update_entry_class'))

    gec_records = get_all_gec_records()
    return render_template('entries/update_entry_class.html', gec_records=gec_records)


@entry_bp.route('/inquiry1')
def inquiry1():
    result = get_most_popular_category()
    return render_template('entries/inquiry1.html', result=result)


@entry_bp.route('/inquiry5')
def inquiry5():
    result = get_entry_classes_per_gathering()
    return render_template('entries/inquiry5.html', result=result)