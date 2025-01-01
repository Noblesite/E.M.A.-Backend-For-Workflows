from pydantic import BaseModel, Field
from typing import List, Optional
from device_product_status_dto import DeviceProductStatusDTO  # Assuming DeviceProductStatusDTO is in a separate module


class DeviceProductStatusListDTO(BaseModel):
    device_product_status_dto_list: List[DeviceProductStatusDTO] = Field(default_factory=list)
    page: Optional[int] = None
    page_size: Optional[int] = None
    total: Optional[int] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: List[dict]):
        """Factory method to create an instance from API response."""
        if api_response:
            device_product_status_dto_list = [
                DeviceProductStatusDTO.from_api_response(status)
                for status in api_response
                if DeviceProductStatusDTO.from_api_response(status).success
            ]
            return cls(
                device_product_status_dto_list=device_product_status_dto_list,
                success=True
            )

        return cls(
            success=False,
            error_code="DeviceProductStatusListDTO mapObject Error: No devices assigned to the product"
        )

    def get_device_product_status_dto_list(self) -> List[DeviceProductStatusDTO]:
        """Getter for device_product_status_dto_list."""
        return self.device_product_status_dto_list

    def get_page(self) -> Optional[int]:
        """Getter for page."""
        return self.page

    def get_page_size(self) -> Optional[int]:
        """Getter for page_size."""
        return self.page_size

    def get_total(self) -> Optional[int]:
        """Getter for total."""
        return self.total

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success


# Example usage
try:
    api_response = [
        {"DeviceId": "12345", "Name": "Test Device 1", "LastJobStatus": "Success"},
        {"DeviceId": "67890", "Name": "Test Device 2", "LastJobStatus": "Failed"}
    ]
    dto = DeviceProductStatusListDTO.from_api_response(api_response)
    print(dto.success)
    for device_status in dto.device_product_status_dto_list:
        print(f"Device ID: {device_status.device_id}, Name: {device_status.name}, Status: {device_status.last_job_status}")
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = []
    dto = DeviceProductStatusListDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.error_code)
except ValueError as e:
    print(f"Error: {e}")
