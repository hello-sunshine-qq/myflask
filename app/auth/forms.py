from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
	email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('密码', validators=[DataRequired()])
	remember_me = BooleanField('记住密码')
	submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
	email = StringField('注册邮箱', validators=[DataRequired(), Length(1, 64), Email()])
	username = StringField('用户名', validators=[DataRequired(), Length(1,128)])
	password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='两次密码不匹配')])
	password2 = PasswordField('确认密码', validators=[DataRequired()])
	submit = SubmitField('注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已被注册')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已存在')

class Changepassword(FlaskForm):
	old_password = PasswordField('旧密码', validators=[DataRequired()])
	new_password = PasswordField('新密码', validators=[DataRequired(),EqualTo('new_password2', message='两次密码不匹配')])
	new_password2 = PasswordField('确认新密码', validators=[DataRequired()])
	submit = SubmitField('确认修改')

class PasswordResetRequest(FlaskForm):
	email = StringField('验证邮箱', validators=[DataRequired(), Length(1,64), Email()])
	submit = SubmitField('确认发送')

class PasswordReset(FlaskForm):
	password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message="两次密码不匹配")])
	password2 = PasswordField('确认密码', validators=[DataRequired()])
	submit = SubmitField('重置密码')


