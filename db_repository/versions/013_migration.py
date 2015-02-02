from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
association = Table('association', pre_meta,
    Column('id_user', Integer, primary_key=True, nullable=False),
    Column('id_answer', Integer, primary_key=True, nullable=False),
    Column('estimate', Integer),
)

answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=512), nullable=False),
    Column('date_reply', DateTime),
    Column('rating', Integer),
    Column('id_question', Integer),
    Column('id_user', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['association'].drop()
    post_meta.tables['answer'].columns['id_user'].create()
    post_meta.tables['answer'].columns['rating'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['association'].create()
    post_meta.tables['answer'].columns['id_user'].drop()
    post_meta.tables['answer'].columns['rating'].drop()
