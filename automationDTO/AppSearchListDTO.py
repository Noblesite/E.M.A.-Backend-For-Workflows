from pydantic import BaseModel, ValidationError
from typing import Dict, Optional
from app_search_dto import AppSearchDTO  # Assuming AppSearchDTO is in the same directory


class AppSearchListDTO(BaseModel):
    app_search_list: Dict[str, AppSearchDTO] = {}
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "Application" in api_response:
            app_search_list = {
                application["Id"]["Value"]: AppSearchDTO(**application)
                for application in api_response.get("Application", [])
            }
            return cls(app_search_list=app_search_list, success=True)

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("AppSearchListDTO Missing Values")

    def get_app_search_list(self) -> Dict[str, AppSearchDTO]:
        return self.app_search_list

    def get_error_code(self) -> Optional[str]:
        return self.error_code

    def get_success(self) -> bool:
        return self.success


# Example usage
try:
    api_response = {
        "Application": [
            {
                "ApplicationName": "Sample App 1",
                "BundleId": "com.example.app1",
                "AppVersion": "1.0.0",
                "Status": "Active",
                "AssignedDeviceCount": 100,
                "Id": {"Value": "APP123"}
            },
            {
                "ApplicationName": "Sample App 2",
                "BundleId": "com.example.app2",
                "AppVersion": "2.0.0",
                "Status": "Inactive",
                "AssignedDeviceCount": 50,
                "Id": {"Value": "APP456"}
            }
        ]
    }
    dto = AppSearchListDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.app_search_list)
    for app_id, app in dto.app_search_list.items():
        print(f"App ID: {app_id}, App Name: {app.application_name}")
except ValueError as e:
    print(f"Error: {e}")
