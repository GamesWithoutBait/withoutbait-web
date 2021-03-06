import flask
from typing import Iterable, Type
import sqlalchemy as sa
from sqlalchemy import orm, MetaData
from sqlalchemy.engine import Engine
import sqlalchemy_utils as sa_utils

from app import app, config
from .base import Base as CustomBase


meta = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
})

Base: Type[CustomBase] = orm.declarative_base(cls=CustomBase, metadata=meta)
engine: Engine = sa.create_engine(config.DB_URI)
_Session = orm.sessionmaker(bind=engine, autoflush=False)

app.session = orm.scoped_session(_Session, scopefunc=flask._app_ctx_stack.__ident_func__)

@app.teardown_appcontext
def close_sessions(exception=None):
    app.session.remove()


if not sa_utils.database_exists(engine.url):
    sa_utils.create_database(engine.url)

def default_value(value):
    return {
        'default': value,
        'server_default': sa.sql.expression.literal(value),
        'nullable': False,
    }


def upcreate(type, values: dict, match=None, default=None, session=None):
    session = session or app.session
    if match:
        if match is True:
            match = values.keys()
        if isinstance(match, str):
            match = [match]
        obj = session.query(type).filter_by(**{x: values[x] for x in match}).first()
        if obj:
            for k, v in values.items():
                setattr(obj, k, v)
            return obj
    obj = type(**values)
    if default:
        for k, v in default.items():
            setattr(obj, k, v)
    session.add(obj)
    return obj


def commit(session=None):
    (session or app.session).commit()


def add(*objs, session=None, save=False):
    session = session or app.session
    for obj in objs:
        session.add(obj)
    if save:
        commit(session=session)

session = app.session

from .mixins import IdMixin, SlugMixin, CreatedMixin, TimedMixin
