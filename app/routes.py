from flask import render_template, request, redirect, url_for
from app import app
from app.actions.index import *
from app.models.User import BaseUser
from app.models.Vaccine import BaseVaccine
from app.models.Article import BaseArticle
from app.models.Village import BaseVillage
from app.models.ConfigVaccine import BaseConfigVaccine

# page list user


@app.route('/admin/users/list')
def userList():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    req = request.args.to_dict()
    search = req.get("search")
    if search == None:
        search = ""
    entries = User.findAll(search)
    size = list(entries.clone()).__len__()
    return render_template('/users/list.html', entries=entries,  id_login=id_login, role_login=role_login, search=search, size=size)

# page create user


@app.route('/admin/users/create', methods=['GET'])
def userCreate():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    villages = Village.findAll()
    vaccines = Vaccine.findAll()
    return render_template('/users/create.html', villages=villages, vaccines=vaccines, id_login=id_login, role_login=role_login)

# api create user


@app.route('/admin/users/create', methods=['POST'])
def userCreatePost():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
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
        data = BaseVaccine("", "", "")
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

# page edit user


@app.route('/admin/users/edit/<string:id>')
def update(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    entry = User.findOne(id)
    villages = Village.findAll()
    return render_template('/users/edit.html', entry=entry, villages=villages, id_login=id_login, role_login=role_login)

# page change status user


@app.route('/admin/users/change-status/<string:id>', methods=['POST'])
def updateStatus(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    User.changStatus(id)
    return redirect(url_for('userList'))
# api change status user


@app.route('/admin/users/update', methods=['POST'])
def updateHandle():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    # Get data form
    form = request.form
    # Handle form
    _id = form.get("_id")
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
    print(form1)
    orders = form1.get("vaccine[][order]")
    names = form1.get("vaccine[][name]")
    dates = form1.get("vaccine[][date]")
    listVaccine = []
    for index in range(len(orders)):
        data = BaseVaccine("", "", "")
        data.name = names[index]
        data.order = int(orders[index])
        data.date = dates[index]
        listVaccine.append(data.__dict__)
    # Add vaccine to form
    entry.vaccine = listVaccine
    # Add document to mongodb
    User.updateOne(_id, entry.__dict__)
    # To page list user
    return redirect(url_for('userList'))

# api delete user


@app.route('/admin/users/delete/<string:id>', methods=['POST'])
def delete(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    User.deleteOne(id)
    return redirect(url_for('userList'))

# End CRUD user

# Start auth

# page login


@app.route('/')
def notFound():
    return redirect(url_for('login'))

# page login


@app.route('/auth/login')
def login():
    return render_template('/auth/login.html', check=False)

# api login


@app.route('/auth/login', methods=['POST'])
def checkLogin():
    form = request.form
    # Handle form
    phone = form.get("phone")
    password = form.get("password")
    entry = Auth.login(phone, password)
    if (entry == None):
        return render_template('/auth/login.html', check=True)
    else:
        global id_login
        id_login = entry['_id']
        global role_login
        role_login = entry['position']
        return redirect(url_for('articles'))

# page register


@app.route('/auth/register')
def register():
    villages = Village.findAll()
    return render_template('/auth/register.html', villages=villages)

# api register


@app.route('/auth/register', methods=['POST'])
def handleRegister():
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
    entry.password = form.get("password")
    entry.enable = 0
    entry.vaccine = []
    # Add document to mongodb
    User.appendOne(entry.__dict__)
    # To page list user
    return redirect(url_for('login'))

# handle logout


@app.route('/auth/logout')
def logout():
    return redirect(url_for('login'))

# page articles


@app.route('/admin/articles/list')
def articles():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    req = request.args.to_dict()
    title = req.get("title")
    if title == None:
        title = ""
    entries = []
    entries = Article.findAll(title)
    size = list(entries.clone()).__len__()
    return render_template('/articles/list.html', entries=entries, role_login=role_login, id_login=id_login, title=title, size=size)

# page create articles


@app.route('/admin/articles/create')
def createArticles():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    villages = Village.findAll()
    return render_template('/articles/create.html', id_login=id_login, role_login=role_login, villages=villages)

# api create articles


@app.route('/admin/articles/create',  methods=['POST'])
def handleCreateArticles():
    form = request.form
    # Handle form
    entry = BaseArticle()
    print(entry)
    entry.title = form.get("title")
    entry.content = form.get("content")
    entry.created_at = form.get("created_at")
    entry.village_id = form.get("village_id")
    entry.village = Village.findOne(entry.village_id)["name"]
    Article.appendOne(entry.__dict__)
    return redirect(url_for('articles'))

# api edit articles


@app.route('/admin/articles/update',  methods=['POST'])
def handleUpdateArticles():
    form = request.form
    # Handle form
    _id = form.get("_id")
    entry = BaseArticle()
    entry.title = form.get("title")
    entry.content = form.get("content")
    entry.created_at = form.get("created_at")
    entry.village_id = form.get("village_id")
    entry.village = Village.findOne(entry.village_id)["name"]
    Article.updateOne(_id, entry.__dict__)
    return redirect(url_for('articles'))

# api delete articles


@app.route('/admin/articles/delete/<string:id>', methods=['POST'])
def deleteArticles(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    Article.deleteOne(id)
    return redirect(url_for('articles'))

# page edit articles


@app.route('/admin/articles/edit/<string:id>')
def updateArticles(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    entry = Article.findOne(id)
    villages = Village.findAll()
    return render_template('/articles/edit.html', entry=entry, id_login=id_login, role_login=role_login, villages=villages)

# vaccine

# page list vaccine


@app.route('/admin/vaccines/list')
def vaccines():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    entries = Vaccine.findAll()
    return render_template('/vaccines/list.html', entries=entries, role_login=role_login, id_login=id_login)

# page create vaccine


@app.route('/admin/vaccines/create')
def createVaccines():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    return render_template('/vaccines/create.html', id_login=id_login, role_login=role_login)

# api create vaccine


@app.route('/admin/vaccines/create',  methods=['POST'])
def handleCreateVaccines():
    form = request.form
    # Handle form
    entry = BaseConfigVaccine()
    entry.name = form.get("name")
    entry.source = form.get("source")
    Vaccine.appendOne(entry.__dict__)
    return redirect(url_for('vaccines'))

# api delete vaccine


@app.route('/admin/vaccines/delete/<string:id>', methods=['POST'])
def deleteVaccines(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    Vaccine.deleteOne(id)
    return redirect(url_for('vaccines'))

# page edit vaccine


@app.route('/admin/vaccines/edit/<string:id>')
def updateVaccines(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    entry = Vaccine.findOne(id)
    return render_template('/vaccines/edit.html', entry=entry, id_login=id_login, role_login=role_login)

# api edit vaccine


@app.route('/admin/vaccines/update',  methods=['POST'])
def handleUpdateVaccines():
    form = request.form
    # Handle form
    _id = form.get("_id")
    entry = BaseConfigVaccine()
    entry.name = form.get("name")
    entry.source = form.get("source")
    Vaccine.updateOne(_id, entry.__dict__)
    return redirect(url_for('vaccines'))

# villages

# page list villages


@app.route('/admin/villages/list')
def villages():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    entries = Village.findAll()
    return render_template('/villages/list.html', entries=entries, role_login=role_login, id_login=id_login)

# page create villages


@app.route('/admin/villages/create')
def createVillages():
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    return render_template('/villages/create.html', id_login=id_login, role_login=role_login)

# api create villages


@app.route('/admin/villages/create',  methods=['POST'])
def handleCreateVillages():
    form = request.form
    # Handle form
    entry = BaseVillage()
    entry.name = form.get("name")
    Village.appendOne(entry.__dict__)
    return redirect(url_for('villages'))

# api delete villages


@app.route('/admin/villages/delete/<string:id>', methods=['POST'])
def deleteVillages(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    Village.deleteOne(id)
    return redirect(url_for('villages'))

# page edit villages


@app.route('/admin/villages/edit/<string:id>')
def updateVillages(id):
    try:
        id_login
    except NameError:
        return redirect(url_for('login'))
    entry = Village.findOne(id)
    print(entry, "village")
    return render_template('/villages/edit.html', entry=entry, id_login=id_login, role_login=role_login)

# api edit villages


@app.route('/admin/villages/update',  methods=['POST'])
def handleUpdateVillages():
    form = request.form
    # Handle form
    _id = form.get("_id")
    entry = BaseVillage()
    entry.name = form.get("name")
    Village.updateOne(_id, entry.__dict__)
    return redirect(url_for('villages'))
