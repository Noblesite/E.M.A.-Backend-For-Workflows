from pydantic import BaseModel
from typing import Optional


class DeleteSmartGroupBySmartGroupIdDTO(BaseModel):
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if not api_response.get("errorCode"):
            return cls(success=True)

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeleteSmartGroupBySmartGroupIdDTO Missing Values")

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = {}
    dto = DeleteSmartGroupBySmartGroupIdDTO.from_api_response(api_response)
    print(dto.success)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {
        "errorCode": "404",
        "message": "Smart Group not found"
    }
    dto = DeleteSmartGroupBySmartGroupIdDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
