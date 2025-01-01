from pydantic import BaseModel
from typing import Optional


class AddNewTagDTO(BaseModel):
    tag_id: Optional[str] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if not api_response.get("errorCode"):
            return cls(success=True, tag_id=api_response.get("Value"))

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("AddNewTagDTO Missing Values")

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_tag_id(self) -> Optional[str]:
        """Getter for tag_id."""
        return self.tag_id


# Example usage
try:
    api_response = {
        "Value": "TAG12345",
    }
    dto = AddNewTagDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.tag_id)
except ValueError as e:
    print(f"Error: {e}")
