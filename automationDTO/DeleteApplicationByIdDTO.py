from pydantic import BaseModel
from typing import Optional


class DeleteApplicationByIdDTO(BaseModel):
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: Optional[dict] = None):
        """Factory method to create an instance from API response."""
        if api_response is None or not api_response.get("errorCode"):
            return cls(success=True)

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeleteApplicationByIdDTO Missing Values")

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = {}
    dto = DeleteApplicationByIdDTO.from_api_response(api_response)
    print(dto.success)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {
        "errorCode": "404",
        "message": "Application not found"
    }
    dto = DeleteApplicationByIdDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
