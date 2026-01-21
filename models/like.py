from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Like(Base):
    __tablename__ = "likes"

    likeId = Column(Integer, primary_key=True, autoincrement=True)
    postId = Column(Integer, ForeignKey("posts.postId", ondelete="CASCADE"), nullable=False, index=True)
    userId = Column(Integer, ForeignKey("users.userId", ondelete="CASCADE"), nullable=False, index=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())

    # 관계 설정
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")

    # 한 사용자가 같은 게시글에 중복 좋아요 방지
    __table_args__ = (
        UniqueConstraint('postId', 'userId', name='uix_post_user'),
    )

    def __repr__(self):
        return f"<Like(likeId={self.likeId}, postId={self.postId}, userId={self.userId})>"
