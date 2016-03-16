from flask import flash, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_paginate import Pagination
from app import app, login_manager
from model import *
from forms import *
import config
from datetime import datetime
import _helper as helper


def _render_login_template(form):
    return render_template('login.html', title='Login', form=form)


@app.route('/')
@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('inbox'))
    return _render_login_template(LoginForm())


@app.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if not form.validate_on_submit():
        flash('Wrong username or password.', 'danger')
        return _render_login_template(form)
    user = User.query\
        .filter_by(username=form.username.data.lower())\
        .first()
    login_user(user, remember=form.remember.data)
    return redirect(url_for('inbox'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


def render_signup_template(form):
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/signup', methods=['GET'])
def signup_get():
    if current_user.is_authenticated:
        return redirect(url_for('inbox'))
    return render_signup_template(SignupForm())


@app.route('/signup', methods=['POST'])
def signup_post():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('inbox'))
    elif User.query.filter_by(username=form.username.data.lower()).count():
        flash("This username is already taken.", 'danger')
    else:
        flash('Wrong username or password.', 'danger')
    return render_signup_template(form)


def _new_mails_count():
    return Mail.query\
        .filter_by(recipient_id=current_user.get_id(), status='sent', viewed=False)\
        .count()


def _draft_count():
    return Mail.query\
        .filter_by(sender_id=current_user.get_id(), status='draft')\
        .count()


@app.route('/inbox')
@app.route('/inbox/<int:page>')
@login_required
def inbox(page=1):
    total = Mail.query.filter_by(recipient_id=current_user.get_id(), status='sent').count()
    mails = Mail.query \
        .filter_by(recipient_id=current_user.get_id(), status='sent') \
        .order_by('timestamp DESC') \
        .paginate(page, config.MAIL_PER_PAGE) \
        .items
    pagination = Pagination(page=page,
                            per_page=config.MAIL_PER_PAGE,
                            total=total,
                            bs_version=3)
    return render_template('inbox.html',
                           title='Inbox',
                           pagination=pagination,
                           new_mails=_new_mails_count(),
                           draft_mails=_draft_count(),
                           mails=mails)


@app.route('/send', methods=['GET'])
@login_required
def send_get():
    draft_id = request.args.get('draft_id', None)
    form = SendMailForm()
    if helper.check_if_number(draft_id):
        mail = Mail.query\
            .filter_by(id=draft_id, sender_id=current_user.get_id(), status='draft')\
            .first()
        if mail:
            form.recipient.data = mail.recipient.username
            form.title.data = mail.title
            form.text.data = mail.text
            form.draft.data = True
            form.draft_id.data = draft_id
    return render_template('send-mail.html',
                           title='Send mail',
                           form=form,
                           new_mails=_new_mails_count(),
                           draft_mails=_draft_count())


def user_exists(username):
    return User.query.filter_by(username=username).count() > 0


@app.route('/send', methods=['POST'])
@login_required
def send_post():
    form = SendMailForm()
    if form.validate_on_submit():
        sender_id = current_user.get_id()
        recipient_id = User.query\
            .filter_by(username=form.recipient.data.lower())\
            .first()\
            .get_id()
        status = 'draft' if form.draft.data is True else 'sent'
        title = form.title.data or '...'
        text = form.text.data or '...'
        if form.draft_id.data:
            draft_id = form.draft_id.data
            draft_mail = Mail\
                .query\
                .filter_by(id=draft_id, sender_id=current_user.get_id(), status='draft')\
                .first()
            if draft_mail:
                Mail.query\
                    .filter_by(id=draft_id) \
                    .update(dict(sender_id=sender_id,
                                 recipient_id=recipient_id,
                                 title=title,
                                 text=text,
                                 status=status,
                                 timestamp=datetime.now().isoformat()))
                db.session.commit()
        else:
            mail = Mail(sender_id, recipient_id, title, text, status)
            db.session.add(mail)
            db.session.commit()
        if status is 'sent':
            flash('Mail successfully sent.', 'success')
        else:
            flash('Mail saved to draft.', 'success')
        form = None
    else:
        if not user_exists(form.recipient.data):
            flash('User with username \'%s\' doesn\'t exist.' % form.recipient.data, 'danger')
        else:
            flash('Validation fail.', 'danger')
    return render_template('send-mail.html',
                           title='Send mail',
                           form=form,
                           new_mails=_new_mails_count(),
                           draft_mails=_draft_count())


@app.route('/mail/<int:id>')
@login_required
def mail(id):
    mail = Mail.query.filter_by(id=id, recipient_id=current_user.get_id()).first()
    if not mail:
        flash('Mail doesn\'t exist.', 'danger')
    else:
        Mail.query.filter_by(id=mail.id).update({'viewed': True})
        db.session.commit()
    return render_template('mail.html',
                           title='Mail',
                           new_mails=_new_mails_count(),
                           draft_mails=_draft_count(),
                           mail=mail)


@app.route('/draft')
@app.route('/draft/<int:page>')
@login_required
def draft(page=1):
    total = Mail.query.filter_by(sender_id=current_user.get_id(), status='draft').count()
    mails = Mail.query \
        .filter_by(sender_id=current_user.get_id(), status='draft') \
        .order_by('timestamp DESC') \
        .paginate(page, config.MAIL_PER_PAGE) \
        .items
    pagination = Pagination(page=page, per_page=config.MAIL_PER_PAGE, total=total, bs_version=3)
    return render_template('draft.html',
                           title='Draft',
                           pagination=pagination,
                           new_mails=_new_mails_count(),
                           draft_mails=_draft_count(),
                           mails=mails)
