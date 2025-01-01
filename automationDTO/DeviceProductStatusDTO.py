from pydantic import BaseModel
from typing import Optional


class DeviceProductStatusDTO(BaseModel):
    device_id: Optional[str] = None
    name: Optional[str] = None
    last_job_status: Optional[str] = None
    last_seen: Optional[str] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if api_response.get("DeviceId") is not None:
            return cls(
                device_id=api_response.get("DeviceId"),
                name=api_response.get("Name"),
                last_job_status=api_response.get("LastJobStatus"),
                last_seen=api_response.get("LastSeen"),
                success=True
            )
        
        return cls(
            success=False,
            error_code="DeviceProductStatusDTO mapObject Error: Missing Values."
        )

    def get_device_id(self) -> Optional[str]:
        """Getter for device_id."""
        return self.device_id

    def get_name(self) -> Optional[str]:
        """Getter for name."""
        return self.name

    def get_last_job_status(self) -> Optional[str]:
        """Getter for last_job_status."""
        return self.last_job_status

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success


# Example usage
try:
    api_response = {
        "DeviceId": "12345",
        "Name": "Test Device",
        "LastJobStatus": "Success",
        "LastSeen": "2023-01-01T00:00:00Z"
    }
    dto = DeviceProductStatusDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.device_id)
    print(dto.name)
    print(dto.last_job_status)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"Name": "Missing DeviceId"}
    dto = DeviceProductStatusDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.error_code)
except ValueError as e:
    print(f"Error: {e}")
