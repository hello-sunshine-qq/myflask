from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from . import auth
from .forms import LoginForm, RegistrationForm, Changepassword, PasswordResetRequest, PasswordReset
from ..models import User
from .. import db
from ..email import send_email

@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed and request.blueprint !='auth': 
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()	
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(password=form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('用户名或密码错误')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('您已退出')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(
				email = form.email.data,
				username = form.username.data,
				password = form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, '确认注册', 'auth/email/confirm', user=user, token=token)
		flash('确认注册邮件已发送至您的邮箱，请查收确认')
		return redirect(url_for('main.index'))
		flash('注册成功，请登录')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)

# 确认邮件视图
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		return redirect(url_for('main.index'))
		flash('您已确认您的邮件')
	else:
		flash('确认邮件链接不正确或已经过期')
	
	return redirect(url_for('main.index'))

#重新发送账户邮件确认
@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, '确认注册', 'auth/email/confirm', user=current_user, token=token)
	flash('新的确认注册邮件已发送至您的邮箱，请查收确认')
	return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('mail.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
	form = Changepassword()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.new_password.data
			db.session.add(current_user)
			db.session.commit()
			flash('修改成功')
			return redirect(url_for('main.index'))
		else:
			flash('密码修改失败，请重试！')
	return render_template('auth/change_password.html', form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index')) 
	form = PasswordResetRequest()
	user = User.query.filter_by(email=form.email.data).first()
	if user:
		token = user.generate_reset_token()
		send_email(user.email, "重置您的博客密码", 'auth/email/reset_password', user=user, token=token)
		flash('重置密码的邮件已发送至您的邮箱，请查收！')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordReset()
	if form.validate_on_submit():
		if User.reset_password(token, form.password.data):
			db.session.commit()
			flash('密码已重置')
			return redirect(url_for('auth.login'))
		else:
			flash('验证失败')
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html', form=form)
