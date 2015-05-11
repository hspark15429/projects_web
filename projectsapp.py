from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setupDB import Base, Project, Category, Entry

engine = create_engine('sqlite:///projects.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

##################################
##########PROJECTS   #############
##################################
@app.route('/')
@app.route('/projects/')
def projects():
    projects = session.query(Project).all()
    categories = session.query(Category).all()
    return render_template('projectsShow.html', projects = projects, categories = categories )

@app.route('/projects/new/', methods = ['POST', 'GET'])
def projects_new():
    if request.method == 'GET':
        return render_template('projectsNew.html')

    if request.method == 'POST':
        newProject = Project(name=request.form['name'])
        session.add(newProject)
        session.commit()
        return redirect(url_for("projects"))
    
@app.route('/projects/edit/<int:project_id>/', methods = ['POST', 'GET'])
def projects_edit(project_id):
    if request.method == 'GET':
        return render_template('projectsEdit.html',  project_id = project_id)

    if request.method == 'POST':
        currentProject = session.query(Project).filter_by(id = project_id).one()
        currentProject.name = request.form['name']
        session.add(currentProject)
        session.commit()
        return redirect(url_for("projects"))

@app.route('/projects/delete/<int:project_id>/', methods = ['POST', 'GET'])
def projects_delete(project_id):
    if request.method == 'GET':
        return render_template('projectsDelete.html',  project_id = project_id)

    if request.method == 'POST':
        currentProject = session.query(Project).filter_by(id=project_id).one()
        session.delete(currentProject)
        session.commit()
        return redirect(url_for("projects",))

##################################
##########ENTRIES    #############
##################################
@app.route('/projects/<int:project_id>/entries/', methods = ['GET'])
def entries(project_id):
    if request.method == 'GET':
        entries = session.query(Entry).filter_by(project_id=project_id).all()
        categories = session.query(Category).filter_by(project_id=project_id).all()
        project = session.query(Project).filter_by(id=project_id).one()
        print(len(categories))
        return render_template('entriesShow.html',  entries = entries, project= project, categories = categories)

@app.route('/projects/<int:project_id>/<int:category_id>/entries/new/', methods = ['GET', 'POST'])
def entries_new(project_id, category_id):
    if request.method == 'GET':
        return render_template('entriesNew.html',  project_id = project_id, category_id=category_id)
    if request.method == 'POST':
        newEntry = Entry(description = request.form['description'], project_id = project_id, category_id = category_id)
        session.add(newEntry)
        session.commit()
        return redirect(url_for("entries",project_id = project_id))

@app.route('/projects/<int:project_id>/entries/edit/<int:entry_id>/', methods = ['GET', 'POST'])
def entries_edit(project_id, entry_id):
    if request.method == 'GET':
        return render_template('entriesEdit.html',  project_id = project_id, entry_id = entry_id)
    if request.method == 'POST':
        entry = session.query(Entry).filter_by(id=entry_id).one()
        entry.description = request.form['description']
        session.add(entry)
        session.commit()
        return redirect(url_for("entries", project_id=project_id,))

@app.route('/projects/<int:project_id>/entries/delete/<int:entry_id>/', methods = ['GET', 'POST'])
def entries_delete(project_id, entry_id):
    if request.method == 'GET':
        return render_template('entriesDelete.html',  project_id = project_id, entry_id=entry_id)
    if request.method == 'POST':
        entry = session.query(Entry).filter_by(id=entry_id).one()
        session.delete(entry)
        session.commit()
        return redirect(url_for("entries", project_id=project_id))

##################################
##########CATEGORIES #############
##################################
@app.route('/projects/<int:project_id>/categories/new/', methods = ['GET', 'POST'])
def categories_new(project_id):
    if request.method == 'GET':
        return render_template('categoriesNew.html',  project_id = project_id)
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], project_id=project_id)
        session.add(newCategory)
        session.commit()
        return redirect(url_for("entries",project_id = project_id))

@app.route('/projects/<int:project_id>/categories/edit/<int:category_id>', methods = ['GET', 'POST'])
def categories_edit(project_id, category_id):
    if request.method == 'GET':
        return render_template('categoriesEdit.html',  project_id = project_id, category_id = category_id)
    if request.method == 'POST':
        category = session.query(Category).filter_by(id=category_id).one()
        category.name = request.form['name']
        return redirect(url_for("entries", project_id=project_id,))

@app.route('/projects/<int:project_id>/categories/delete/<int:category_id>', methods = ['GET', 'POST'])
def categories_delete(project_id, category_id):
    if request.method == 'GET':
        return render_template('categoriesDelete.html',  project_id = project_id, category_id=category_id)
    if request.method == 'POST':
        category = session.query(Category).filter_by(id=category_id).one()
        session.delete(category)
        session.commit()
        return redirect(url_for("entries", project_id=project_id))

if __name__ == '__main__':
    app.secret_key = "somesecretkey"
    app.debug = True
    app.run(host = '0.0.0.0', port = 50000)


