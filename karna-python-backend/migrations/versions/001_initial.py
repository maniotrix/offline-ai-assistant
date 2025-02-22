"""Initial migration

Revision ID: 001
Create Date: 2025-02-20
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

    # Create cached_intents table with actions as JSON
    op.create_table('cached_intents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('command_uuid', sa.String(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('meta_data', sa.JSON(), nullable=True),
        sa.Column('actions', sa.JSON(), nullable=False),  # New column for storing actions
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['command_uuid'], ['cached_commands.uuid'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cached_intents_uuid'), 'cached_intents', ['uuid'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_cached_intents_uuid'), table_name='cached_intents')
    op.drop_table('cached_intents')
    op.drop_index(op.f('ix_cached_commands_domain'), table_name='cached_commands')
    op.drop_index(op.f('ix_cached_commands_name'), table_name='cached_commands')
    op.drop_index(op.f('ix_cached_commands_uuid'), table_name='cached_commands')
    op.drop_table('cached_commands')