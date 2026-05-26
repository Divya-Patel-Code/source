from sqlalchemy import and_
from sqlalchemy.orm import Session
from application.models.connections import Connection
from sqlalchemy.sql import expression


class ConnectionRepository:

    def create(self, db: Session, data: dict) -> Connection:
        connection = Connection(**data)
        db.add(connection)
        db.commit()
        db.refresh(connection)
        return connection

    def get_by_id(self, db: Session, connection_id, user_id):
        return db.query(Connection).filter(and_(Connection.id == connection_id, Connection.user_id == user_id)).first()

    def get_by_id_only(self, db: Session, connection_id):
        return db.query(Connection).filter(expression.true() & (Connection.id == connection_id)).first()

    def get_all(self, db: Session, user_id, page: int = 1, limit: int = 10):
        query = db.query(Connection).filter(expression.true() & Connection.user_id == user_id)

        total = query.count()
        offset = (page - 1) * limit  # How many records to skip
        results = query.offset(offset).limit(limit).all()

        return results, total

    def get_by_provider(self, db: Session, provider_id, user_id):
        return db.query(Connection).filter(
            and_(Connection.provider_id == provider_id, Connection.user_id == user_id)
        ).all()

    def update(self, db: Session, connection: Connection, update_data: dict):
        for key, value in update_data.items():
            setattr(connection, key, value)

        db.commit()
        db.refresh(connection)
        return connection

    def delete(self, db: Session, connection: Connection):
        db.delete(connection)
        db.commit()