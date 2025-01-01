from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class DeviceDetailsDTO(BaseModel):
    device_id: Optional[str] = Field(None, alias="DeviceId.Value")
    udid: Optional[str] = Field(None, alias="UDID")
    serial_number: Optional[str] = Field(None, alias="SerialNumber")
    asset_number: Optional[str] = Field(None, alias="AssetNumber")
    friendly_name: Optional[str] = Field(None, alias="FriendlyName")
    organization_group_id: Optional[int] = Field(None, alias="OrganizationGroupId")
    username: Optional[str] = Field(None, alias="Username")
    available_disk_space: Optional[int] = Field(None, alias="AvailableDiskSpace")
    total_memory: Optional[int] = Field(None, alias="TotalMemory")
    device_network_info: Optional[Dict[str, Any]] = Field(None, alias="DeviceNetworkInfo")
    available_disk_space_in_mb: Optional[int] = None
    total_memory_in_mb: Optional[int] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "SerialNumber" in api_response:
            available_disk_space = api_response.get("AvailableDiskSpace")
            total_memory = api_response.get("TotalMemory")
            return cls(
                device_id=api_response.get("DeviceId", {}).get("Value"),
                udid=api_response.get("UDID"),
                serial_number=api_response.get("SerialNumber"),
                asset_number=api_response.get("AssetNumber"),
                friendly_name=api_response.get("FriendlyName"),
                organization_group_id=api_response.get("OrganizationGroupId"),
                username=api_response.get("Username"),
                available_disk_space=available_disk_space,
                total_memory=total_memory,
                device_network_info=api_response.get("DeviceNetworkInfo"),
                available_disk_space_in_mb=(available_disk_space // 1024 // 1024) if available_disk_space else None,
                total_memory_in_mb=(total_memory // 1024 // 1024) if total_memory else None,
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceDetailsDTO Missing Values")

    def get_available_disk_space_in_mb(self) -> Optional[int]:
        """Getter for available_disk_space_in_mb."""
        return self.available_disk_space_in_mb

    def get_total_memory_in_mb(self) -> Optional[int]:
        """Getter for total_memory_in_mb."""
        return self.total_memory_in_mb


# Example usage
try:
    api_response = {
        "DeviceId": {"Value": "12345"},
        "UDID": "udid-12345",
        "SerialNumber": "SN123456789",
        "AssetNumber": "A12345",
        "FriendlyName": "Test Device",
        "OrganizationGroupId": 456,
        "Username": "jdoe",
        "AvailableDiskSpace": 53687091200,  # 50 GB in bytes
        "TotalMemory": 8589934592,  # 8 GB in bytes
        "DeviceNetworkInfo": {"IP": "192.168.1.100"}
    }
    dto = DeviceDetailsDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.serial_number)
    print(dto.available_disk_space_in_mb)
    print(dto.total_memory_in_mb)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"errorCode": "404", "message": "Device not found"}
    dto = DeviceDetailsDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
