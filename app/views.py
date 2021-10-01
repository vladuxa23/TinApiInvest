import os

from flask import url_for, redirect, render_template, flash, g, session
from app import app, db


@app.route('/')
def index():
	if not os.path.exists('app/capital.db'):
		print("БД создана")
		db.create_all()

	return "<h1>INDEX1</h1>"
