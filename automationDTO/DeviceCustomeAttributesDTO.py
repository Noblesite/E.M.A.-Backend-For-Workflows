from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class DeviceCustomeAttributesDTO(BaseModel):
    device_id: Optional[str] = Field(None, alias="DeviceId")
    udid: Optional[str] = Field(None, alias="Udid")
    serial_number: Optional[str] = Field(None, alias="SerialNumber")
    enrollment_user_name: Optional[str] = Field(None, alias="EnrollmentUserName")
    asset_number: Optional[str] = Field(None, alias="AssetNumber")
    custom_attributes: Dict[str, Optional[str]] = Field(default_factory=dict, alias="CustomAttributes")
    error_code: Dict[str, str] = Field(default_factory=dict)
    success: bool = False

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "DeviceId" in api_response:
            custom_attributes = {
                attr["Name"]: attr.get("Value") for attr in api_response.get("CustomAttributes", [])
            }
            return cls(
                device_id=api_response.get("DeviceId"),
                udid=api_response.get("Udid"),
                serial_number=api_response.get("SerialNumber"),
                enrollment_user_name=api_response.get("EnrollmentUserName"),
                asset_number=api_response.get("AssetNumber"),
                custom_attributes=custom_attributes,
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceCustomeAttributesDTO Missing Values")

    def get_device_id(self) -> Optional[str]:
        """Getter for device_id."""
        return self.device_id

    def get_udid(self) -> Optional[str]:
        """Getter for udid."""
        return self.udid

    def get_serial_number(self) -> Optional[str]:
        """Getter for serial_number."""
        return self.serial_number

    def get_enrollment_user_name(self) -> Optional[str]:
        """Getter for enrollment_user_name."""
        return self.enrollment_user_name

    def get_asset_number(self) -> Optional[str]:
        """Getter for asset_number."""
        return self.asset_number

    def get_custom_attributes(self) -> Dict[str, Optional[str]]:
        """Getter for custom_attributes."""
        return self.custom_attributes

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Dict[str, str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = {
        "DeviceId": "12345",
        "SerialNumber": "SN123456789",
        "Udid": "udid-12345",
        "EnrollmentUserName": "jdoe",
        "AssetNumber": "A12345",
        "CustomAttributes": [
            {"Name": "Attribute1", "Value": "Value1"},
            {"Name": "Attribute2", "Value": "Value2"}
        ]
    }
    dto = DeviceCustomeAttributesDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.custom_attributes)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"errorCode": "404", "message": "Device not found"}
    dto = DeviceCustomeAttributesDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
