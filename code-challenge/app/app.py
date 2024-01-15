#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db,Power

import os

cwd=os.getcwd()

db_dir=f'sqlite:////{cwd}/db/app.db'

print(db_dir)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bonganimasemola/Development/coding/PHASE4/python-code-challenge-superheroes/code-challenge/app/db/app.db'
app.config['SQLALCHEMY_DATABASE_URI'] =db_dir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''


if __name__ == '__main__':
    app.run(port=5555)
