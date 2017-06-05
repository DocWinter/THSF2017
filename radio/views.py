from flask import render_template, redirect, url_for

from . import app, db
from .forms import RpiForm
from .models import Rpi


def update_rpi(rpi):
	s = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
	s.connect(dict(rpi.ip.split[':']))
	s.send('PS {}'.format(rpi.ps).decode('utf8'))
	s.send('RT {}'.format(rpi.rt).decode('utf8'))
	if rpi.ta:
		s.send('TA on')
	else:
		s.send('TA off')
	s.close()



@app.route('/', methods=['GET', 'POST'])
def index():
	rpis = Rpi.query.all()
	form = RpiForm()
	if form.validate_on_submit():
		for rpi in rpis:
			rpi.ps = form.ps.data
			rpi.rt = form.rt.data
			rpi.ta = form.ta.data
			db.session.commit()
			rpis = Rpi.query.all()
			for rpi in rpis:
				update_rpi(rpi)
	return render_template('index.html', form=form, rpis=rpis)


@app.route('/rpis', methods=['GET', 'POST'])
def rpis():
	form = RpiForm()
	errors = []
	if form.validate_on_submit():
		name, ip = form.name.data, form.ip.data
		if Rpi.query.filter_by(name=name).first() is not None:
			errors.append('Name is already in use')
		if Rpi.query.filter_by(ip=ip).first() is not None:
			errors.append('Ip is already in use')
		if errors == []:
			rpi = Rpi(form.name.data, form.ip.data,
					  form.ps.data, form.rt.data, form.ta.data
					 )
			db.session.add(rpi)
			db.session.commit()
			return redirect(url_for('index'))
	return render_template('rpis.html', form=form, errors=errors)


@app.route('/rpi/<int:rpi_id>', methods=['GET', 'POST'])
def rpi(rpi_id):
	rpi = Rpi.query.filter_by(id=rpi_id).first()
	errors = []
	if rpi is None:
		return redirect(url_for('index'))

	form = RpiForm()
	form.name.data = rpi.name
	form.ip.data = rpi.ip
	form.ps.data = rpi.ps
	form.rt.data = rpi.rt
	form.ta.data = rpi.ta

	if form.validate_on_submit():
		name, ip = form.name.data, form.ip.data
		if name != rpi.name and Rpi.query.filter_by(name=name).first() is not None:
			errors.append('Name is already in use')
		if ip != rpi.ip and Rpi.query.filter_by(ip=ip).first() is not None:
			errors.append('Ip is already in use')
		if errors == []:
			rpi.name = form.name.data
			rpi.ip = form.ip.data
			rpi.ps = form.ps.data
			rpi.rt = form.rt.data
			rpi.ta = form.ta.data
			db.session.commit()
			update_rpi(rpi)
			return redirect(url_for('index'))
	return render_template('rpis.html', form=form, rpi=rpi, errors=errors)


@app.route('/rpi/<int:rpi_id>/del')
def delete_rpi(rpi_id):
	rpi = Rpi.query.filter_by(id=rpi_id).first()
	db.session.delete(rpi)
	db.session.commit()
	return redirect(url_for('index'))
