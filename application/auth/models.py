from application import db
from application.models import Base


class User(Base):
    __tablename__ = "account"
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    role = db.Column(db.String(64))

    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password
        self.role = role

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_role(self):
        return self.role
