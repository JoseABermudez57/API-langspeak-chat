from fastapi import APIRouter

from src.application.dtos.responses.base_response import BaseResponse

router = APIRouter()


@router.get("/v1", response_model=BaseResponse)
async def health():
    return BaseResponse(data=None, message="Service is running", status_code=200, success=True, http_status="OK")
