from flask_wtf import Form
from wtforms import BooleanField, StringField
from wtforms.validators import Length

class RpiForm(Form):
	name = StringField('Name')
	ip = StringField('Ip Address')
	ps = StringField('Program Service', [Length(min=0, max=8)])
	rt = StringField('Radio Text', [Length(min=0, max=64)])
	ta = BooleanField('Traffic Announcement')
