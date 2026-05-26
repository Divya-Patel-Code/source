from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from application.db.dependencies import get_db
from application.schemas.connection_schema import ConnectionCreate, ConnectionUpdate
from application.services.connection_services import ConnectionService
from application.utils.auth_dependencies import get_current_user
from application.utils.exceptions import AppException
from application.utils.response import success_response

router = APIRouter(prefix = "/connections")
service = ConnectionService()

@router.post("/test")
def test_connection_api(data: ConnectionCreate, db: Session = Depends(get_db)):
    try:
        connection = service.test_connections(db, data)

        return success_response(
            data = {"Connected": connection},
            message = "Connected Successfully"
        )

    except AppException as e:
        raise e

    except Exception as e:
        raise AppException(str(e), 500)

@router.post("/create")
def create_connection_api(
    data: ConnectionCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = UUID(current_user["user_id"])
        connection = service.create_connection(db, data, user_id)
        return success_response(
            code=201,
            data = {"connection_id": connection.id},
            message = "Connection Created Successfully"
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e), 500)

@router.get("/")
def get_all_connection_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = UUID(current_user["user_id"])
        connections, total = service.get_all_connections(db, user_id, page, limit)
        return success_response(
            data = {"connections": connections, "total": total},
            message = "Connections Fetched Successfully"
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e), 500)

@router.get("/{id}")
def get_connection_by_id_api(
    id: UUID, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = UUID(current_user["user_id"])
        connection = service.get_connection_by_id(db, id, user_id)
        if not connection:
            raise AppException("Connection not found", 404)
            
        return success_response(
            data = {"connection": connection},
            message = "Connection Fetched Successfully"
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e), 500)

@router.put("/{id}")
def update_connection_api(
    id: UUID, 
    data: ConnectionUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = UUID(current_user["user_id"])
        connection = service.update_connection(db, id, data, user_id)
        return success_response(
            data = {"connection_id": connection.id},
            message = "Connection Updated Successfully"
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e), 500)

@router.delete("/{id}")
def delete_connection_api(
    id: UUID, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = UUID(current_user["user_id"])
        result = service.delete_connection(db, id, user_id)
        return success_response(
            data = result,
            message = "Connection Deleted Successfully"
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e), 500)