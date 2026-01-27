from typing import Optional, List, Text

from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_image: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    like_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # 관계 설정
    author: Mapped["User"] = relationship(back_populates="posts")
    liked_by: Mapped[List["Like"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")

class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # 관계 설정
    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="liked_by")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")