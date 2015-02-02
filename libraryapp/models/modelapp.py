# -*- coding: utf-8 -*-

from libraryapp import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password = db.Column(db.String(64))
    date_registration = db.Column(db.DateTime)
    question = db.relationship('Question', backref='author', lazy='dynamic')
    answer = db.relationship('Answer', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, nullable=False, unique=True)
    date_post = db.Column(db.DateTime)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer = db.relationship('Answer', backref='questions', lazy='dynamic')

    def __repr__(self):
        return '<Question %r>' % (self.title)


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(512), index=True, nullable=False, unique=True)
    date_reply = db.Column(db.DateTime)
    estimate = db.Column(db.Boolean)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Answer %r>' % (self.body)
