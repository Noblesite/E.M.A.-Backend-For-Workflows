from pydantic import BaseModel, Field
from typing import Optional


class DeviceAppsDTO(BaseModel):
    application_name: Optional[str] = Field(None, alias="ApplicationName")
    version: Optional[str] = Field(None, alias="Version")
    status: Optional[str] = Field(None, alias="Status")
    size: Optional[int] = Field(None, alias="Size")
    application_identifier: Optional[str] = Field(None, alias="ApplicationIdentifier")
    type: Optional[str] = Field(None, alias="Type")
    is_managed: Optional[bool] = Field(None, alias="IsManaged")
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "ApplicationIdentifier" in api_response:
            return cls(**api_response, success=True)

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceAppsDTO Missing Values")

    def get_application_name(self) -> Optional[str]:
        """Getter for application_name."""
        return self.application_name

    def get_version(self) -> Optional[str]:
        """Getter for version."""
        return self.version

    def get_status(self) -> Optional[str]:
        """Getter for status."""
        return self.status

    def get_size(self) -> Optional[int]:
        """Getter for size."""
        return self.size

    def get_application_identifier(self) -> Optional[str]:
        """Getter for application_identifier."""
        return self.application_identifier

    def get_type(self) -> Optional[str]:
        """Getter for type."""
        return self.type

    def get_is_managed(self) -> Optional[bool]:
        """Getter for is_managed."""
        return self.is_managed

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success


# Example usage
try:
    api_response = {
        "ApplicationName": "Example App",
        "Version": "1.0.0",
        "Status": "Installed",
        "Size": 2048,
        "ApplicationIdentifier": "com.example.app",
        "Type": "Mobile",
        "IsManaged": True
    }
    dto = DeviceAppsDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.application_name)
    print(dto.application_identifier)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"errorCode": "404", "message": "Application not found"}
    dto = DeviceAppsDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
