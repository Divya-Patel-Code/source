import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship
from application.db.session import Base


class UseCaseField(Base):
    __tablename__ = "usecase_fields"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False)
    is_required = Column(Boolean, default=False)
    type = Column(String, nullable=False)
    depends_on = Column(String, nullable=True, default=None)

    min = Column(Integer, default=-1)
    max = Column(Integer, default=-1)

    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"))

    provider = relationship("Provider", back_populates="use_case_fields")