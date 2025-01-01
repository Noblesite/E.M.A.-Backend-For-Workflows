from pydantic import BaseModel
from typing import Optional, Union


class CreateNewRelayServerDTO(BaseModel):
    relay_server_id: Union[str, dict, None] = None
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if not api_response.get("errorCode"):
            return cls(
                success=True,
                relay_server_id=api_response.get("Value") or api_response
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("CreateNewRelayServerDTO Missing Values")

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_relay_server_id(self) -> Union[str, dict, None]:
        """Getter for relay_server_id."""
        return self.relay_server_id


# Example usage
try:
    api_response = {
        "Value": "RELAY123"
    }
    dto = CreateNewRelayServerDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.relay_server_id)
except ValueError as e:
    print(f"Error: {e}")
