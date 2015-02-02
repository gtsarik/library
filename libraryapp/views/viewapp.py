# -*- coding: utf-8 -*-

import datetime
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from libraryapp.forms.forms import LoginForm, RegistrationForm, AskQuestionForm, AnswerForm
from libraryapp import app, login_manager
from libraryapp.models.modelapp import User, Question, Answer
from libraryapp import app, db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.before_request
def before_request():
    g.user = current_user


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/')
@app.route('/index')
def index():
    posts = []
    element = {}
    questions = Question.query.all()
    session['page'] = 'index'

    for question in questions:
        for user in User.query.filter_by(id=question.id_user):
            element['autor'] = user.nickname
        element['question'] = question.title
        posts.append(element)
        element = {}

    return render_template("index.html",
        title=u'Главная',
        user=g.user,
        posts=posts)


def checkQuestionTitle(question):
    query_question = Question.query.filter_by(title=question)
    id_question = False

    for q in query_question:
        id_question = True

    return id_question


@app.route('/send_ajax', methods=['GET','POST'])
def send_ajax():
    id_answer = request.form.getlist('id')
    question = request.form.getlist('question')

    for n in id_answer:
        id_answer = n

    for n in request.form.getlist('question'):
        question = n

    for n in request.form.getlist('estimate'):
        estimate = n and True or False

    query_question = Question.query.filter_by(title=question).first()
    question_id = query_question.id
    answer = Answer.query.filter_by(id=id_answer).first()
    answer.estimate = estimate
    answer.id_question = question_id
    db.session.commit()

    return jsonify({'key': 'success'})


@app.route('/qa', methods=["GET", "POST"])
@app.route("/qa/<question>", methods=["GET", "POST"])
def qa(question=None):
    session['page'] = 'qa'

    if question is not None:
        session['question'] = question

    form = AnswerForm(request.form)
    now_datetime = datetime.datetime.now()
    answer_title = []
    answer_all = []
    answers = []
    answer = {}
    id_question = -1
    question = unicode(session['question'])
    is_check = False

    if not checkQuestionTitle(question):
        question = question + u'?'

    query_question = Question.query.filter_by(title=question).first()
    answer_all = Answer.query.filter_by(id_question=query_question.id).all()
    id_question = unicode(query_question.id)

    for an in answer_all:
        answer['id'] = an.id
        answer['body'] = an.body

        for n in User.query.filter_by(id=an.id_user):
            answer['autor'] = n.nickname

        if an.estimate and an.estimate is not None:
            answer['estimate'] = an.estimate
        else:
            answer['estimate'] = False

        answers.append(answer)
        answer = {}

    if id_question != -1:
        if request.method == 'POST' and form.validate():
            answer_form = Answer(body=form.body.data,
                        date_reply=now_datetime,
                        id_question=id_question,
                        id_user=g.user.get_id())

            db.session.add(answer_form)
            db.session.commit()
            flash(u'%s, Ваш ответ отправлен' % g.user.nickname)
            
            return redirect(url_for('qa'))
   
    return render_template('qa.html',
        question=question,
        answers=answers,
        form=form)


@app.route('/ask_question', methods=["GET", "POST"])
def ask_question():
    form = AskQuestionForm(request.form)
    now_datetime = datetime.datetime.now()
    id_user = g.user.get_id()
    session['page'] = 'ask_question'

    if request.method == 'POST' and form.validate():
        question = Question(title=form.question.data,
                    date_post=now_datetime,
                    id_user=id_user)
        db.session.add(question)
        db.session.commit()
        flash(u'%s, Ваш вопрос отправлен' % g.user.nickname)
        return redirect(url_for('index'))

    return render_template('ask_question.html',
        title=u'Задать вопрос',
        form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        print 'LOGIN'
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    if form.validate_on_submit():
        remember_me = form.remember_me.data

        g.user = User.query.filter_by(
            nickname=form.login.data,
            password=form.password.data).first()

        if g.user != None:
            if g.user.is_authenticated():
                login_user(g.user, remember=remember_me)
                flash(u"Вы вошли как %s" % g.user.nickname)
                
                return redirect(url_for('index'))
        else:
            flash(u"Неправильный Логин или Пароль! Попробуйте еще раз")
            return redirect(url_for('login'))

    return render_template('login.html',
        title=u'Войти в Систему',
        form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    now_datetime = datetime.datetime.now()
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User(nickname=form.username.data,
                    password=form.password.data,
                    date_registration=now_datetime)
        db.session.add(user)
        db.session.commit()
        flash(u'Спасибо за регистрацию')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
