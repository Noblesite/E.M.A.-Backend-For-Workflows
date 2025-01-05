from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class DynamicNewDeploymentObject(BaseModel):
    basic_user_time_zone: Optional[str] = None
    basic_user_name: Optional[str] = None
    basic_user_email: Optional[EmailStr] = None
    basic_user_password: Optional[str] = None
    organizational_group_id: Optional[str] = None
    basic_user_display_name: Optional[str] = None
    basic_user_first_name: Optional[str] = None
    basic_user_last_name: Optional[str] = None
    organization_group_name: Optional[str] = None
    organization_group_enrollment_id: Optional[str] = None
    orginzation_group_id: Optional[str] = None
    basic_user_id: Optional[str] = None
    time_zone_user_group_id: Optional[str] = None

    class Config:
        validate_assignment = True

    def set_last_name(self, last_name: str):
        self.basic_user_last_name = last_name

    def set_first_name(self, first_name: str):
        self.basic_user_first_name = first_name

    def set_basic_user_email(self, email: str):
        self.basic_user_email = email

    def set_basic_user_name(self, name: str):
        self.basic_user_name = name

    def set_basic_user_password(self, password: str):
        self.basic_user_password = password

    def set_basic_user_time_zone(self, time_zone: str):
        self.basic_user_time_zone = time_zone

    def set_organizational_group_id(self, group_id: str):
        self.organizational_group_id = group_id

    def set_organization_group_name(self, group_name: str):
        self.organization_group_name = group_name

    def set_organization_group_enrollment_id(self, enrollment_id: str):
        self.organization_group_enrollment_id = enrollment_id

    def set_basic_user_id(self, user_id: str):
        self.basic_user_id = user_id

    def set_time_zone_user_group_id(self, group_id: str):
        self.time_zone_user_group_id = group_id