from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression
from application.models.fields import Field
from application.models.providers import Provider
from application.models.usecase_fields import UseCaseField


class ProviderRepository:
    def create(self, db: Session, data):
        provider = Provider(
            title = data.title,
            value = data.value,
            type = data.type,
            img_url = data.img_url,
            status = data.status
        )

        db.add(provider)
        db.flush()

        for field in data.fields:
            db_field = Field(
                name=field.name,
                key=field.key,
                is_required=field.isRequired,
                type=field.type,
                min=field.min,
                max=field.max,
                provider_id=provider.id
            )
            db.add(db_field)

        for f in data.use_case_fields:
            field = UseCaseField(
                name=f.name,
                key=f.key,
                is_required=f.isRequired,
                type=f.type,
                min=f.min,
                max=f.max,
                depends_on=f.depends_on,
                provider_id=provider.id
            )
            db.add(field)

        db.commit()
        db.refresh(provider)

        return provider

    def get_by_name(self, db: Session, title: str, value: str):
        return db.query(Provider).filter(
            expression.true() &
            (Provider.title == title) & (Provider.value == value)
        ).first()

    def get_all_providers(self, db: Session):
        return db.query(Provider).all()

    def get_by_id(self, db: Session, provider_id: UUID):
        return db.query(Provider).filter(
            expression.true() &
            (Provider.id == provider_id)
        ).first()

    def get_fields_by_provider_id(self, db: Session, provider_id: UUID):
        return db.query(Field).filter(
            expression.true() &
            (Field.provider_id == provider_id)
        ).all()

    def get_usecase_fields_by_provider_id(self, db: Session, provider_id: UUID):
        return db.query(UseCaseField).filter(
            expression.true() &
            (UseCaseField.provider_id == provider_id)
        ).all()