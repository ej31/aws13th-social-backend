from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Comment(Base):
    __tablename__ = "comments"

    commentId = Column(Integer, primary_key=True, autoincrement=True)
    postId = Column(Integer, ForeignKey("posts.postId", ondelete="CASCADE"), nullable=False, index=True)
    userId = Column(Integer, ForeignKey("users.userId", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())

    # 관계 설정
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment(commentId={self.commentId}, postId={self.postId}, userId={self.userId})>"
