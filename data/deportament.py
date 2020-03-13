import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Departments(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, autoincrement=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True)
    members = sqlalchemy.Column(sqlalchemy.String, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
