import httpx
from config import settings
from typing import List, Dict, Any, Optional

class LMSApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Base GET request handler with error reporting."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    return {"status": "ok", "data": response.json()}
                
                return {
                    "status": "error", 
                    "message": f"HTTP {response.status_code} {response.reason_phrase}. The backend service may be down."
                }
        except httpx.ConnectError:
            return {
                "status": "error",
                "message": f"connection refused ({url}). Check that the services are running."
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"unsupported error: {str(e)}"
            }

    async def get_items(self) -> Dict[str, Any]:
        return await self._get("items/")

    async def get_pass_rates(self, lab_id: str) -> Dict[str, Any]:
        return await self._get("analytics/pass-rates", params={"lab": lab_id})

lms_client = LMSApiClient(settings.LMS_API_URL, settings.LMS_API_KEY)
