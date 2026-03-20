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
            async with httpx.AsyncClient(timeout=15.0) as client:
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

    async def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Base POST request handler."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(url, headers=self.headers, json=data or {})
                if response.status_code in (200, 201):
                    return {"status": "ok", "data": response.json()}
                return {"status": "error", "message": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Tools endpoints
    async def get_items(self) -> Dict[str, Any]:
        return await self._get("items/")

    async def get_learners(self) -> Dict[str, Any]:
        return await self._get("learners/")

    async def get_scores(self, lab: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("analytics/scores", params={"lab": lab} if lab else None)

    async def get_pass_rates(self, lab: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("analytics/pass-rates", params={"lab": lab} if lab else None)

    async def get_timeline(self, lab: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("analytics/timeline", params={"lab": lab} if lab else None)

    async def get_groups(self, lab: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("analytics/groups", params={"lab": lab} if lab else None)

    async def get_top_learners(self, lab: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
        params = {"limit": limit}
        if lab: params["lab"] = lab
        return await self._get("analytics/top-learners", params=params)

    async def get_completion_rate(self, lab: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("analytics/completion-rate", params={"lab": lab} if lab else None)

    async def trigger_sync(self) -> Dict[str, Any]:
        return await self._post("pipeline/sync")

lms_client = LMSApiClient(settings.LMS_API_URL, settings.LMS_API_KEY)
