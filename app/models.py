from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Your User, Employee, Late, Leave models go here
# Employee Model (Example)

class user(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    emp_id=db.Column(db.Integer)
    name=db.Column(db.String(30))
    one=db.Column(db.String(30))
    two=db.Column(db.String(30))
    three=db.Column(db.String(30))
    four=db.Column(db.String(30))
    five=db.Column(db.String(30))
    six=db.Column(db.String(30))
    seven=db.Column(db.String(30))
    eight=db.Column(db.String(30))
    nine=db.Column(db.String(30))
    ten=db.Column(db.String(30))
    eleven=db.Column(db.String(30))
    twelve=db.Column(db.String(30))
    thirteen=db.Column(db.String(30))
    fourteen=db.Column(db.String(30))
    fifteen=db.Column(db.String(30))
    sixteen=db.Column(db.String(30))
    seventeen=db.Column(db.String(30))
    eighteen=db.Column(db.String(30))
    nineteen=db.Column(db.String(30))
    twenty=db.Column(db.String(30))
    tw_one=db.Column(db.String(30))
    tw_two=db.Column(db.String(30))
    tw_three=db.Column(db.String(30))
    tw_four=db.Column(db.String(30))
    tw_five=db.Column(db.String(30))
    tw_six=db.Column(db.String(30))
    tw_seven=db.Column(db.String(30))
    tw_eight=db.Column(db.String(30))
    tw_nine=db.Column(db.String(30))
    thirty=db.Column(db.String(30))
    th_one=db.Column(db.String(30))

    
class notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=db.func.now())
    def __init__(self, message):
        self.message = message

class employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer)
    emp_name = db.Column(db.String(150), nullable=False)

# Late Model (Example)
class late(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer)
    emp_name = db.Column(db.String(150), nullable=False)
    reason = db.Column(db.String(150), nullable=False)
    from_time = db.Column(db.String(150), nullable=False)
    to_time = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), default='Pending')
    hod_approval = db.Column(db.String(150), default='Pending')
    approved_by = db.Column(db.String(150), default='Pending')
    hr_approval = db.Column(db.String(150), default='Pending')
    date = db.Column(db.DateTime(timezone=True), default=func.now())
# Leave Model (Example)
class leave(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer)
    emp_name = db.Column(db.String(150), nullable=False)
    reason = db.Column(db.String(150), nullable=False)
    from_date = db.Column(db.String(150), nullable=False)
    to_date = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), default='Pending')
    hod_approval = db.Column(db.String(150), default='Pending')
    approved_by = db.Column(db.String(150), default='Pending')
    hr_approval = db.Column(db.String(150), default='Pending')
    date = db.Column(db.DateTime(timezone=True), default=func.now())
