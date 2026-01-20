from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Post(Base):
    __tablename__ = "posts"

    postId = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    userId = Column(Integer, ForeignKey("users.userId", ondelete="CASCADE"), nullable=False, index=True)
    viewCount = Column(Integer, nullable=False, default=0)
    likeCount = Column(Integer, nullable=False, default=0)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # 관계 설정
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(postId={self.postId}, title={self.title}, userId={self.userId})>"
