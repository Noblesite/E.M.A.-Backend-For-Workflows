from pydantic import BaseModel, ValidationError
from typing import Dict, Optional, List
from dep_device_by_og_dto import DEPDeviceByOGDTO  # Assuming this DTO is in a separate file


class DEPDeviceByOGListDTO(BaseModel):
    dep_device_list: Dict[str, DEPDeviceByOGDTO] = {}
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: List[dict]):
        """Factory method to create an instance from API response."""
        if not any(device.get("errorCode") for device in api_response):
            dep_device_list = {
                device["deviceSerialNumber"]: DEPDeviceByOGDTO.from_api_response(device)
                for device in api_response
            }
            return cls(dep_device_list=dep_device_list, success=True)

        if "errorCode" in api_response[0]:
            error_message = f"Error code: {api_response[0]['errorCode']} Error Message: {api_response[0].get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DEPDeviceByOGListDTO Missing Values")

    def get_dep_device_list(self) -> Dict[str, DEPDeviceByOGDTO]:
        """Getter for dep_device_list."""
        return self.dep_device_list

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = [
        {
            "deviceSerialNumber": "12345ABC",
            "deviceFriendlyName": "Test Device 1",
            "deviceImei": "111222333444555",
            "deviceOwnership": "Corporate",
            "username": "jdoe",
            "enrollmentStatus": "Enrolled",
            "deviceModel": "iPhone 12",
            "profileUuid": "abcd-efgh-ijkl-mnop",
            "deviceAssetNumber": "A123456",
            "organizationGroupName": "Test Org",
            "profileName": "Corporate Profile"
        },
        {
            "deviceSerialNumber": "67890XYZ",
            "deviceFriendlyName": "Test Device 2",
            "deviceImei": "666555444333222",
            "deviceOwnership": "Corporate",
            "username": "asmith",
            "enrollmentStatus": "Pending",
            "deviceModel": "iPad Pro",
            "profileUuid": "mnop-ijkl-efgh-abcd",
            "deviceAssetNumber": "A654321",
            "organizationGroupName": "Demo Org",
            "profileName": "Retail Profile"
        }
    ]
    dto = DEPDeviceByOGListDTO.from_api_response(api_response)
    print(dto.success)
    for serial, device in dto.dep_device_list.items():
        print(f"Serial: {serial}, Friendly Name: {device.device_friendly_name}")
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = [{"errorCode": "500", "message": "Internal Server Error"}]
    dto = DEPDeviceByOGListDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
