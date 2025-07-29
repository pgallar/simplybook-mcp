from typing import Dict, Any, List
import httpx

class NotesClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_notes_list(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}notes",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_note_details(self, note_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}notes/{note_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def create_note(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}notes",
                json=note_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def modify_note(self, note_id: str, note_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}notes/{note_id}",
                json=note_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def delete_note(self, note_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}notes/{note_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()