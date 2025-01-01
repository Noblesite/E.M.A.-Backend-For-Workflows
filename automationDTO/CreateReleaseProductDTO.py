from pydantic import BaseModel, ValidationError
from typing import Optional


class CreateReleaseProductDTO(BaseModel):
    product_id: Optional[str] = None
    error_code: Optional[str] = None
    success: bool = False

    @classmethod
    def from_api_response(cls, api_response: str):
        """Factory method to create an instance from API response."""
        if isinstance(api_response, str) and "Successfully created" in api_response:
            try:
                tmp_string_array = api_response.split("(", 1)[1].split(")", 1)
                product_id = tmp_string_array[0]
                return cls(product_id=product_id, success=True)
            except IndexError:
                raise ValueError("Unable to parse product ID from the API response.")

        if isinstance(api_response, dict) and "errorCode" in api_response:
            error_message = f"Error code: {api_response.get('errorCode')} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("CreateReleaseProductDTO Missing Values")

    def get_product_id(self) -> Optional[str]:
        """Getter for product_id."""
        return self.product_id

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success


# Example usage
try:
    api_response = "Successfully created product (PROD12345)"
    dto = CreateReleaseProductDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.product_id)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {
        "errorCode": "500",
        "message": "Internal Server Error"
    }
    dto = CreateReleaseProductDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
