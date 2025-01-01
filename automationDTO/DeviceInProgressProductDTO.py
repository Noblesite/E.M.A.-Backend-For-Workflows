from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from device_in_progress_product import DeviceInProgressProduct  # Assuming DeviceInProgressProduct is in a separate module


class DeviceInProgressProductDTO(BaseModel):
    device_in_progress_product_list: Dict[str, DeviceInProgressProduct] = Field(default_factory=dict)
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: List[dict]):
        """Factory method to create an instance from API response."""
        if not any("errorCode" in device for device in api_response):
            device_in_progress_product_list = {
                device["DeviceId"]: DeviceInProgressProduct(
                    device_id=device["DeviceId"],
                    name=device["Name"],
                    last_job_status=device["LastJobStatus"]
                )
                for device in api_response
            }
            return cls(
                device_in_progress_product_list=device_in_progress_product_list,
                success=True
            )

        if "errorCode" in api_response[0]:
            error_message = f"Error code: {api_response[0]['errorCode']} Error Message: {api_response[0].get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceInProgressProductDTO Missing Values")

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_device_in_progress_product_list(self) -> Dict[str, DeviceInProgressProduct]:
        """Getter for device_in_progress_product_list."""
        return self.device_in_progress_product_list


# Example usage
try:
    api_response = [
        {"DeviceId": "12345", "Name": "Test Device 1", "LastJobStatus": "In Progress"},
        {"DeviceId": "67890", "Name": "Test Device 2", "LastJobStatus": "Retrying"}
    ]
    dto = DeviceInProgressProductDTO.from_api_response(api_response)
    print(dto.success)
    for device_id, device in dto.device_in_progress_product_list.items():
        print(f"Device ID: {device_id}, Name: {device.name}, Last Job Status: {device.last_job_status}")
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = [{"errorCode": "404", "message": "No devices found"}]
    dto = DeviceInProgressProductDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
