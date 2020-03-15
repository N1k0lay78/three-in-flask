from datetime import datetime
from os import abort

from flask import Flask, render_template, url_for, request, make_response, jsonify
from flask_login import LoginManager, login_manager, login_user, login_required, current_user, logout_user
from werkzeug.utils import redirect

import jobs_api
import users_api
from data.category import Category
from data.deportament import Departments
from data.forms import RegisterForm, LoginForm, JobsForm, DepartmentsForm

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register/', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/works/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/works/")


@app.route('/works/')
def works():
    jobs = []
    for i, job in enumerate(session.query(Jobs).all()):
        _job = {}
        _job['id'] = i + 1
        _job['title'] = job.job
        leader = session.query(User).filter(User.id == job.team_leader).first()
        _job['tl_id'] = leader.id
        _job['team_leader'] = f'{leader.name} {leader.surname}'
        _job['duration'] = job.work_size
        _job['collaboration'] = job.collaborators
        _job['category'] = session.query(Category).filter(Category.jobs)
        _job['is_finished'] = job.is_finished
        _job['user'] = job.user
        jobs.append(_job)
    return render_template('works.html', jobs=jobs, style=url_for('static', filename='css/style.css'))


@app.route('/add-job/', methods=['GET', 'POST'])
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            start_date=datetime.now()
        )
        categ = Category()
        categ.name = form.category.data
        job.category.append(categ)
        session.add(job)
        session.commit()
        return redirect('/works/')
    return render_template('addjob.html', title='Добавление работы', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id,
                                         (Jobs.user == current_user) | (current_user.id == 1)).first()
        if job:
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.category.data = job.category
            form.is_finished.data = job.is_finished
        else:
            abort()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id,
                                         (Jobs.user == current_user) | (current_user.id == 1)).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            categ = Category()
            categ.name = form.category.data
            job.category.append(categ)
            job.is_finished = form.is_finished.data
            session.commit()
            return redirect('/works/')
        else:
            abort()
    return render_template('addjob.html', title='Редактирование работы', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id,
                                     (Jobs.user == current_user) | (current_user.id == 1)).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort()
    return redirect('/works/')


@app.route('/departments/')
def _departments():
    departments = []
    for i, depart in enumerate(session.query(Departments).all()):
        _deprat = {}
        _deprat["id"] = i + 1
        _deprat["title"] = depart.title
        tl = session.query(User).filter(User.id == depart.chief).first()
        _deprat["team_leader"] = f"{tl.name} {tl.surname}"
        _deprat["email"] = depart.email
        _deprat["collaboration"] = depart.members
        _deprat["tl_id"] = tl.id
        departments.append(_deprat)
    return render_template('departments.html', departments=departments,
                           style=url_for('static', filename='css/style.css'))


@app.route('/add-depart/', methods=['GET', 'POST'])
def add_depart():
    form = DepartmentsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        depart = Departments(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        session.add(depart)
        session.commit()
        return redirect('/departments/')
    return render_template('action-depart.html', title='Добавление департмаент', form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_depart(id):
    form = DepartmentsForm()
    if request.method == "GET":
        session = db_session.create_session()
        depart = session.query(Departments).filter(Departments.id == id,
                                                   (Departments.user == current_user) | (current_user.id == 1)).first()
        if depart:
            form.title.data = depart.title
            form.chief.data = depart.chief
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort()
    if form.validate_on_submit():
        session = db_session.create_session()
        depart = session.query(Departments).filter(Departments.id == id,
                                                   (Departments.user == current_user) | (current_user.id == 1)).first()
        if depart:
            depart.title = form.title.data
            depart.chief = form.chief.data
            depart.members = form.members.data
            depart.email = form.email.data
            session.commit()
            return redirect('/departments/')
        else:
            abort()
    return render_template('action-depart.html', title='Редактирование департамента', form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departs_delete(id):
    session = db_session.create_session()
    depart = session.query(Departments).filter(Departments.id == id,
                                               (Departments.user == current_user) | (current_user.id == 1)).first()
    if depart:
        session.delete(depart)
        session.commit()
    else:
        abort()
    return redirect('/departments/')


def main():
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    print('http://127.0.0.1:5000/login/')
    print('http://127.0.0.1:5000/works/')
    print('http://127.0.0.1:5000/jobs/1')
    print('http://127.0.0.1:5000/api/jobs/')
    print('http://127.0.0.1:5000/departments/')
    main()
