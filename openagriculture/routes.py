from openagriculture import app, db
from openagriculture.models import Field, User
from openagriculture.forms import CreateFieldForm, DeleteFieldForm
from openagriculture.forms import LoginForm, RegisterForm, EditUserDetailsForm

from flask import render_template, redirect, url_for, flash
from flask import jsonify
from flask_login import login_user, logout_user, current_user, login_required

from pyproj import Geod
import numpy as np
import json

################################################################################

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login_page():

    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data) :
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

################################################################################

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("login_page"))

################################################################################

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():

        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)

        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

################################################################################

@app.route('/home')
@app.route('/dashboard')
@login_required
def home_page():

    # Retrieve current user
    user = current_user

    # Get user fields
    fields = user.fields

    print("Fields",fields)

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

    map_center = (minlat, minlon, maxlat, maxlon)

    return render_template('home.html', fields=fields, fields_dataset=json.dumps(fields_dataset), map_center=map_center)

################################################################################

@app.route('/fields')
@login_required
def fields_page():

    # Retrieve user fields
    fields = current_user.fields

    return render_template('fields.html', fields=fields)

################################################################################

@app.route('/create-field', methods=["POST", "GET"])
@login_required
def create_field_page():
    form = CreateFieldForm()

    if form.validate_on_submit():

        lat = [float(l) for l in form.geometry.data.split(',')[::2]]
        lon = [float(l) for l in form.geometry.data.split(',')[1::2]]

        geod = Geod('+a=6378137 +f=0.0033528106647475126')
        poly_area, poly_perimeter = geod.polygon_area_perimeter(lon, lat)

        def PolyArea(x,y):
            return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

        field_to_create = Field(name=form.name.data,
                                crop=form.crop.data,
                                geometry=form.geometry.data,
                                area=np.round(np.abs(poly_area/1e4),2))


        current_user.fields.append(field_to_create)
        db.session.commit()

        return redirect(url_for('home_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error while creating new field: {err_msg}', category='danger')

    return render_template('create_field.html', form=form)

################################################################################

@app.route('/delete-field', methods=["POST","GET"])
@login_required
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

################################################################################

@app.route('/<string:name>')
@app.route('/<string:name>/<int:index>')
@login_required
def field_details_page(name, index=-1):

    field = Field.query.filter_by(name=name).first()

    field_data = {}
    field_data["geometry"]  = [(float(lat),float(lon)) for lat,lon in zip(field.geometry.split(',')[::2],field.geometry.split(',')[1::2])]

    msi_list = []

    for idx,multispectraindex in enumerate(field.msi_index):

        msi = {}

        msi["date"]       = multispectraindex.date
        msi["latitude"]   = multispectraindex.latitude
        msi["longitude"]  = multispectraindex.longitude
        msi["ndvi"]       = multispectraindex.ndvi
        msi_list.append(msi)



    if(len(msi_list) == 0) :
        field_data["is_empty"] = True
    else:
        field_data["is_empty"] = False

    if(field_data["is_empty"] == False):

        field_data["latitude"] = msi_list[index]["latitude"]
        field_data["longitude"] = msi_list[index]["longitude"]
        field_data["ndvi"] = msi_list[index]["ndvi"]
        field_data["date"] = msi_list[index]["date"]
        field_data["current_index"] = index

    mean_ndvi = np.average([float(el) for el in field_data["ndvi"].split(',')])

    return render_template('field_details.html', mean_ndvi=mean_ndvi, current_index=index, field_data=json.dumps(field_data), name=field.name, crop=field.crop, area=field.area, date=field_data["date"])

################################################################################

@app.route('/edit-user-details', methods=["POST","GET"])
@login_required
def edit_user_detail_page():

    user = current_user

    form = EditUserDetailsForm()

    if form.validate_on_submit():

        user.company_name = form.company_name.data
        user.farm_address = form.farm_address.data
        user.fiscal_code = form.fiscal_code.data

        db.session.commit()


    return render_template('edit_user_details.html', form=form, user=user)

################################################################################
