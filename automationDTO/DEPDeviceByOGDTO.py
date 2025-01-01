from pydantic import BaseModel
from typing import Optional


class DEPDeviceByOGDTO(BaseModel):
    device_friendly_name: Optional[str] = None
    device_serial_number: Optional[str] = None
    device_imei: Optional[str] = None
    device_ownership: Optional[str] = None
    username: Optional[str] = None
    enrollment_status: Optional[str] = None
    device_model: Optional[str] = None
    profile_uuid: Optional[str] = None
    device_asset_number: Optional[str] = None
    organization_group_name: Optional[str] = None
    profile_name: Optional[str] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "deviceSerialNumber" in api_response:
            return cls(
                device_friendly_name=api_response.get("deviceFriendlyName"),
                device_serial_number=api_response.get("deviceSerialNumber"),
                device_imei=api_response.get("deviceImei"),
                device_ownership=api_response.get("deviceOwnership"),
                username=api_response.get("username"),
                enrollment_status=api_response.get("enrollmentStatus"),
                device_model=api_response.get("deviceModel"),
                profile_uuid=api_response.get("profileUuid"),
                device_asset_number=api_response.get("deviceAssetNumber"),
                organization_group_name=api_response.get("organizationGroupName"),
                profile_name=api_response.get("profileName"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DEPDeviceByOGDTO Missing Values")

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = {
        "deviceSerialNumber": "12345ABC",
        "deviceFriendlyName": "Test Device",
        "deviceImei": "111222333444555",
        "deviceOwnership": "Corporate",
        "username": "jdoe",
        "enrollmentStatus": "Enrolled",
        "deviceModel": "iPhone 12",
        "profileUuid": "abcd-efgh-ijkl-mnop",
        "deviceAssetNumber": "A123456",
        "organizationGroupName": "Test Org",
        "profileName": "Corporate Profile"
    }
    dto = DEPDeviceByOGDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.device_friendly_name)
    print(dto.device_serial_number)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {
        "errorCode": "404",
        "message": "Device not found"
    }
    dto = DEPDeviceByOGDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
