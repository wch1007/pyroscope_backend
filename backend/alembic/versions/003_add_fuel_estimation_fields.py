"""Add fuel estimation fields

Revision ID: 003
Revises: 002
Create Date: 2026-02-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Modify fuel_load column from String to DECIMAL
    op.alter_column(
        'scan_records',
        'fuel_load',
        type_=sa.DECIMAL(10, 4),
        existing_type=sa.String(20),
        nullable=True
    )
    
    # Add new fuel estimation fields
    op.add_column('scan_records', sa.Column('one_hour_fuel', sa.DECIMAL(10, 4), nullable=True))
    op.add_column('scan_records', sa.Column('ten_hour_fuel', sa.DECIMAL(10, 4), nullable=True))
    op.add_column('scan_records', sa.Column('hundred_hour_fuel', sa.DECIMAL(10, 4), nullable=True))
    op.add_column('scan_records', sa.Column('pine_cone_count', sa.Integer(), nullable=True))


def downgrade() -> None:
    # Remove new fields
    op.drop_column('scan_records', 'pine_cone_count')
    op.drop_column('scan_records', 'hundred_hour_fuel')
    op.drop_column('scan_records', 'ten_hour_fuel')
    op.drop_column('scan_records', 'one_hour_fuel')
    
    # Revert fuel_load back to String
    op.alter_column(
        'scan_records',
        'fuel_load',
        type_=sa.String(20),
        existing_type=sa.DECIMAL(10, 4),
        nullable=True
    )
