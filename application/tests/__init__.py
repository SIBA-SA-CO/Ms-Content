from flask_sqlalchemy import SQLAlchemy
from  application import create_app,db
from ..models import db
import unittest



class BaseTestClass(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()

    def tearDown(self):
        # Elimina todas las tablas de la base de datos# Elimina todas las tablas de la base de datos
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()



