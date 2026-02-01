"""create job view table

Revision ID: 05ee05e08e85
Revises: 9e3f995a1af1
Create Date: 2026-01-12 15:45:40.150375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from typing import Text


# revision identifiers, used by Alembic.
revision: str = '05ee05e08e85'
down_revision: Union[str, None] = '9e3f995a1af1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



#    """Upgrade schema."""
def upgrade(): 
    op.create_table( "job_views", 
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False), 
                    sa.Column("job_id", sa.Integer, sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), 
                    sa.Column("viewed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                    sa.UniqueConstraint("job_id", "user_id", name="uq_job_user_view") ) 




#    """Downgrade schema."""
def downgrade(): 
    op.drop_table("job_views")