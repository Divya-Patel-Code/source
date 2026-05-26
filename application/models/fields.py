import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from application.db.session import Base


class Field(Base):
    __tablename__ = "fields"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    key = Column(String, nullable=True)
    is_required = Column(Boolean, default=False)
    type = Column(String, nullable=False)
    min = Column(Integer, default=-1)
    max = Column(Integer, default=-1)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"))

    provider = relationship("Provider", back_populates="fields")