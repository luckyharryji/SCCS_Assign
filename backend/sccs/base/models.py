import datetime

from peewee import MySQLDatabase, Model, PrimaryKeyField, DateTimeField

from .. import settings

def get_database(options):
    return MySQLDatabase(**options)

db = get_database(settings.DATABASE_OPTIONS)

class BaseModel(Model):
    '''
    basic databse model including connection to be inheried by subclass model
    '''
    id = PrimaryKeyField(primary_key = True)
    created_date = DateTimeField(default = datetime.datetime.now)

    class Meta:
        database = db
