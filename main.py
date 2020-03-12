from datetime import datetime

from flask import Flask, render_template
from werkzeug.utils import redirect
from forms import RegisterForm

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=['GET', 'POST'])
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
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    # флаг для задач
    zadacha_1 = True
    zadacha_2 = True
    zadacha_3 = False
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
    if zadacha_2:
        jobs = Jobs()
        jobs.team_leader = 1
        jobs.job = 'deployment of residential modules 1 and 2'
        jobs.work_size = 15
        jobs.collaborators = '2, 3'
        jobs.start_date = datetime.now()
        session.add(jobs)
        session.commit()
    if zadacha_3:
        jobs = []
        for job in session.query(Jobs).all():
            _job = {}
            _job['title'] = job.job
            _job['duration'] = job.work_size
            _job['collaboration'] = job.collaborators

    app.run()


if __name__ == '__main__':
    main()