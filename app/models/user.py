from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Integer, default=0)  # 0 = normal user, 1 = admin (e.g. a librarian)

    # This lets us do user.borrow_records to get everything this user has borrowed
    borrow_records = relationship("BorrowRecord", back_populates="user")