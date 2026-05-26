from sqlalchemy.orm import Session
from application.utils.exceptions import AppException
from application.utils.dynamic_validator import validate_config
from application.connectors.connector_factory import ConnectorFactory
from application.repositories.provider_repository import ProviderRepository
from application.repositories.connection_repository import ConnectionRepository


class ConnectionService:
    def __init__(self):
        self.connection_repo = ConnectionRepository()
        self.provider_repo = ProviderRepository()

    def create_connection(self, db: Session, data, user_id):
        self.test_connections(db, data)

        payload = {
            "user_id": user_id,
            "provider_id": data.provider_id,
            "config": data.config,
            "status": "active"
        }

        return self.connection_repo.create(db, payload)

    def update_connection(self, db: Session, connection_id, data, user_id):
        connection = self.connection_repo.get_by_id(db, connection_id, user_id)

        if not connection:
            raise AppException("Connection not found", 404)

        provider = self.provider_repo.get_by_id(db, connection.provider_id)

        if data.config:
            validate_config(provider.fields, data.config)

            connector = ConnectorFactory.get_connector(provider, data.config)
            connector.test_connection()

        return self.connection_repo.update(db, connection, data.dict(exclude_unset=True))

    def get_all_connections(self, db: Session, user_id, page: int, limit: int):
        results, total = self.connection_repo.get_all(db, user_id = user_id, page = page, limit = limit)

        providers = self.provider_repo.get_all_providers(db)
        provider_map = {provider.id: provider for provider in providers}

        formatted = []

        for connection in results:
            provider = provider_map.get(connection.provider_id)

            formatted.append({
                "id": connection.id,
                "user_id": connection.user_id,
                "provider": {
                    "id": provider.id,
                    "title": provider.title,
                    "value": provider.value,
                    "image_url": provider.img_url
                },
                "config": connection.config,
                "status": connection.status,
                "created_at": connection.created_at.isoformat() if connection.created_at else None,
                "updated_at": connection.updated_at.isoformat() if connection.updated_at else None
            })

        return formatted, total

    def get_connection_by_id(self, db: Session, connection_id, user_id):
        return self.connection_repo.get_by_id(db, connection_id, user_id)

    def delete_connection(self, db: Session, connection_id, user_id):
        connection = self.connection_repo.get_by_id(db, connection_id, user_id)

        if not connection:
            raise AppException("Connection not found", 404)

        self.connection_repo.delete(db, connection)
        return {"message": "Connection deleted successfully"}

    def test_connections(self, db: Session, data):
        provider = self.provider_repo.get_by_id(db, data.provider_id)

        if not provider:
            raise AppException("Provider Not Found", 404)

        validate_config(provider.fields, data.config)
        connector = self.build_connector(db, data.config)
        return connector.test_connection()

    def build_connector(self, db: Session, connection_id):
        connection = self.connection_repo.get_by_id_only(db, connection_id)
        provider = self.provider_repo.get_by_id(db, connection.provider_id)

        if not provider:
            raise AppException("Provider Not Found", 404)

        config = connection.config
        validate_config(provider.fields, config)
        return ConnectorFactory.get_connector(provider, config)