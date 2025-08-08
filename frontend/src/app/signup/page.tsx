"use client";

import React, { useState } from 'react';
import axios from 'axios';
import { SignUpFormData } from '../../types';
import styles from './signup.module.css';

const GATEWAY_URL = 'http://localhost:8000/api/v1/companies/signup';

const SignUpPage = () => {
  const [formData, setFormData] = useState<SignUpFormData>({
    companyNameKorean: '',
    companyNameEnglish: '',
    companyAddressKorean: '',
    companyAddressEnglish: '',
    representativeName: '',
    contactPersonName: '',
    contactPersonTitle: '',
    contactPersonDepartment: '',
    contactPersonEmail: '',
    contactPersonPhone: '',
    defaultCommunicationLanguage: 'Korean',
    allowDomainSignUp: false,
    adminAccountEmail: '',
    adminAccountPassword: '',
  });

  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;

    if (type === 'checkbox') {
      const { checked } = e.target as HTMLInputElement;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setMessage(null);
    try {
      const response = await axios.post(GATEWAY_URL, formData);
      setMessage({ type: 'success', text: 'Sign-up successful! Response: ' + JSON.stringify(response.data) });
      // Optionally, reset form
      // setFormData({ ...initial state... });
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'An unexpected error occurred.';
      setMessage({ type: 'error', text: 'Sign-up failed: ' + (typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg)) });
    }
  };

  return (
    <div className={styles.formContainer}>
      <h2>Create a New Company Account</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <fieldset className={styles.fieldset}>
          <legend className={styles.legend}>Company Information</legend>
          {/* Company Fields */}
          <div className={styles.inputGroup}><label className={styles.label}>Company Name (Korean)</label><input type="text" name="companyNameKorean" value={formData.companyNameKorean} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Company Name (English)</label><input type="text" name="companyNameEnglish" value={formData.companyNameEnglish} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Company Address (Korean)</label><input type="text" name="companyAddressKorean" value={formData.companyAddressKorean} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Company Address (English)</label><input type="text" name="companyAddressEnglish" value={formData.companyAddressEnglish} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Representative Name</label><input type="text" name="representativeName" value={formData.representativeName} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Language</label><select name="defaultCommunicationLanguage" value={formData.defaultCommunicationLanguage} onChange={handleChange} className={styles.select}><option value="Korean">Korean</option><option value="English">English</option></select></div>
        </fieldset>

        <fieldset className={styles.fieldset}>
          <legend className={styles.legend}>Contact Person</legend>
          {/* Contact Person Fields */}
          <div className={styles.inputGroup}><label className={styles.label}>Name</label><input type="text" name="contactPersonName" value={formData.contactPersonName} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Title</label><input type="text" name="contactPersonTitle" value={formData.contactPersonTitle} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Department</label><input type="text" name="contactPersonDepartment" value={formData.contactPersonDepartment} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Email</label><input type="email" name="contactPersonEmail" value={formData.contactPersonEmail} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Phone</label><input type="tel" name="contactPersonPhone" value={formData.contactPersonPhone} onChange={handleChange} className={styles.input} required /></div>
        </fieldset>

        <fieldset className={styles.fieldset}>
          <legend className={styles.legend}>Admin Account</legend>
          {/* Admin Account Fields */}
          <div className={styles.inputGroup}><label className={styles.label}>Admin Email</label><input type="email" name="adminAccountEmail" value={formData.adminAccountEmail} onChange={handleChange} className={styles.input} required /></div>
          <div className={styles.inputGroup}><label className={styles.label}>Admin Password</label><input type="password" name="adminAccountPassword" value={formData.adminAccountPassword} onChange={handleChange} className={styles.input} required /></div>
          <div className={`${styles.inputGroup} ${styles.fullWidth} ${styles.checkboxGroup}`}><input type="checkbox" name="allowDomainSignUp" checked={formData.allowDomainSignUp} onChange={handleChange} /><label className={styles.label}>Allow Sign-up with Company Domain</label></div>
        </fieldset>

        <button type="submit" className={styles.button}>Sign Up</button>

        {message && (
          <div className={`${styles.message} ${message.type === 'success' ? styles.success : styles.error}`}>
            {message.text}
          </div>
        )}
      </form>
    </div>
  );
};

export default SignUpPage;
