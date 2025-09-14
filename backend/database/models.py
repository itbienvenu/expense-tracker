import uuid
from sqlalchemy import Column, String, Float, Date, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database.dbs import Base


# Association table for many-to-many
transaction_category = Table(
    "transaction_category",
    Base.metadata,
    Column("transaction_id", UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete")
    categories = relationship("Category", back_populates="owner", cascade="all, delete")


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, index=True, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    # relationships
    owner = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", secondary=transaction_category, back_populates="categories")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)   # positive = income, negative = expense
    date = Column(Date, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    # relationships
    owner = relationship("User", back_populates="transactions")
    categories = relationship("Category", secondary=transaction_category, back_populates="transactions")
