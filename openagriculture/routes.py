from openagriculture import app, db
from openagriculture.models import Field
from openagriculture.forms import CreateFieldForm, DeleteFieldForm
from flask import render_template, redirect, url_for, flash

import numpy as np
import json

@app.route('/')
@app.route('/home')
@app.route('/dashboard')
def home_page():
    fields = Field.query.all()

    fields_dataset = []

    minlat = 1000
    minlon = 1000
    maxlat = -1000
    maxlon = -1000

    for field in fields:

        lat = [float(l) for l in field.geometry.split(',')[::2]]
        lon = [float(l) for l in field.geometry.split(',')[1::2]]

        current_minlat, current_maxlat = min(lat), max(lat)
        current_minlon, current_maxlon = min(lon), max(lon)

        if current_minlat < minlat : minlat = current_minlat
        if current_maxlat > maxlat : maxlat = current_maxlat
        if current_minlon < minlon : minlon = current_minlon
        if current_maxlon > maxlon : maxlon = current_maxlon

        _f = {}
        _f['name'] = field.name
        _f['crop'] = field.crop
        _f['area'] = field.area

        _f['geometry'] = [(float(lat),float(lon)) for lat,lon in zip(field.geometry.split(',')[::2],field.geometry.split(',')[1::2])]


        fields_dataset.append(_f)


    map_center = ((maxlat+minlat)/2, (maxlon+minlon)/2)

    return render_template('home.html', fields=fields, fields_dataset=json.dumps(fields_dataset), map_center=map_center)


@app.route('/fields')
def fields_page():
    fields = Field.query.all()

    return render_template('fields.html', fields=fields)

@app.route('/create-field', methods=["POST", "GET"])
def create_field_page():
    form = CreateFieldForm()

    if form.validate_on_submit():

        lat = [float(l) for l in form.geometry.data.split(',')[::2]]
        lon = [float(l) for l in form.geometry.data.split(',')[1::2]]

        def PolyArea(x,y):
            return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

        field_to_create = Field(name=form.name.data,
                                crop=form.crop.data,
                                geometry=form.geometry.data,
                                area=PolyArea(lat,lon))
        db.session.add(field_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error while creating new field: {err_msg}', category='danger')

    return render_template('create_field.html', form=form)

@app.route('/delete-field', methods=["POST","GET"])
def delete_field_page():

    form = DeleteFieldForm()

    form.field.choices = [(g.name,g.name) for g in Field.query.all()]

    # Retrieve fields entries from Database
    fields = Field.query.all()

    if form.validate_on_submit():

        field_to_delete = Field.query.filter_by(name=form.field.data).first()
        db.session.delete(field_to_delete)
        db.session.commit()

        return redirect(url_for('home_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error while creating new field: {err_msg}', category='danger')



    return render_template('delete_field.html', form=form, fields=fields)


@app.route('/<string:name>')
def field_details_page(name):    
    field = Field.query.filter_by(name=name).first()
    return render_template('field_details.html', field=field)
