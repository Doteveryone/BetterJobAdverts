from jobcert import db

class Publisher(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    domain = db.Column(db.String(80), unique=True)
    white_listed = db.Column(db.Boolean())

    def __init__(self, username, email):
        self.name = name
        self.domain = domain

    def __repr__(self):
        return '<Publisher %r %r>' % (self.name, self.domain)