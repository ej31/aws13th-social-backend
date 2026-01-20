from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    tokenId = Column(Integer, primary_key=True, autoincrement=True)
    tokenHash = Column(String(255), unique=True, nullable=False, index=True)
    userId = Column(Integer, ForeignKey("users.userId", ondelete="CASCADE"), nullable=False, index=True)
    expiresAt = Column(DateTime, nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())

    # 관계 설정
    user = relationship("User", back_populates="refresh_tokens")

    def __repr__(self):
        return f"<RefreshToken(tokenId={self.tokenId}, userId={self.userId})>"
