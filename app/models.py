from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ProjectInfo(db.Model):
    __tablename__ = 'project_info'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(5))
    device_name = db.Column(db.String(64))
    project_name = db.Column(db.String(64))
    device_com = db.Column(db.String(64))
    # relation_table = db.Column(db.String(64))
    protocol = db.Column(db.String(64))

    def __repr__(self):
        return '<device_id %r>' % self.device_id

    def __getitem__(self, key):
        return self.__dict__[key] if key in self.__dict__ else None

class AnalogInfo(db.Model):
    __tablename__ = 'analog_info'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(5))
    name = db.Column(db.String(64))
    unit = db.Column(db.String(64))
    value_type = db.Column(db.String(64))
    precision = db.Column(db.String(64))
    min_value = db.Column(db.String(64))
    max_value = db.Column(db.String(64))
    ratio = db.Column(db.String(64))
    command = db.Column(db.String(64))
    cmd_param = db.Column(db.String(64))
    cmd_length = db.Column(db.String(2))

    def __getitem__(self, key):
        return self.__dict__[key] if key in self.__dict__ else None

class DigitInfo(db.Model):
    __tablename__ = 'digit_info'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(5))
    name = db.Column(db.String(64))
    ratio = db.Column(db.String(64))
    mapper = db.Column(db.String(64))
    command = db.Column(db.String(64))
    cmd_param = db.Column(db.String(64))
    cmd_length = db.Column(db.String(2))

    def __getitem__(self, key):
        return self.__dict__[key] if key in self.__dict__ else None
