/**
 * Defines the shape of the data for the user sign-up form.
 * This interface is used for state management in the frontend component
 * and matches the Pydantic model in the gateway service.
 */
export interface SignUpFormData {
  companyNameKorean: string;
  companyNameEnglish: string;
  companyAddressKorean: string;
  companyAddressEnglish: string;
  representativeName: string;
  contactPersonName: string;
  contactPersonTitle: string;
  contactPersonDepartment: string;
  contactPersonEmail: string;
  contactPersonPhone: string;
  defaultCommunicationLanguage: string;
  allowDomainSignUp: boolean;
  adminAccountEmail: string;
  adminAccountPassword: string;
}
