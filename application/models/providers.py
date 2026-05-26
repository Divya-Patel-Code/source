import uuid
import enum
from sqlalchemy.orm import relationship
from application.db.session import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, JSON, Enum

class ProviderStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Provider(Base):
    __tablename__ = "providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, unique=True, nullable=False)
    value = Column(String, unique=True, nullable=False)
    type = Column(JSON, nullable=True)
    img_url = Column(String, nullable=True)
    status = Column(Enum(ProviderStatus), default=ProviderStatus.INACTIVE)

    fields = relationship("Field", back_populates="provider", cascade="all, delete")
    connections = relationship("Connection", back_populates="provider", cascade="all, delete")
    use_case_fields = relationship("UseCaseField", back_populates="provider", cascade="all, delete")