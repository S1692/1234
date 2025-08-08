import httpx
import os
from fastapi import APIRouter, HTTPException, status
from app.domain.schemas import SignUpRequest

router = APIRouter(
    prefix="/api/v1/companies",
    tags=["Company"],
)

# Use an environment variable for the downstream service URL for flexibility.
# Default to the example value from the prompt if not set.
COMPANY_SERVICE_URL = os.getenv("COMPANY_SERVICE_URL", "http://company-service:8080/internal/api/companies")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_company(request_data: SignUpRequest):
    """
    Receives sign-up data, logs it, and forwards it to the downstream company-service.
    """
    # Critical Step 1: Log the validated request data.
    # .model_dump_json() is the Pydantic v2 equivalent of .json()
    print(f"Gateway received signup request: {request_data.model_dump_json(indent=2)}")

    # Step 2: Forward the validated request to the 'company-service'.
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=COMPANY_SERVICE_URL,
                json=request_data.model_dump(), # .model_dump() is Pydantic v2 for .dict()
                timeout=30.0, # Set a reasonable timeout.
            )
            # Raise an exception for 4xx/5xx client/server errors.
            response.raise_for_status()
            # If the request was successful, return the response from the downstream service.
            return response.json()

        except httpx.RequestError as e:
            # Handles network-level errors, such as connection refused.
            print(f"Error requesting company service: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="The company service is currently unavailable. Please try again later."
            )
        except httpx.HTTPStatusError as e:
            # Handles application-level HTTP errors returned by the downstream service.
            # Forwards the error details from the downstream service to the client.
            print(f"Company service returned an error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json()
            )
