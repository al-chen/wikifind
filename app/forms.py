from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class WikiForm(Form):
    first = StringField('first', validators=[DataRequired()])
    second = StringField('second', validators=[DataRequired()])