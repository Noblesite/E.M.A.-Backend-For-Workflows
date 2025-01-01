from pydantic import BaseModel
from typing import Optional, Dict, Any
import json


class DeleteDeviceDetailsbyDeviceIdDTO(BaseModel):
    json_response: Optional[str] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: Dict[str, Any]):
        """Factory method to create an instance from API response."""
        if not api_response.get("errorCode"):
            return cls(
                success=True,
                json_response=json.dumps(api_response)
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeleteDeviceDetailsbyDeviceIdDTO Missing Values")

    def get_json_response(self) -> Optional[str]:
        """Getter for json_response."""
        return self.json_response

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = {"deviceId": "12345", "status": "Deleted"}
    dto = DeleteDeviceDetailsbyDeviceIdDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.json_response)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {
        "errorCode": "404",
        "message": "Device not found"
    }
    dto = DeleteDeviceDetailsbyDeviceIdDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
