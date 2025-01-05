from sys_rest_controller import SYSRestController
from organization_group_dto import OrganizationGroupDTO
from csv_processor import read_csv

def process_organization_groups(csv_file_path, headers):
    sys_controller = SYSRestController(headers)
    org_groups = read_csv(csv_file_path)
    
    for org_group in org_groups:
        payload = {
            "GroupName": org_group["GroupName"],
            "ParentID": org_group["ParentID"],
            "GroupType": org_group["GroupType"],
            # Add other required fields here
        }

        status_code, response_data = sys_controller.create_organization_group(payload)
        response_dto = OrganizationGroupDTO(response_data)

        if status_code == 200:
            print(f"Success: {response_dto}")
        else:
            print(f"Failed to create group. Error: {response_dto}")

if __name__ == "__main__":
    csv_file_path = "path_to_your_csv_file.csv"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "aw-tenant-code": "YOUR_TENANT_CODE",
        "Content-Type": "application/json",
    }
    process_organization_groups(csv_file_path, headers)