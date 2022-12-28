from flask import render_template, request,redirect, url_for
from app import app
from app.actions.index import *
from app.models.User import BaseUser
from app.models.Vaccine import BaseVaccine
# User controller
@app.route('/admin/users')
@app.route('/admin/users/list')
def userList():
    entries = User.findAll()
    villages = Village.findAll()
    return render_template('/users/list.html', entries=entries)

@app.route('/admin/users/create', methods=['GET'])
def userCreate():
    villages = Village.findAll()
    vaccines = Vaccine.findAll()
    return render_template('/users/create.html', villages=villages, vaccines= vaccines)

@app.route('/admin/users/create', methods=['POST'])
def  userCreatePost():
    # Get data form
    form = request.form
    # Handle form
    entry = BaseUser()
    entry.name = form.get("name")
    entry.dob = form.get("dob")
    entry.position = int(form.get("position"))
    entry.sex = int(form.get("sex"))
    entry.village_id = form.get("village_id")
    entry.village = Village.findOne(entry.village_id)["name"]
    entry.health_insurance = form.get("health_insurance")
    entry.card = form.get("card")
    entry.phone = form.get("phone")
    entry.description = form.get("description")
    entry.password = '123456'
    entry.enable = 1
    # Handle Vaccine
    form1 = form.to_dict(flat=False)
    orders = form1.get("vaccine[][order]")
    names = form1.get("vaccine[][name]")
    dates = form1.get("vaccine[][date]")
    listVaccine = []
    for index in range(len(orders)):
        data =  BaseVaccine("","","")
        data.name = names[index]
        data.order = int(orders[index])
        data.date = dates[index]
        listVaccine.append(data.__dict__)
    # Add vaccine to form
    entry.vaccine = listVaccine
    # Add document to mongodb
    User.appendOne(entry.__dict__)
    # To page list user
    return redirect(url_for('userList'))

# @app.route('/update/<int:id>')
# def updateRoute(id):
#     if not id or id != 0:
#         entry = Entry.query.get(id)
#         if entry:
#             return render_template('update.html', entry=entry)

#     return "of the jedi"

# @app.route('/update/<int:id>', methods=['POST'])
# def update(id):
#     if not id or id != 0:
#         entry = Entry.query.get(id)
#         if entry:
#             form = request.form
#             title = form.get('title')
#             description = form.get('description')
#             entry.title = title
#             entry.description = description
#             db.session.commit()
#         return redirect('/')

#     return "of the jedi"


@app.route('/admin/users/delete/<string:id>', methods=['POST'])
def delete(id):
    User.deleteOne(id)
    return redirect(url_for('userList'))
 
# @app.route('/turn/<int:id>')
# def turn(id):
#     if not id or id != 0:
#         entry = Entry.query.get(id)
#         if entry:
#             entry.status = not entry.status
#             db.session.commit()
#         return redirect('/')

#     return "of the jedi"

# @app.errorhandler(Exception)
# def error_page(e):
#     return "of the jedi"
