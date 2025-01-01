import requests


class MAMRestController:
    def __init__(self, apiurl, tenant, authorization):
        self.apiurl = apiurl
        self.tenant = tenant
        self.authorization = authorization

    def _make_request(self, method, endpoint, payload=None, params=None, files=None):
        """Helper function to make HTTP requests."""
        url = f"{self.apiurl}{endpoint}"
        headers = {
            "Authorization": self.authorization,
            "aw-tenant-code": self.tenant,
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, json=payload, params=params, headers=headers, files=files)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()

    def upload_blob(self, filename, apk_file_path, module_type, organization_group_id):
        """Upload an application blob."""
        endpoint = f"/mam/blobs/uploadblob?filename={filename}&organizationgroupid={organization_group_id}&moduleType={module_type}"
        with open(apk_file_path, "rb") as apk_file:
            return self._make_request("POST", endpoint, files={"file": apk_file})

    def rename_blob_application(self, application_name, application_value):
        """Rename a blob application."""
        endpoint = f"/mam/apps/internal/{application_value}"
        payload = {
            "ApplicationName": application_name,
            "EnableProvisioning": True
        }
        return self._make_request("PUT", endpoint, payload=payload)

    def install_blob(self, blob_value, appname, deploy, auto_update_version, location_group_id):
        """Install a blob."""
        endpoint = "/mam/apps/internal/begininstall"
        payload = {
            "DeviceType": 5,
            "BlobId": blob_value,
            "ApplicationName": appname,
            "EnableProvisioning": False,
            "SupportedModels": {"Model": [{"ModelId": 5, "ModelName": "Android"}]},
            "PushMode": deploy,
            "AutoUpdateVersion": auto_update_version,
            "LocationGroupID": location_group_id,
        }
        return self._make_request("POST", endpoint, payload=payload)

    def install_blob_product(self, blob_value, appname, deploy, auto_update_version, location_group_id):
        """Install a blob product."""
        endpoint = "/mam/apps/internal/begininstall"
        payload = {
            "DeviceType": 5,
            "BlobId": blob_value,
            "ApplicationName": appname,
            "EnableProvisioning": True,
            "SupportedModels": {"Model": [{"ModelId": 5, "ModelName": "Android"}]},
            "PushMode": deploy,
            "AutoUpdateVersion": auto_update_version,
            "LocationGroupID": location_group_id,
        }
        return self._make_request("POST", endpoint, payload=payload)

    def assign_internal_app_to_smart_group(self, app_id, smart_groups, effective_date):
        """Assign an internal app to a smart group."""
        endpoint = f"/mam/apps/internal/{app_id}/assignments"
        payload = {
            "DeploymentParameters": {
                "EffectiveDate": effective_date,
                "PushMode": "Auto",
                "RemoveOnUnEnroll": True
            },
            "SmartGroupIds": smart_groups,
        }
        return self._make_request("POST", endpoint, payload=payload)

    def delete_application_assignment_to_smart_group(self, app_id, smart_group_ids):
        """Remove all smart groups from an application."""
        endpoint = f"/mam/apps/internal/{app_id}/assignments"
        payload = {"SmartGroupIDs": smart_group_ids, "id": app_id}
        return self._make_request("DELETE", endpoint, payload=payload)

    def details_of_internal_app_by_app_id(self, app_id):
        """Get details of an internal app by app ID."""
        endpoint = f"/mam/apps/internal/{app_id}"
        return self._make_request("GET", endpoint)

    def retire_internal_application(self, app_id):
        """Retire an internal application."""
        endpoint = f"/mam/apps/internal/{app_id}/retire"
        return self._make_request("POST", endpoint)

    def edit_assignments_associated_with_internal_app(self, app_id, smart_groups):
        """Edit assignments of an internal app."""
        endpoint = f"/mam/apps/internal/{app_id}/assignments"
        payload = {
            "DeploymentParameters": {
                "AdaptiveManagement": True,
                "ApplicationBackup": False,
                "AutoUpdateDevicesWithPreviousVersion": True,
                "PushMode": "Auto",
                "RemoveOnUnEnroll": True,
                "AllowManagement": True,
                "Rank": 0
            },
            "SmartGroupIds": smart_groups,
        }
        return self._make_request("PUT", endpoint, payload=payload)

    def update_sg_assignments_with_internal_app(self, app_id, smart_groups, remove_smart_groups):
        """Update smart group assignments for an internal app."""
        endpoint = f"/mam/apps/internal/{app_id}/assignments"
        payload = {
            "DeploymentParameters": {
                "AdaptiveManagement": True,
                "ApplicationBackup": False,
                "AutoUpdateDevicesWithPreviousVersion": True,
                "PushMode": "Auto",
                "RemoveOnUnEnroll": True,
                "AllowManagement": True,
                "Rank": 0
            },
            "SmartGroupIds": smart_groups,
            "SmartGroupIdsForDeletion": remove_smart_groups,
        }
        return self._make_request("PUT", endpoint, payload=payload)

    def search_application_by_bundle_id(self, bundle_id):
        """Search for an application by bundle ID."""
        endpoint = f"/mam/apps/search?bundleid={bundle_id}"
        return self._make_request("GET", endpoint)

    def delete_application_by_app_id(self, app_id):
        """Delete an application by app ID."""
        endpoint = f"/mam/apps/internal/{app_id}"
        return self._make_request("DELETE", endpoint)

    def get_api_url(self):
        """Return the API URL."""
        return self.apiurl