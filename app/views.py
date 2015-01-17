from flask import render_template
from app import app
from .forms import WikiForm
import find
import best_search

@app.route('/', methods=['GET', 'POST'])
def index():
	form = WikiForm()
	path = []
	if form.validate_on_submit():
		u1 = form.first.data
		u2 = form.second.data
		dic1 = {u1: None}
		dic2 = {"None": u2}
		path, depth = best_search.best_search(u1, u2)
	return render_template('index.html',
							title="WikiFind",
							form=form,
							boo=form.validate_on_submit(),
							path=path)
