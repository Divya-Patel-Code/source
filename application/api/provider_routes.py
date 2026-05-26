from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from application.db.dependencies import get_db
from application.schemas.provider_schema import ProviderCreate
from application.services.provider_services import ProviderService
from application.utils.exceptions import AppException
from application.utils.response import success_response

router = APIRouter(prefix="/providers")
service = ProviderService()

@router.post("/")
async def create_provider(data: ProviderCreate, db: Session = Depends(get_db)):
    try:
        provider = service.create_provider(db, data)
        return success_response(provider, "Provider Created Successfully", 201)

    except ValueError as e:
        raise AppException(str(e), 400)

    except Exception as e:
        raise AppException(str(e), 500)

@router.get("/")
async def get_all_providers(db: Session = Depends(get_db)):
    try:
        providers = service.get_all_providers(db)
        return success_response(providers, "All Providers Fetched Successfully", 200)

    except Exception as e:
        raise AppException(f"Failed to fetch providers :- {str(e)}", 500)

@router.get("/{provider_id}")
async def get_provider_by_id(provider_id: UUID, db: Session = Depends(get_db)):
    try:
        provider = service.get_provider_by_id(db, provider_id)
        return success_response(provider, f"Provider with id {provider_id} fetched successfully", 200)

    except ValueError as e:
        raise AppException(str(e), 400)

    except Exception as e:
        raise AppException(f"Failed to get provider : {str(e)}" ,500)

@router.get("/fields/{provider_id}")
async def get_provider_connection_fields(provider_id: UUID, db: Session = Depends(get_db)):
    try:
        provider_fields = service.get_provider_fields(db, provider_id)
        return success_response(provider_fields, f"Provider Fields fetched successfully", 200)

    except ValueError as e:
        raise AppException(str(e), 400)

    except Exception as e:
        raise AppException(f"Failed to get provider fields : {str(e)}", 500)

@router.get("/usecase-fields/{provider_id}")
async def get_provider_usecase_fields(provider_id: UUID, db: Session = Depends(get_db)):
    try:
        provider_usecase_fields = service.get_provider_usecase_fields(db, provider_id)
        return success_response(provider_usecase_fields, f"Provider use case fields fetched successfully", 200)

    except ValueError as e:
        raise AppException(str(e), 400)

    except Exception as e:
        raise AppException(f"Failed to get provider usecase fields : {str(e)}" ,500)