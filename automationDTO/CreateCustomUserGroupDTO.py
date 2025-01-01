from pydantic import BaseModel, ValidationError
from typing import Optional


class CreateCustomUserGroupDTO(BaseModel):
    uuid: Optional[str] = None
    value: Optional[str] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "uuid" in api_response and "Value" in api_response:
            return cls(
                uuid=api_response.get("uuid"),
                value=api_response.get("Value"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("CreateCustomUserGroupDTO Missing Values")

    def get_uuid(self) -> Optional[str]:
        """Getter for uuid."""
        return self.uuid

    def get_value(self) -> Optional[str]:
        """Getter for value."""
        return self.value

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success


# Example usage
try:
    api_response = {
        "uuid": "1234-5678-9012",
        "Value": "CustomUserGroup123"
    }
    dto = CreateCustomUserGroupDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.uuid)
    print(dto.value)
except ValueError as e:
    print(f"Error: {e}")
