from sqlalchemy import Column, Integer,ForeignKey


from database.db import Base

class Like(Base):
    __tablename__ ="likes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
