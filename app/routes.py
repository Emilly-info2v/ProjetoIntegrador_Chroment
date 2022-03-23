from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import RegisterUser, LoginUser, RegisterTask

from app import db
from app.models import User
from app.models import Task


def init_app(app):

    # Landing Page

    @app.route('/')
    def index():
        if current_user.is_active:
            tasks = Task.query.all()
            return render_template('home.html', tasks=tasks)
        return render_template('index.html')

    # autenticação 

    @app.route('/register/', methods=('GET', 'POST'))
    def register():
        form = RegisterUser()

        if form.validate_on_submit():

            if User.query.filter_by(email=form.email.data).first():
                flash("O email já está registrado", category="danger")
                return redirect(url_for('register'))

            user = User()

            user.name = form.name.data
            user.email = form.email.data
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect(url_for('index'))

        return render_template('register.html', form=form)

    @app.route('/login/', methods=('GET', 'POST'))
    def login():
        form = LoginUser()

        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()

            if not user:
                flash("Email incorreto", category="danger")
                return redirect(url_for('login'))

            if not check_password_hash(user.password, form.password.data):
                flash("Email correto", category='success')
                flash("Senha incorreta", category='danger')
                return redirect(url_for('login'))

            login_user(user)
            return redirect(url_for('index'))

        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # Perfil

    @app.route('/perfil/')
    def profile():
        user = User.query.filter_by(id=current_user.id).first()
        form = RegisterUser()
        return render_template('profile.html', user=user, form=form)

    @app.route('/perfil/edit', methods=('GET', 'POST'))
    def edit_profile():
        user = User.query.filter_by(id=current_user.id).first()
        form = RegisterUser()

        form.name.data = user.name
        form.email.data = user.email

        return render_template('edit_profile.html', form=form, user=user)

    @app.route('/perfil/edit/submit', methods=('GET', 'POST'))
    def submit_profile_edit():
        form = RegisterUser()

        user = User.query.filter_by(id=current_user.id).first()

        if form.validate_on_submit():

            if User.query.filter_by(email=form.email.data).first():
                if form.email.data != user.email:
                    flash("O email já está registrado", category="danger")
                    return redirect(url_for("edit_profile"))

            user.name = form.name.data
            user.email = form.email.data

            db.session.commit()

            return redirect(url_for('profile'))

    @app.route('/perfil/excluir')
    def delete_profile():
        user = User.query.filter_by(id=current_user.id).first()

        db.session.delete(user)
        db.session.commit()

        return redirect(url_for('index'))

    # usuários

    @app.route('/usuarios/')
    def users():
        users = User.query.all()
        return render_template('users.html', users=users)

    # Tarefas
    
    @app.route('/tarefa/<id>')
    def task(id):
        task = Task.query.filter_by(id=id).first()
        return render_template('task.html', task=task)

    @app.route('/criar/tarefa', methods=('GET', 'POST'))
    def new_task():
        form = RegisterTask()

        if form.validate_on_submit():

            task = Task()

            task.title = form.title.data
            task.description = form.description.data

            db.session.add(task)
            db.session.commit()

            flash('Tarefa criada com sucesso', category='success')

        form.title.data = ''
        form.description.data = ''

        return render_template('new_task.html', form=form)

    @app.route('/tarefa/concluida/<id>')
    def task_completed(id):
        task = Task.query.filter_by(id=id).first()

        db.session.delete(task)
        db.session.commit()

        return redirect(url_for('index'))

    @app.route('/tarefa/editar/<id>', methods=('GET', 'POST'))
    def edit_task(id):
        form = RegisterTask()
        task = Task.query.filter_by(id=id).first()

        form.title.data = task.title
        form.description.data = task.description

        return render_template('edit_task.html', task=task, form=form)

    @app.route('/tarefa/editar/submit/<id>', methods=('GET', 'POST'))
    def submit_task_edit(id):
        form = RegisterTask()
        task = Task.query.filter_by(id=id).first()

        if form.validate_on_submit():

            task.title = form.title.data
            task.description = form.description.data

            db.session.commit()

            return redirect(url_for('task', id=id))

    @app.route('/tarefa/excluir/<id>')
    def delete_task(id):
        task = Task.query.filter_by(id=id).first()

        db.session.delete(task)
        db.session.commit()

        return redirect(url_for('index'))