from pydantic import BaseModel, Field
from typing import Dict, Optional
from device_search_dto import DeviceSearchDTO  # Assuming DeviceSearchDTO is in a separate module


class DeviceSearchListDTO(BaseModel):
    device_search_list: Dict[str, DeviceSearchDTO] = Field(default_factory=dict, alias="Devices")
    page: Optional[int] = Field(None, alias="Page")
    page_size: Optional[int] = Field(None, alias="PageSize")
    total: Optional[int] = Field(None, alias="Total")
    error_code: Optional[str] = None
    success: bool = False

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "Devices" in api_response:
            device_search_list = {
                device["Id"]["Value"]: DeviceSearchDTO.from_api_response(device)
                for device in api_response["Devices"]
            }
            return cls(
                device_search_list=device_search_list,
                page=api_response.get("Page"),
                page_size=api_response.get("PageSize"),
                total=api_response.get("Total"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceSearchListDTO Missing Values")

    def get_device_search_list(self) -> Dict[str, DeviceSearchDTO]:
        """Getter for device_search_list."""
        return self.device_search_list

    def get_page(self) -> Optional[int]:
        """Getter for page."""
        return self.page

    def get_page_size(self) -> Optional[int]:
        """Getter for page_size."""
        return self.page_size

    def get_total(self) -> Optional[int]:
        """Getter for total."""
        return self.total

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success


# Example usage
try:
    api_response = {
        "Devices": [
            {
                "Id": {"Value": "12345"},
                "Udid": "udid-12345",
                "SerialNumber": "SN123456789",
                "MacAddress": "00:11:22:33:44:55",
                "OperatingSystem": "Android",
                "DeviceFriendlyName": "Test Device"
            },
            {
                "Id": {"Value": "67890"},
                "Udid": "udid-67890",
                "SerialNumber": "SN987654321",
                "MacAddress": "00:55:44:33:22:11",
                "OperatingSystem": "iOS",
                "DeviceFriendlyName": "Sample Device"
            }
        ],
        "Total": 2,
        "Page": 1,
        "PageSize": 10
    }
    dto = DeviceSearchListDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.total)
    for device_id, device in dto.device_search_list.items():
        print(f"Device ID: {device_id}, Friendly Name: {device.device_friendly_name}")
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"errorCode": "404", "message": "No devices found"}
    dto = DeviceSearchListDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
