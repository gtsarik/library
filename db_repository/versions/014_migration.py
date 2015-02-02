from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer = Table('answer', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String),
    Column('date_reply', DateTime),
    Column('id_question', Integer),
    Column('id_user', Integer),
    Column('rating', Integer),
)

answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=512), nullable=False),
    Column('date_reply', DateTime),
    Column('estimate', Boolean),
    Column('id_question', Integer),
    Column('id_user', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answer'].columns['rating'].drop()
    post_meta.tables['answer'].columns['estimate'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answer'].columns['rating'].create()
    post_meta.tables['answer'].columns['estimate'].drop()
