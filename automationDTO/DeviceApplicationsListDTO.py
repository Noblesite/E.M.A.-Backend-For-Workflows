from pydantic import BaseModel, Field
from typing import List, Optional
from device_apps_dto import DeviceAppsDTO  # Assuming DeviceAppsDTO is in a separate module


class DeviceApplicationsListDTO(BaseModel):
    device_apps_list: List[DeviceAppsDTO] = Field(default_factory=list, alias="DeviceApps")
    total: Optional[int] = Field(None, alias="Total")
    page: Optional[int] = Field(None, alias="Page")
    page_size: Optional[int] = Field(None, alias="PageSize")
    error_code: Optional[str] = None
    success: bool = False

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "DeviceApps" in api_response:
            device_apps_list = [DeviceAppsDTO(**app_details) for app_details in api_response.get("DeviceApps", [])]
            return cls(
                device_apps_list=device_apps_list,
                total=api_response.get("Total"),
                page=api_response.get("Page"),
                page_size=api_response.get("PageSize"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceApplicationsListDTO Missing Values")

    def get_device_apps_list(self) -> List[DeviceAppsDTO]:
        """Getter for device_apps_list."""
        return self.device_apps_list

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_total(self) -> Optional[int]:
        """Getter for total."""
        return self.total

    def get_page_size(self) -> Optional[int]:
        """Getter for page_size."""
        return self.page_size

    def get_page(self) -> Optional[int]:
        """Getter for page."""
        return self.page


# Example usage
try:
    api_response = {
        "DeviceApps": [
            {"AppName": "App 1", "AppId": "com.example.app1", "Version": "1.0.0"},
            {"AppName": "App 2", "AppId": "com.example.app2", "Version": "2.0.0"}
        ],
        "Total": 2,
        "Page": 1,
        "PageSize": 10
    }
    dto = DeviceApplicationsListDTO.from_api_response(api_response)
    print(dto.success)
    for app in dto.device_apps_list:
        print(f"App Name: {app.app_name}, App ID: {app.app_id}")
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"errorCode": "404", "message": "Apps not found"}
    dto = DeviceApplicationsListDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
