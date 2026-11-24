from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001"


def upgrade():
    op.add_column(
        "links",
        sa.Column("category", sa.String(60), server_default="Без категории", nullable=False),
    )


def downgrade():
    op.drop_column("links", "category")
