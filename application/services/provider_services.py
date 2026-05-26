from dataclasses import fields
from uuid import UUID
from sqlalchemy.orm import Session
from application.repositories.provider_repository import ProviderRepository


class ProviderService:
    def __init__(self):
        self.repo = ProviderRepository()

    def create_provider(self, db: Session, data):
        existing_provider = self.repo.get_by_name(db, data.title, data.value)

        if existing_provider:
            raise ValueError("Provider Already Exists")

        provider = self.repo.create(db, data)

        return {
            "id": provider.id,
            "title": provider.title,
            "value": provider.value,
            "img_url": provider.img_url,
            "type": provider.type,
            "status": provider.status,
            "fields": provider.fields,
            "use_case_fields": provider.use_case_fields
        }

    def get_provider_by_id(self, db: Session, provider_id: UUID):
        provider = self.repo.get_by_id(db, provider_id)

        if not provider:
            raise ValueError("Provider not found")

        return {
            "id": provider.id,
            "title": provider.title,
            "value": provider.value,
            "img_url": provider.img_url,
            "type": provider.type,
            "status": provider.status
        }

    def get_all_providers(self, db: Session):
        providers = self.repo.get_all_providers(db)

        result = []

        for provider in providers:
            result.append({
                "id": provider.id,
                "title": provider.title,
                "value": provider.value,
                "img_url": provider.img_url,
                "type": provider.type,
                "status": provider.status
            })

        return result

    def get_provider_fields(self, db: Session, provider_id: UUID):
        fields = self.repo.get_fields_by_provider_id(db, provider_id)

        if not fields:
            raise ValueError("No fields found for this provider")

        result = []

        for field in fields:
            result.append({
                "id": field.id,
                "name": field.name,
                "key": field.key,
                "is_required": field.is_required,
                "type": field.type,
                "min": field.min,
                "max": field.max
            })

        return result

    def get_provider_usecase_fields(self, db: Session, provider_id: UUID):
        usecase_fields = self.repo.get_usecase_fields_by_provider_id(db, provider_id)

        if not usecase_fields:
            raise ValueError("No use case fields found for this provider")

        result = []

        for usecase_field in usecase_fields:
            result.append({
                "id": usecase_field.id,
                "name": usecase_field.name,
                "key": usecase_field.key,
                "is_required": usecase_field.is_required,
                "type": usecase_field.type,
                "depends_on": usecase_field.depends_on,
                "min": usecase_field.min,
                "max": usecase_field.max
            })

        return result