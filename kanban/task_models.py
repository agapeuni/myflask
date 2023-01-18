from kanban import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(200), nullable=False, default="PLAN")
    priority = db.Column(db.Integer, nullable=False, default=1)
    contents = db.Column(db.Text(), nullable=False)
