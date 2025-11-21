import React from 'react';
import { useForm } from 'react-hook-form';

const PersonalDetailsForm = ({ onSubmit }) => {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const indianStates = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
    'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Puducherry', 'Chandigarh',
    'Andaman and Nicobar Islands', 'Dadra and Nagar Haveli', 'Daman and Diu',
    'Lakshadweep'
  ];

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="label">Full Name *</label>
          <input
            type="text"
            className="input-field"
            {...register('full_name', {
              required: 'Full name is required',
              minLength: { value: 2, message: 'Name must be at least 2 characters' }
            })}
          />
          {errors.full_name && <p className="error-text">{errors.full_name.message}</p>}
        </div>

        <div>
          <label className="label">Email *</label>
          <input
            type="email"
            className="input-field"
            {...register('email', {
              required: 'Email is required',
              pattern: { value: /^\S+@\S+$/i, message: 'Invalid email address' }
            })}
          />
          {errors.email && <p className="error-text">{errors.email.message}</p>}
        </div>

        <div>
          <label className="label">Phone Number *</label>
          <input
            type="tel"
            className="input-field"
            placeholder="+919876543210"
            {...register('phone', {
              required: 'Phone number is required',
              pattern: { value: /^\+?[1-9]\d{9,14}$/, message: 'Invalid phone number' }
            })}
          />
          {errors.phone && <p className="error-text">{errors.phone.message}</p>}
        </div>

        <div>
          <label className="label">Date of Birth *</label>
          <input
            type="date"
            className="input-field"
            max={new Date().toISOString().split('T')[0]}
            {...register('date_of_birth', { required: 'Date of birth is required' })}
          />
          {errors.date_of_birth && <p className="error-text">{errors.date_of_birth.message}</p>}
        </div>

        <div>
          <label className="label">Gender *</label>
          <select
            className="input-field"
            {...register('gender', { required: 'Gender is required' })}
          >
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
          {errors.gender && <p className="error-text">{errors.gender.message}</p>}
        </div>

        <div>
          <label className="label">Nationality *</label>
          <input
            type="text"
            className="input-field"
            defaultValue="Indian"
            {...register('nationality', { required: 'Nationality is required' })}
          />
          {errors.nationality && <p className="error-text">{errors.nationality.message}</p>}
        </div>

        <div>
          <label className="label">State *</label>
          <select
            className="input-field"
            {...register('state', { required: 'State is required' })}
          >
            <option value="">Select State</option>
            {indianStates.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
          {errors.state && <p className="error-text">{errors.state.message}</p>}
        </div>

        <div>
          <label className="label">City *</label>
          <input
            type="text"
            className="input-field"
            {...register('city', { required: 'City is required' })}
          />
          {errors.city && <p className="error-text">{errors.city.message}</p>}
        </div>
      </div>

      <div className="flex justify-end">
        <button type="submit" className="btn-primary">
          Next: Physical Details
        </button>
      </div>
    </form>
  );
};

export default PersonalDetailsForm;
