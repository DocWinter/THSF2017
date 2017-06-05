from radio import db

class Rpi(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	ip = db.Column(db.String(80), unique=True)
	ps = db.Column(db.String(8))
	rt = db.Column(db.String(64))
	ta = db.Column(db.Boolean())

	def __init__(self, name, ip, ps='', rt='', ta=True):
		self.name, self.ip = name, ip
		self.ps, self.rt, self.ta = ps, rt, ta

	def __rpr__(self):
		return f'<Rpi {self.name} - {self.ip}>'
