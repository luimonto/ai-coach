from fastapi import APIRouter, Depends

from app.core.dependencies import get_activity_sync_service
from app.schemas.activity_sync import ActivitySyncRequest, ActivitySyncResponse
from app.services.activity_sync_service import ActivitySyncService


router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post("/sync", response_model=ActivitySyncResponse)
def sync_activities(
    request: ActivitySyncRequest,
    service: ActivitySyncService = Depends(get_activity_sync_service),
) -> ActivitySyncResponse:
    return service.sync(
        external_id=request.external_id,
        activities=request.activities,
    )
