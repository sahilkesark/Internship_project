import React from 'react';
import { useForm } from 'react-hook-form';

const EducationDetailsForm = ({ onSubmit, onBack }) => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  
  const hasNCC = watch('has_ncc');

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="label">Highest Education Level *</label>
          <select
            className="input-field"
            {...register('highest_education', { required: 'Education level is required' })}
          >
            <option value="">Select Education Level</option>
            <option value="high_school">10th Standard</option>
            <option value="intermediate">12th Standard / Intermediate</option>
            <option value="bachelors">Bachelor's Degree</option>
            <option value="masters">Master's Degree</option>
            <option value="doctorate">Doctorate / PhD</option>
          </select>
          {errors.highest_education && <p className="error-text">{errors.highest_education.message}</p>}
        </div>

        <div>
          <label className="label">Stream / Field *</label>
          <select
            className="input-field"
            {...register('stream', { required: 'Stream is required' })}
          >
            <option value="">Select Stream</option>
            <option value="science">Science</option>
            <option value="commerce">Commerce</option>
            <option value="arts">Arts / Humanities</option>
            <option value="engineering">Engineering</option>
            <option value="medical">Medical</option>
            <option value="law">Law</option>
            <option value="other">Other</option>
          </select>
          {errors.stream && <p className="error-text">{errors.stream.message}</p>}
        </div>

        <div>
          <label className="label">University / Board *</label>
          <input
            type="text"
            className="input-field"
            {...register('university', { required: 'University/Board is required' })}
          />
          {errors.university && <p className="error-text">{errors.university.message}</p>}
        </div>

        <div>
          <label className="label">Graduation / Passing Year *</label>
          <input
            type="number"
            className="input-field"
            {...register('graduation_year', {
              required: 'Graduation year is required',
              min: { value: 1990, message: 'Invalid year' },
              max: { value: 2030, message: 'Invalid year' }
            })}
          />
          {errors.graduation_year && <p className="error-text">{errors.graduation_year.message}</p>}
        </div>

        <div>
          <label className="label">Percentage / CGPA *</label>
          <input
            type="number"
            step="0.01"
            className="input-field"
            placeholder="Enter percentage (e.g., 75.5)"
            {...register('percentage_or_cgpa', {
              required: 'Percentage/CGPA is required',
              min: { value: 0, message: 'Invalid percentage' },
              max: { value: 100, message: 'Invalid percentage' }
            })}
          />
          {errors.percentage_or_cgpa && <p className="error-text">{errors.percentage_or_cgpa.message}</p>}
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            id="has_ncc"
            className="w-5 h-5 text-primary-600"
            {...register('has_ncc')}
          />
          <label htmlFor="has_ncc" className="text-sm font-medium text-gray-700">
            Do you have NCC certificate?
          </label>
        </div>

        {hasNCC && (
          <div>
            <label className="label">NCC Certificate Type</label>
            <select className="input-field" {...register('ncc_certificate')}>
              <option value="">Select Certificate</option>
              <option value="A Certificate">A Certificate</option>
              <option value="B Certificate">B Certificate</option>
              <option value="C Certificate">C Certificate</option>
            </select>
          </div>
        )}

        <div>
          <label className="label">Additional Qualifications (Optional)</label>
          <p className="text-sm text-gray-500 mb-2">
            Enter any additional qualifications, certifications, or achievements (one per line)
          </p>
          <textarea
            className="input-field"
            rows="3"
            placeholder="e.g., State-level sports certificate&#10;Debate competition winner&#10;Volunteer work"
            {...register('additional_qualifications_text')}
          />
        </div>
      </div>

      <div className="flex justify-between">
        <button type="button" onClick={onBack} className="btn-secondary">
          Back
        </button>
        <button type="submit" className="btn-primary">
          Next: OLQ Test
        </button>
      </div>
    </form>
  );
};

export default EducationDetailsForm;
