from pydantic import BaseModel
from typing import Optional


class CreateSmartGroupDTO(BaseModel):
    value: Optional[str] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if not api_response.get("errorCode"):
            return cls(
                value=api_response.get("Value"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("CreateSmartGroupDTO Missing Values")

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
        "Value": "SG12345"
    }
    dto = CreateSmartGroupDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.value)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {
        "errorCode": "400",
        "message": "Invalid request"
    }
    dto = CreateSmartGroupDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
