from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.expression import func


from app.database.db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False, index=True)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False,
                        server_default=func.now())
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
