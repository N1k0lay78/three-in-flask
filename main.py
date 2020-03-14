from datetime import datetime

from flask import Flask, render_template, url_for
from flask_login import LoginManager, login_manager, login_user
from werkzeug.utils import redirect
from data.forms import RegisterForm, LoginForm

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register/', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        print(123)
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


@app.route('/works/')
def works():
    jobs = []
    for i, job in enumerate(session.query(Jobs).all()):
        _job = {}
        _job['id'] = i + 1
        _job['title'] = job.job
        leader = session.query(User).filter(User.id == job.team_leader).first()
        _job['team_leader'] = f'{leader.name} {leader.surname}'
        _job['duration'] = job.work_size
        _job['collaboration'] = job.collaborators
        _job['is_finished'] = job.is_finished
        jobs.append(_job)
    print(jobs)
    return render_template('works.html', jobs=jobs, style=url_for('static', filename='css/style.css'))


def main():
    # флаг для задач
    zadacha_1 = False
    zadacha_2 = False
    if zadacha_1:
        user = User()
        user.surname = 'Scott'
        user.name = 'Ridley'
        user.age = 21
        user.position = 'captain'
        user.speciality = 'research engineer'
        user.address = 'module_1'
        user.email = 'scott_chief@mars.org'
        session.add(user)
        session.commit()
        user = User()
        user.surname = 'Nikniksham'
        user.name = 'Nikniksham'
        user.age = 21
        user.position = 'captain'
        user.speciality = 'engineer'
        user.address = 'module_10'
        user.email = 'nikniksham@mars.org'
        session.add(user)
        session.commit()
        user = User()
        user.surname = 'Builder'
        user.name = 'Bob'
        user.age = 21
        user.position = 'Worker'
        user.speciality = 'Builder'
        user.address = 'module_1'
        user.email = 'Bob@mars.org'
        session.add(user)
        session.commit()
        user = User()
        user.surname = 'Builder'
        user.name = 'Bot'
        user.age = 21
        user.position = 'gost'
        user.speciality = 'Builder'
        user.address = 'module_1'
        user.email = 'Bot@mars.org'
        session.add(user)
        session.commit()
    if zadacha_2:
        jobs = Jobs()
        jobs.team_leader = 1
        jobs.job = 'deployment of residential modules 1 and 2'
        jobs.work_size = 15
        jobs.collaborators = '2, 3'
        jobs.start_date = datetime.now()
        session.add(jobs)
        session.commit()
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    print('http://127.0.0.1:5000/login/')
    main()
