# -*- coding:utf-8 -*-

from flask_migrate import Migrate
from app import app
from database.exts import db

migrate = Migrate(app, db)
