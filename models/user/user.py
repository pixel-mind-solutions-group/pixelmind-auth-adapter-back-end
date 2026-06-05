from sqlalchemy import Column, DateTime, Integer, String, Boolean
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, nullable=False)

    firstName = Column("first_name", String, nullable=False)
    lastName = Column("last_name", String, nullable=False)

    username = Column("username", String, nullable=False)

    active = Column("active", Boolean, nullable=False, default=False)

    emailVerified = Column("email_verified", Boolean, nullable=False)

    failCount = Column("fail_count", Integer, nullable=False)

    createdBy = Column("created_by", String, nullable=False)
    createdAt = Column("created_at", DateTime, nullable=False)

    updatedBy = Column("updated_by", String)
    updatedAt = Column("updated_at", DateTime)
