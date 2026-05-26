import uuid
from datetime import datetime
import enum
from application.db.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Enum, UniqueConstraint


class ConnectionStatus(str, enum.Enum):
    ACTIVE = "active"
    FAILED = "failed"
    INACTIVE = "inactive"


class Connection(Base):
    __tablename__ = "connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False, index=True)

    config = Column(JSON, nullable=False)
    status = Column(Enum(ConnectionStatus), default=ConnectionStatus.ACTIVE)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    provider = relationship("Provider", back_populates="connections")

    # __table_args__ = (
    #     UniqueConstraint("user_id", "name", name="uq_user_connection_name"),
    # )