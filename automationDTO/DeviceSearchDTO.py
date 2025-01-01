from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class DeviceSearchDTO(BaseModel):
    udid: Optional[str] = Field(None, alias="Udid")
    serial_number: Optional[str] = Field(None, alias="SerialNumber")
    mac_address: Optional[str] = Field(None, alias="MacAddress")
    imei: Optional[str] = Field(None, alias="Imei")
    eas_id: Optional[str] = Field(None, alias="EasId")
    asset_number: Optional[str] = Field(None, alias="AssetNumber")
    device_friendly_name: Optional[str] = Field(None, alias="DeviceFriendlyName")
    location_group_id: Optional[Dict[str, Any]] = Field(None, alias="LocationGroupId")
    location_group_id_value: Optional[str] = Field(None, alias="LocationGroupId.Id.Value")
    location_group_id_uuid: Optional[str] = Field(None, alias="LocationGroupId.Uuid")
    location_group_id_name: Optional[str] = Field(None, alias="LocationGroupId.Name")
    location_group_name: Optional[str] = Field(None, alias="LocationGroupName")
    user_name: Optional[str] = Field(None, alias="UserName")
    user_email_address: Optional[str] = Field(None, alias="UserEmailAddress")
    ownership: Optional[str] = Field(None, alias="Ownership")
    platform_id: Optional[Dict[str, Any]] = Field(None, alias="PlatformId")
    platform_id_value: Optional[str] = Field(None, alias="PlatformId.Id.Value")
    platform_id_name: Optional[str] = Field(None, alias="PlatformId.Name")
    platform_id_platform: Optional[str] = Field(None, alias="PlatformId.Platform", default="Unknown")
    model_id: Optional[Dict[str, Any]] = Field(None, alias="ModelId")
    model_id_value: Optional[str] = Field(None, alias="ModelId.Id.Value")
    model_id_name: Optional[str] = Field(None, alias="ModelId.Name")
    model: Optional[str] = Field(None, alias="Model")
    operating_system: Optional[str] = Field(None, alias="OperatingSystem")
    phone_number: Optional[str] = Field(None, alias="PhoneNumber")
    last_seen: Optional[str] = Field(None, alias="LastSeen")
    enrollment_status: Optional[str] = Field(None, alias="EnrollmentStatus")
    compliance_status: Optional[str] = Field(None, alias="ComplianceStatus")
    compromised_status: Optional[str] = Field(None, alias="CompromisedStatus")
    last_enrolled_on: Optional[str] = Field(None, alias="LastEnrolledOn")
    last_compliance_check_on: Optional[str] = Field(None, alias="LastComplianceCheckOn")
    last_compromised_check_on: Optional[str] = Field(None, alias="LastCompromisedCheckOn")
    is_supervised: Optional[bool] = Field(None, alias="IsSupervised")
    is_remote_management_enabled: Optional[bool] = Field(None, alias="IsRemoteManagementEnabled")
    data_encryption_yn: Optional[bool] = Field(None, alias="DataEncryptionYN")
    ac_line_status: Optional[str] = Field(None, alias="AcLineStatus")
    virtual_memory: Optional[int] = Field(None, alias="VirtualMemory")
    oem_info: Optional[str] = Field(None, alias="OEMInfo")
    last_system_sample_time: Optional[str] = Field(None, alias="LastSystemSampleTime", default="Unknown")
    is_device_dnd_enabled: Optional[bool] = Field(None, alias="IsDeviceDNDEnabled")
    is_device_locator_enabled: Optional[bool] = Field(None, alias="IsDeviceLocatorEnabled")
    is_network_tethered: Optional[bool] = Field(None, alias="IsNetworkTethered")
    battery_level: Optional[int] = Field(None, alias="BatteryLevel")
    is_roaming: Optional[bool] = Field(None, alias="IsRoaming")
    last_network_lan_sample_time: Optional[str] = Field(None, alias="LastNetworkLANSampleTime", default="Unknown")
    last_bluetooth_sample_time: Optional[str] = Field(None, alias="LastBluetoothSampleTime", default="Unknown")
    system_integrity_protection_enabled: Optional[bool] = Field(None, alias="SystemIntegrityProtectionEnabled")
    processor_architecture: Optional[str] = Field(None, alias="ProcessorArchitecture")
    total_physical_memory: Optional[int] = Field(None, alias="TotalPhysicalMemory")
    available_physical_memory: Optional[int] = Field(None, alias="AvailablePhysicalMemory")
    os_build_version: Optional[str] = Field(None, alias="OSBuildVersion")
    host_name: Optional[str] = Field(None, alias="HostName")
    local_host_name: Optional[str] = Field(None, alias="LocalHostName")
    device_id: Optional[str] = Field(None, alias="Id.Value")
    uuid: Optional[str] = Field(None, alias="Uuid")
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "Id" in api_response:
            return cls(**api_response, success=True)

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceSearchDTO Missing Values")

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = {
        "Id": {"Value": "12345"},
        "Udid": "udid-12345",
        "SerialNumber": "SN123456789",
        "MacAddress": "00:11:22:33:44:55",
        "OperatingSystem": "Android",
        "DeviceFriendlyName": "Test Device",
        "LocationGroupId": {"Id": {"Value": "LGID1"}, "Uuid": "UUID1", "Name": "Test Group"},
        "PlatformId": {"Id": {"Value": "PLID1"}, "Name": "Test Platform"},
        "ModelId": {"Id": {"Value": "MOD1"}, "Name": "Test Model"},
        "BatteryLevel": 95
    }
    dto = DeviceSearchDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.device_friendly_name)
    print(dto.battery_level)
except ValueError as e:
    print(f"Error: {e}")
