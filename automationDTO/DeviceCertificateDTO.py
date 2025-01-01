from pydantic import BaseModel, Field
from typing import Optional


class DeviceCertificateDTO(BaseModel):
    first_sample_time: Optional[str] = Field(None, alias="FirstSampleTime")
    last_sample_time: Optional[str] = Field(None, alias="LastSampleTime")
    device_id: Optional[str] = Field(None, alias="DeviceId.Id.Value")
    certificate_loaded: Optional[bool] = Field(None, alias="CertificateLoaded")
    name: Optional[str] = Field(None, alias="Name")
    expires_on: Optional[str] = Field(None, alias="ExpiresOn")
    issued_by: Optional[str] = Field(None, alias="IssuedBy")
    status: Optional[str] = Field(None, alias="Status")
    cert_id: Optional[str] = Field(None, alias="Id.Value")
    success: bool = False
    error_code: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_response: dict):
        """Factory method to create an instance from API response."""
        if "FirstSampleTime" in api_response:
            return cls(
                first_sample_time=api_response.get("FirstSampleTime"),
                last_sample_time=api_response.get("LastSampleTime"),
                device_id=api_response.get("DeviceId", {}).get("Id", {}).get("Value"),
                certificate_loaded=api_response.get("CertificateLoaded"),
                name=api_response.get("Name"),
                expires_on=api_response.get("ExpiresOn"),
                issued_by=api_response.get("IssuedBy"),
                status=api_response.get("Status"),
                cert_id=api_response.get("Id", {}).get("Value"),
                success=True
            )

        if "errorCode" in api_response:
            error_message = f"Error code: {api_response['errorCode']} Error Message: {api_response.get('message', '')}"
            raise ValueError(error_message)

        raise ValueError("DeviceCertificateDTO Missing Values")

    def get_first_sample_time(self) -> Optional[str]:
        """Getter for first_sample_time."""
        return self.first_sample_time

    def get_last_sample_time(self) -> Optional[str]:
        """Getter for last_sample_time."""
        return self.last_sample_time

    def get_device_id(self) -> Optional[str]:
        """Getter for device_id."""
        return self.device_id

    def get_certificate_loaded(self) -> Optional[bool]:
        """Getter for certificate_loaded."""
        return self.certificate_loaded

    def get_name(self) -> Optional[str]:
        """Getter for name."""
        return self.name

    def get_expires_on(self) -> Optional[str]:
        """Getter for expires_on."""
        return self.expires_on

    def get_issued_by(self) -> Optional[str]:
        """Getter for issued_by."""
        return self.issued_by

    def get_status(self) -> Optional[str]:
        """Getter for status."""
        return self.status

    def get_cert_id(self) -> Optional[str]:
        """Getter for cert_id."""
        return self.cert_id

    def get_success(self) -> bool:
        """Getter for success."""
        return self.success

    def get_error_code(self) -> Optional[str]:
        """Getter for error_code."""
        return self.error_code


# Example usage
try:
    api_response = {
        "FirstSampleTime": "2023-01-01T00:00:00Z",
        "LastSampleTime": "2023-01-15T00:00:00Z",
        "DeviceId": {"Id": {"Value": "12345"}},
        "CertificateLoaded": True,
        "Name": "Test Certificate",
        "ExpiresOn": "2024-01-01T00:00:00Z",
        "IssuedBy": "Cert Authority",
        "Status": "Valid",
        "Id": {"Value": "cert-12345"}
    }
    dto = DeviceCertificateDTO.from_api_response(api_response)
    print(dto.success)
    print(dto.name)
    print(dto.expires_on)
except ValueError as e:
    print(f"Error: {e}")

try:
    api_response = {"errorCode": "404", "message": "Certificate not found"}
    dto = DeviceCertificateDTO.from_api_response(api_response)
except ValueError as e:
    print(f"Error: {e}")
