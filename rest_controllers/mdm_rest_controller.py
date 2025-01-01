import requests


class MDMRestController:
    def __init__(self, apiurl, tenant, authorization):
        self.apiurl = apiurl
        self.tenant = tenant
        self.authorization = authorization

    def _make_request(self, method, endpoint, payload=None, params=None):
        """Helper function to make HTTP requests."""
        url = f"{self.apiurl}{endpoint}"
        headers = {
            "Authorization": self.authorization,
            "aw-tenant-code": self.tenant,
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, json=payload, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_smart_group(self, smart_group_name, user_group, managed_by_og_id):
        """Create a new Smart Group."""
        payload = {
            "Name": smart_group_name,
            "ManagedByOrganizationGroupId": managed_by_og_id,
            "UserGroups": [{"Id": user_group}],
        }
        return self._make_request("POST", "/mdm/smartgroups", payload)

    def update_product_details(self, product_id, smart_group):
        """Assign Products to Smart Group."""
        payload = {"SmartGroups": {"SmartGroupID": smart_group}}
        return self._make_request("POST", f"/mdm/products/{product_id}/update", payload)

    def retrieve_device_information(self, serial_number):
        """Retrieve device information by serial number."""
        return self._make_request("GET", f"/mdm/devices/serialnumber/{serial_number}")

    def extensive_search_device_details(self, device_id):
        """Extensive search for device details by device ID."""
        params = {"deviceid": device_id}
        return self._make_request("GET", "/mdm/devices/extensivesearch", params=params)

    def reprocessing_product(self, device_ids, product_id):
        """Reprocess a product."""
        payload = {
            "ForceFlag": True,
            "DeviceIds": [{"ID": device_ids}],
            "ProductID": product_id,
        }
        return self._make_request("POST", "/mdm/products/reprocessProduct", payload)

    def get_device_health_check(self, organization_group_id, page_size, page):
        """Get a list of devices by organization group ID."""
        params = {
            "organizationgroupid": organization_group_id,
            "pagesize": page_size,
            "page": page,
        }
        return self._make_request("GET", "/mdm/products/devicehealthcheck", params=params)

    def delete_device_details_by_device_id(self, device_id):
        """Delete device record by device ID."""
        return self._make_request("DELETE", f"/mdm/devices/{device_id}")

    def delete_smart_group_by_id(self, smart_group_id):
        """Delete a smart group by ID."""
        return self._make_request("DELETE", f"/mdm/smartgroups/{smart_group_id}")

    def create_new_relay_server(self, relay_server_object):
        """Create a new relay server."""
        payload = relay_server_object.to_dict()  # Assuming relay_server_object has a `to_dict()` method.
        return self._make_request("POST", "/mdm/relayservers", payload)

    def find_device_by_serial_number(self, serial_number, repetitions, gap):
        """Make a device ring to help locate it."""
        payload = {
            "Platform": "Android",
            "NumberOfRepetitions": repetitions,
            "GapBetweenRepetitions": gap,
        }
        params = {"searchby": "Serialnumber", "id": serial_number}
        return self._make_request("POST", "/mdm/devices/commands/finddevice", payload, params)

    def send_soft_reset(self, device_id):
        """Restart a mobile device."""
        payload = {"CommandXml": "SoftReset"}
        return self._make_request("POST", f"/mdm/devices/{device_id}/commands", payload)

    def activate_prod_product(self, product_id):
        """Activate a product."""
        return self._make_request("POST", f"/mdm/products/{product_id}/activate")

    def update_device_custom_attribute(self, device_id, attribute_name, app_group, value):
        """Update custom attribute for a device."""
        payload = {
            "CustomAttributes": [{"Name": attribute_name, "Value": value, "ApplicationGroup": app_group}]
        }
        return self._make_request("PUT", f"/mdm/devices/{device_id}/customattributes", payload)

    def sync_device_by_serial_number(self, serial_number):
        """Force a device to check in."""
        params = {"command": "SyncDevice", "searchby": "Serialnumber", "id": serial_number}
        return self._make_request("POST", "/mdm/devices/commands", params=params)

    def clear_device_passcode(self, device_id):
        """Clear a device passcode."""
        params = {"command": "ClearPasscode"}
        return self._make_request("POST", f"/mdm/devices/{device_id}/commands", params=params)

    def device_wipe_by_serial_number(self, serial_number):
        """Factory reset a device."""
        params = {"command": "DeviceWipe", "searchBy": "Serialnumber", "id": serial_number}
        return self._make_request("POST", "/mdm/devices/commands", params=params)

    def get_product_info(self, product_id):
        """Get product information by ID."""
        return self._make_request("GET", f"/mdm/products/{product_id}")