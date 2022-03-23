from flask_wtf import FlaskForm
from wtforms.fields import (EmailField, PasswordField, StringField, SubmitField, TextAreaField)

class LoginUser(FlaskForm):
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  submit = SubmitField("Entrar")

class RegisterUser(FlaskForm):
  name = StringField("Nome")
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  submit = SubmitField("Criar conta")


class RegisterTask(FlaskForm):
  title = StringField('Título')
  description = TextAreaField('Descrição')
  submit = SubmitField('Criar tarefa')