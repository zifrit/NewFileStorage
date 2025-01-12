"""add files table

Revision ID: fffaf6db8c2f
Revises: 
Create Date: 2024-12-04 15:40:30.900126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fffaf6db8c2f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('file_size', sa.Integer(), nullable=False, comment='File size in bytes'),
    sa.Column('file_path', sa.String(length=255), nullable=False, comment='The relative path to the file'),
    sa.Column('file_format', sa.String(length=255), nullable=False, comment='The file format'),
    sa.Column('file_old_name', sa.String(length=255), nullable=False, comment='The old name of the file'),
    sa.Column('file_new_name', sa.String(length=255), nullable=False, comment='The new name of the file'),
    sa.Column('file_extension', sa.String(length=255), nullable=False, comment='The file extension'),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    # ### end Alembic commands ###
