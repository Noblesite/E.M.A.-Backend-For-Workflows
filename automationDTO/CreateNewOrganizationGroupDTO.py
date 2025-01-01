from pydantic import BaseModel
from typing import Optional


class CreateNewOrganizationGroupDTO(BaseModel):
    id: Optional[str] = None
    uuid: Optional[str] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if not api_response.get("errorCode"):
            return cls(
                id=api_response.get("Value"),
                uuid=api_response.get("uuid"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("CreateNewOrganizationGroupDTO Missing Values")

    def get_id(self) -> Optional[str]:
        """Getter for id."""
        return self.id

    def get_uuid(self) -> Optional[str]:
        """Getter for uuid."""
        return self.uuid

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success


# Example usage
try:
    api_response = {
        "Value": "ORG123",
        "uuid": "abcd-efgh-ijkl-mnop"
    }
    dto = CreateNewOrganizationGroupDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.id)
    print(dto.uuid)
except ValueError as e:
    print(f"Error: {e}")
