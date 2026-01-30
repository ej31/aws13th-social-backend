from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.models.post import Post
from db.models.user import User


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uq_likes_post_user"),
    )

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    post_id: Mapped[str] = mapped_column(
        String(40),
        ForeignKey("posts.id", ondelete="CASCADE"),
        index=True
    )
    user_id: Mapped[str | None] = mapped_column(
        String(40),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped[User] = relationship(back_populates="likes", lazy="noload")
    post: Mapped[Post] = relationship(back_populates="likes", lazy="noload")
