from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, MacAddress

class FirePut(FlaskForm):
    macaddr = StringField('macaddr', validators=[MacAddress()])
    fwname = StringField('fwname', validators=[DataRequired()])
    comment = StringField('comment', validators=[DataRequired()])
