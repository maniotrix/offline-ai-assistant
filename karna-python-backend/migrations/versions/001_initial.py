"""Initial migration

Revision ID: 001
Create Date: 2023-10-20
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create cached_commands table
    op.create_table('cached_commands',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('domain', sa.String(), nullable=False),
        sa.Column('is_in_cache', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cached_commands_uuid'), 'cached_commands', ['uuid'], unique=True)
    op.create_index(op.f('ix_cached_commands_name'), 'cached_commands', ['name'], unique=False)
    op.create_index(op.f('ix_cached_commands_domain'), 'cached_commands', ['domain'], unique=False)

    # Create cached_intents table
    op.create_table('cached_intents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('command_uuid', sa.String(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('meta_data', sa.JSON(), nullable=True),  # Changed from metadata to meta_data
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['command_uuid'], ['cached_commands.uuid'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cached_intents_uuid'), 'cached_intents', ['uuid'], unique=True)

    # Create cached_actions table
    op.create_table('cached_actions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('intent_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('coordinates_x', sa.Integer(), nullable=False),
        sa.Column('coordinates_y', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['intent_id'], ['cached_intents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cached_actions_uuid'), 'cached_actions', ['uuid'], unique=True)

def downgrade() -> None:
    op.drop_table('cached_actions')
    op.drop_table('cached_intents')
    op.drop_table('cached_commands')