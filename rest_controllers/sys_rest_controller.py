import requests


class SYSRestController:
    def __init__(self, apiurl, tenant, authorization):
        self.apiurl = apiurl
        self.tenant = tenant
        self.authorization = authorization

    def _make_request(self, method, endpoint, payload=None, params=None):
        """Helper function to handle HTTP requests."""
        url = f"{self.apiurl}{endpoint}"
        headers = {
            "Authorization": self.authorization,
            "aw-tenant-code": self.tenant,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        }
        response = requests.request(method, url, json=payload, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def search_custom_user_group_with_params(self, name):
        """Search for custom user groups by name."""
        endpoint = f"/system/usergroups/custom/search?groupname={name}"
        return self._make_request("GET", endpoint)

    def create_custom_user_group(self, group_name, organization_group):
        """Create a custom user group."""
        endpoint = "/system/usergroups/createcustomusergroup"
        payload = {
            "GroupName": group_name,
            "Description": f"EMA generated User Group. Created on: {requests.utils.formatdate()}",
            "ManagedByOrganizationGroupID": organization_group,
        }
        return self._make_request("POST", endpoint, payload=payload)

    def retrieve_list_of_users_from_custom_user_group_id(self, user_group_id):
        """Retrieve users in a custom user group by group ID."""
        endpoint = f"/system/usergroups/{user_group_id}/users?pagesize=20000"
        return self._make_request("GET", endpoint)

    def search_for_enrollment_user(self, username):
        """Search for an enrollment user by username."""
        endpoint = f"/system/users/search?username={username}"
        return self._make_request("GET", endpoint)

    def register_device_to_enrollment_user(self, user_id, first_name, location_group_id, ownership, message_id):
        """Register a device to an enrollment user."""
        endpoint = f"/system/users/{user_id}/registerdevice"
        payload = {
            "FriendlyName": f"{first_name}'s Device",
            "LocationGroupId": location_group_id,
            "Ownership": ownership,
            "MessageTemplateId": message_id,
            "MessageType": "Email",
        }
        return self._make_request("POST", endpoint, payload=payload)

    def delete_custom_user_group(self, user_group_id):
        """Delete a custom user group by ID."""
        endpoint = f"/system/usergroups/{user_group_id}/delete"
        return self._make_request("DELETE", endpoint)

    def create_new_organization_group(self, organization_group_name, organization_group_id, location_group_id):
        """Create a new organization group."""
        endpoint = f"/system/groups/{location_group_id}"
        payload = {
            "Name": organization_group_name,
            "GroupId": organization_group_id,
            "LocationGroupType": "Container",
            "Country": "US",
            "Locale": "en-US",
            "AddDefaultLocation": "No",
            "EnableRestApiAccess": True,
        }
        return self._make_request("POST", endpoint, payload=payload)

    def create_new_enrollment_user(self, username, password, first_name, last_name, email, location_group_id):
        """Create a new enrollment user."""
        endpoint = "/system/users/adduser"
        payload = {
            "UserName": username,
            "Password": password,
            "FirstName": first_name,
            "LastName": last_name,
            "Status": "True",
            "Email": email,
            "SecurityType": 2,
            "LocationGroupId": location_group_id,
            "Role": "Basic Access",
            "MessageType": "None",
        }
        return self._make_request("POST", endpoint, payload=payload)

    def get_children_organization_groups_from_parent(self, location_group_id):
        """Get all child organization groups from parent location group ID."""
        endpoint = f"/system/groups/{location_group_id}/children"
        return self._make_request("GET", endpoint)

    def add_user_to_user_group(self, user_id, user_group_id):
        """Add a user to a user group."""
        endpoint = f"/system/usergroups/{user_group_id}/user/{user_id}/addusertogroup"
        return self._make_request("POST", endpoint)

    def remove_user_from_custom_group(self, user_group, user_id):
        """Remove a user from a custom group."""
        endpoint = f"/system/usergroups/{user_group}/user/{user_id}/removeuserfromgroup"
        return self._make_request("POST", endpoint)

    def get_user_account(self, user_id):
        """Get user account information by user ID."""
        endpoint = f"/system/users/{user_id}"
        return self._make_request("GET", endpoint)

    def update_user_account(self, user_id, json_data):
        """Update a user's account."""
        endpoint = f"/system/users/{user_id}/update"
        return self._make_request("POST", endpoint, payload=json_data)

    def search_for_organization_group(self, og_name):
        """Search for an organizational group by name."""
        endpoint = f"/system/groups/search?groupid={og_name}"
        return self._make_request("GET", endpoint)

    def get_api_url(self):
        """Get the API URL."""
        return self.apiurl