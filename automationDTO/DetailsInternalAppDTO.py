from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class DetailsInternalAppDTO(BaseModel):
    application_name: Optional[str] = Field(alias="ApplicationName")
    app_id: Optional[int] = Field(alias="AppId")
    actual_file_version: Optional[str] = Field(alias="ActualFileVersion")
    build_version: Optional[str] = Field(alias="BuildVersion")
    airwatch_app_version: Optional[str] = Field(alias="AirwatchAppVersion")
    status: Optional[str] = Field(alias="Status")
    managed_by: Optional[str] = Field(alias="ManagedBy")
    managed_by_uuid: Optional[str] = Field(alias="ManagedByUuid")
    assume_management_of_user_installed_app: Optional[bool] = Field(alias="AssumeManagementOfUserInstalledApp")
    platform: Optional[str] = Field(alias="Platform")
    supported_models: Optional[List[str]] = Field(alias="SupportedModels")
    minimum_operating_system: Optional[str] = Field(alias="MinimumOperatingSystem")
    app_size_in_kb: Optional[int] = Field(alias="AppSizeInKB")
    category_list: Optional[List[str]] = Field(alias="CategoryList")
    comments: Optional[str] = Field(alias="Comments")
    application_url: Optional[str] = Field(alias="ApplicationUrl")
    sdk: Optional[bool] = Field(alias="Sdk")
    sdk_profile_id: Optional[int] = Field(alias="SdkProfileId")
    sdk_profile_uuid: Optional[str] = Field(alias="SdkProfileUuid")
    devices_assigned_count: Optional[int] = Field(alias="DevicesAssignedCount")
    devices_installed_count: Optional[int] = Field(alias="DevicesInstalledCount")
    devices_not_installed_count: Optional[int] = Field(alias="DevicesNotInstalledCount")
    rating: Optional[int] = Field(alias="Rating")
    change_log: Optional[str] = Field(alias="ChangeLog")
    renewal_date: Optional[str] = Field(alias="RenewalDate")
    assignments: Optional[List[Dict[str, Any]]] = Field(alias="Assignments")
    smart_group_ids: Optional[List[int]] = []
    smart_group_uuids: Optional[List[str]] = []
    effective_dates: Optional[List[str]] = []
    excluded_smart_group_ids: Optional[List[int]] = Field(alias="ExcludedSmartGroupIds")
    excluded_smart_group_guids: Optional[List[str]] = Field(alias="ExcludedSmartGroupGuids")
    msi_deployment_param_model: Optional[Dict[str, Any]] = Field(alias="MsiDeploymentParamModel")
    deployment_options: Optional[Dict[str, Any]] = Field(alias="DeploymentOptions")
    files_options: Optional[Dict[str, Any]] = Field(alias="FilesOptions")
    mac_os_software_deployment_summary: Optional[Dict[str, Any]] = Field(alias="MacOsSoftwareDeploymentSummary")
    id: Optional[int] = Field(alias="id")
    uuid: Optional[str] = Field(alias="uuid")
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "ApplicationName" in api_response and "id" in api_response and "uuid" in api_response:
            assignments = api_response.get("Assignments", [])
            smart_group_ids = [sg.get("SmartGroupId") for sg in assignments]
            smart_group_uuids = [sg.get("SmartGroupUuid") for sg in assignments]
            effective_dates = [sg.get("EffectiveDate") for sg in assignments]
            return cls(
                **api_response,
                success=True,
                smart_group_ids=smart_group_ids,
                smart_group_uuids=smart_group_uuids,
                effective_dates=effective_dates
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DetailsInternalAppDTO Missing Values")

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = {
        "ApplicationName": "Sample App",
        "AppId": 12345,
        "ActualFileVersion": "1.0.0",
        "BuildVersion": "100",
        "AirwatchAppVersion": "1.2.3",
        "Status": "Active",
        "ManagedBy": "Admin",
        "ManagedByUuid": "abcd-efgh",
        "AssumeManagementOfUserInstalledApp": True,
        "Platform": "iOS",
        "SupportedModels": ["iPhone", "iPad"],
        "MinimumOperatingSystem": "iOS 14",
        "AppSizeInKB": 2048,
        "CategoryList": ["Productivity"],
        "Comments": "This is a test app.",
        "ApplicationUrl": "https://example.com",
        "Sdk": True,
        "DevicesAssignedCount": 10,
        "DevicesInstalledCount": 8,
        "DevicesNotInstalledCount": 2,
        "Rating": 4,
        "ChangeLog": "Initial release",
        "Assignments": [
            {"SmartGroupId": 1, "SmartGroupUuid": "sg-uuid-1", "EffectiveDate": "2023-01-01"},
            {"SmartGroupId": 2, "SmartGroupUuid": "sg-uuid-2", "EffectiveDate": "2023-02-01"}
        ],
        "ExcludedSmartGroupIds": [3],
        "ExcludedSmartGroupGuids": ["sg-uuid-3"],
        "id": 123,
        "uuid": "app-uuid"
    }
    dto = DetailsInternalAppDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.application_name)
    print(dto.smart_group_ids)
except ValueError as e:
    print(f"Error: {e}")
