from pydantic import BaseModel, Field
from typing import List, Optional
from device_details_dto import DeviceDetailsDTO  # Assuming DeviceDetailsDTO is in a separate module


class DeviceHealthCheckDTO(BaseModel):
    device_details_list: List[DeviceDetailsDTO] = Field(default_factory=list, alias="Device")
    error_code: Optional[str] = None
    success: bool = False
    total: Optional[int] = Field(None, alias="Total")

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "errorCode" not in api_response:
            device_details_list = [
                DeviceDetailsDTO.from_api_response(device) for device in api_response.get("Device", [])
            ]
            return cls(
                device_details_list=device_details_list,
                total=api_response.get("Total"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceHealthCheckDTO Missing Values")

    def get_device_details_list(self) -> List[DeviceDetailsDTO]:
        """Getter for device_details_list."""
        return self.device_details_list

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_total(self) -> Optional[int]:
        """Getter for total."""
        return self.total


# Example usage
try:
    api_response = {
        "Device": [
            {
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
            },
            {
                "DeviceId": {"Value": "67890"},
                "UDID": "udid-67890",
                "SerialNumber": "SN987654321",
                "AssetNumber": "A98765",
                "FriendlyName": "Sample Device",
                "OrganizationGroupId": 789,
                "Username": "asmith",
                "AvailableDiskSpace": 10737418240,  # 10 GB in bytes
                "TotalMemory": 4294967296,  # 4 GB in bytes
                "DeviceNetworkInfo": {"IP": "192.168.1.101"}
            }
        ],
        "Total": 2
    }
    dto = DeviceHealthCheckDTO.from_api_response(api_response)
    print(dto.success)
    for device in dto.device_details_list:
        print(f"Device ID: {device.device_id}, Serial: {device.serial_number}, Free Disk Space (MB): {device.available_disk_space_in_mb}")
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"errorCode": "404", "message": "No devices found"}
    dto = DeviceHealthCheckDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
