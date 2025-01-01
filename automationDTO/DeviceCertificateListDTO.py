from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from device_certificate_dto import DeviceCertificateDTO  # Assuming DeviceCertificateDTO is in a separate module


class DeviceCertificateListDTO(BaseModel):
    device_certificates_list: Dict[str, DeviceCertificateDTO] = Field(default_factory=dict, alias="DeviceCertificates")
    page: Optional[int] = Field(None, alias="Page")
    page_size: Optional[int] = Field(None, alias="PageSize")
    total: Optional[int] = Field(None, alias="Total")
    error_code: Optional[str] = None
    success: bool = False

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "DeviceCertificates" in api_response:
            device_certificates = {
                cert["Id"]["Value"]: DeviceCertificateDTO.from_api_response(cert)
                for cert in api_response.get("DeviceCertificates", [])
            }
            return cls(
                device_certificates_list=device_certificates,
                page=api_response.get("Page"),
                page_size=api_response.get("PageSize"),
                total=api_response.get("Total"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceCertificateListDTO Missing Values")

    def get_device_certificates_list(self) -> Dict[str, DeviceCertificateDTO]:
        """Getter for device_certificates_list."""
        return self.device_certificates_list

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
    api_response = {
        "DeviceCertificates": [
            {
                "FirstSampleTime": "2023-01-01T00:00:00Z",
                "LastSampleTime": "2023-01-15T00:00:00Z",
                "DeviceId": {"Id": {"Value": "12345"}},
                "CertificateLoaded": True,
                "Name": "Test Certificate 1",
                "ExpiresOn": "2024-01-01T00:00:00Z",
                "IssuedBy": "Cert Authority",
                "Status": "Valid",
                "Id": {"Value": "cert-12345"}
            },
            {
                "FirstSampleTime": "2023-01-02T00:00:00Z",
                "LastSampleTime": "2023-01-16T00:00:00Z",
                "DeviceId": {"Id": {"Value": "67890"}},
                "CertificateLoaded": False,
                "Name": "Test Certificate 2",
                "ExpiresOn": "2023-12-31T00:00:00Z",
                "IssuedBy": "Cert Authority 2",
                "Status": "Expired",
                "Id": {"Value": "cert-67890"}
            }
        ],
        "Total": 2,
        "Page": 1,
        "PageSize": 10
    }
    dto = DeviceCertificateListDTO.from_api_response(api_response)
    print(dto.success)
    for cert_id, cert in dto.device_certificates_list.items():
        print(f"Cert ID: {cert_id}, Name: {cert.name}, Expires On: {cert.expires_on}")
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"errorCode": "404", "message": "No certificates found"}
    dto = DeviceCertificateListDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
