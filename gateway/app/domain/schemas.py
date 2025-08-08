from pydantic import BaseModel, EmailStr

class SignUpRequest(BaseModel):
    """
    Pydantic model for validating the incoming sign-up request data.
    """
    companyNameKorean: str
    companyNameEnglish: str
    companyAddressKorean: str
    companyAddressEnglish: str
    representativeName: str
    contactPersonName: str
    contactPersonTitle: str
    contactPersonDepartment: str
    contactPersonEmail: EmailStr
    contactPersonPhone: str
    defaultCommunicationLanguage: str
    allowDomainSignUp: bool
    adminAccountEmail: EmailStr
    adminAccountPassword: str

    class Config:
        # Allows Pydantic to work with ORM models, not strictly needed for
        # request bodies but good practice. `from_attributes` is for Pydantic v2.
        from_attributes = True
        # The frontend sends camelCase, which matches the model fields.
        # If the model used snake_case, we would need an alias generator.
