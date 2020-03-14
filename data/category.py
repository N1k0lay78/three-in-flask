import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    association_table = sqlalchemy.Table('jobs_to_category', SqlAlchemyBase.metadata,
                                         sqlalchemy.Column('news', sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('jobs.id')),
                                         sqlalchemy.Column('category', sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('category.id')))
