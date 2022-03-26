from openagriculture import app, db
from openagriculture.models import Field
from openagriculture.forms import CreateFieldForm
from flask import render_template, redirect, url_for, flash

import numpy as np

@app.route('/')
@app.route('/home')
@app.route('/dashboard')
def home_page():
    fields = Field.query.all()
    return render_template('home.html', fields=fields)


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
