from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from device_failed_product import DeviceFailedProduct  # Assuming DeviceFailedProduct is in a separate module


class DeviceFailedProductDTO(BaseModel):
    device_failed_product_list: Dict[str, DeviceFailedProduct] = Field(default_factory=dict)
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: List[dict]):
        """Factory method to create an instance from API response."""
        if not any("errorCode" in failed_device for failed_device in api_response):
            device_failed_product_list = {
                failed_device["DeviceId"]: DeviceFailedProduct(
                    device_id=failed_device["DeviceId"],
                    name=failed_device["Name"],
                    last_job_status=failed_device["LastJobStatus"]
                )
                for failed_device in api_response
            }
            return cls(device_failed_product_list=device_failed_product_list, success=True)

        if "errorCode" in api_response[0]:
            error_message = f"Error code: {api_response[0]['errorCode']} Error Message: {api_response[0].get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceFailedProductDTO Missing Values")

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_device_failed_product_list(self) -> Dict[str, DeviceFailedProduct]:
        """Getter for device_failed_product_list."""
        return self.device_failed_product_list


# Example usage
try:
    api_response = [
        {"DeviceId": "12345", "Name": "Test Device 1", "LastJobStatus": "Failed"},
        {"DeviceId": "67890", "Name": "Test Device 2", "LastJobStatus": "Timeout"}
    ]
    dto = DeviceFailedProductDTO.from_api_response(api_response)
    print(dto.success)
    for device_id, failed_device in dto.device_failed_product_list.items():
        print(f"Device ID: {device_id}, Name: {failed_device.name}, Last Job Status: {failed_device.last_job_status}")
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = [{"errorCode": "404", "message": "No failed devices found"}]
    dto = DeviceFailedProductDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
