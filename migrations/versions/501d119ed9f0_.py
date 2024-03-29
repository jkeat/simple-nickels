"""empty message

Revision ID: 501d119ed9f0
Revises: None
Create Date: 2015-07-25 14:54:52.874354

"""

# revision identifiers, used by Alembic.
revision = '501d119ed9f0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text(u'now()'), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('confirmed_email', sa.Boolean(), nullable=True),
    sa.Column('passhash', sa.String(length=255), nullable=True),
    sa.Column('is_oauth_user', sa.Boolean(), nullable=True),
    sa.Column('twitter_username', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('twitter_username'),
    sa.UniqueConstraint('username')
    )
    op.create_table('wallets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickels', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallets')
    op.drop_table('users')
    ### end Alembic commands ###
