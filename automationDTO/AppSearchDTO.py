from pydantic import BaseModel
from typing import Optional


class AppSearchDTO(BaseModel):
    application_name: Optional[str] = None
    bundle_id: Optional[str] = None
    app_version: Optional[str] = None
    status: Optional[str] = None
    assigned_device_count: Optional[int] = None
    app_id: Optional[str] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "ApplicationName" in api_response:
            return cls(
                application_name=api_response.get("ApplicationName"),
                bundle_id=api_response.get("BundleId"),
                app_version=api_response.get("AppVersion"),
                status=api_response.get("Status"),
                assigned_device_count=api_response.get("AssignedDeviceCount"),
                app_id=api_response.get("Id", {}).get("Value"),
                success=True,
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("AppSearchDTO Missing Values")

    def get_application_name(self) -> Optional[str]:
        return self.application_name

    def get_bundle_id(self) -> Optional[str]:
        return self.bundle_id

    def get_app_version(self) -> Optional[str]:
        return self.app_version

    def get_status(self) -> Optional[str]:
        return self.status

    def get_assigned_device_count(self) -> Optional[int]:
        return self.assigned_device_count

    def get_app_id(self) -> Optional[str]:
        return self.app_id

    def get_error_code(self) -> Optional[str]:
        return self.error_code

    def get_success(self) -> bool:
        return self.success


# Example usage
try:
    api_response = {
        "ApplicationName": "Sample App",
        "BundleId": "com.example.app",
        "AppVersion": "1.0.0",
        "Status": "Active",
        "AssignedDeviceCount": 100,
        "Id": {"Value": "APP123"},
    }
    dto = AppSearchDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.application_name)
    print(dto.bundle_id)
    print(dto.app_id)
except ValueError as e:
    print(f"Error: {e}")
