from pydantic import BaseModel, ValidationError
from typing import List, Optional


class AddDevicesToTagDTO(BaseModel):
    accepted_items: Optional[int] = None
    failed_items: Optional[int] = None
    faults: List[str] = []
    total_items: Optional[int] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if not api_response.get("errorCode"):
            return cls(
                success=True,
                accepted_items=api_response.get("AcceptedItems"),
                failed_items=api_response.get("FailedItems"),
                total_items=api_response.get("TotalItems"),
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("AddDevicesToTagDTO Missing Values")

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_accepted_items(self) -> Optional[int]:
        """Getter for accepted_items."""
        return self.accepted_items

    def get_failed_items(self) -> Optional[int]:
        """Getter for failed_items."""
        return self.failed_items

    def get_faults(self) -> List[str]:
        """Getter for faults."""
        return self.faults

    def get_total_items(self) -> Optional[int]:
        """Getter for total_items."""
        return self.total_items


# Example usage
try:
    api_response = {
        "AcceptedItems": 5,
        "FailedItems": 2,
        "TotalItems": 7,
    }
    dto = AddDevicesToTagDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.accepted_items)
    print(dto.failed_items)
except ValueError as e:
    print(f"Error: {e}")
