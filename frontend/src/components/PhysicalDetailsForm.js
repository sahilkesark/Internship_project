import React from 'react';
import { useForm } from 'react-hook-form';

const PhysicalDetailsForm = ({ onSubmit, onBack }) => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  
  const hasMedicalConditions = watch('has_medical_conditions');

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="label">Height (cm) *</label>
          <input
            type="number"
            step="0.1"
            className="input-field"
            {...register('height_cm', {
              required: 'Height is required',
              min: { value: 140, message: 'Height must be at least 140 cm' },
              max: { value: 220, message: 'Height must be less than 220 cm' }
            })}
          />
          {errors.height_cm && <p className="error-text">{errors.height_cm.message}</p>}
        </div>

        <div>
          <label className="label">Weight (kg) *</label>
          <input
            type="number"
            step="0.1"
            className="input-field"
            {...register('weight_kg', {
              required: 'Weight is required',
              min: { value: 40, message: 'Weight must be at least 40 kg' },
              max: { value: 150, message: 'Weight must be less than 150 kg' }
            })}
          />
          {errors.weight_kg && <p className="error-text">{errors.weight_kg.message}</p>}
        </div>

        <div>
          <label className="label">Left Eye Vision (6/x) *</label>
          <input
            type="number"
            step="0.1"
            className="input-field"
            placeholder="e.g., 6 for 6/6"
            {...register('eyesight_left', {
              required: 'Left eye vision is required',
              min: { value: 0, message: 'Invalid vision value' },
              max: { value: 10, message: 'Invalid vision value' }
            })}
          />
          {errors.eyesight_left && <p className="error-text">{errors.eyesight_left.message}</p>}
        </div>

        <div>
          <label className="label">Right Eye Vision (6/x) *</label>
          <input
            type="number"
            step="0.1"
            className="input-field"
            placeholder="e.g., 6 for 6/6"
            {...register('eyesight_right', {
              required: 'Right eye vision is required',
              min: { value: 0, message: 'Invalid vision value' },
              max: { value: 10, message: 'Invalid vision value' }
            })}
          />
          {errors.eyesight_right && <p className="error-text">{errors.eyesight_right.message}</p>}
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            id="has_medical_conditions"
            className="w-5 h-5 text-primary-600"
            {...register('has_medical_conditions')}
          />
          <label htmlFor="has_medical_conditions" className="text-sm font-medium text-gray-700">
            Do you have any medical conditions?
          </label>
        </div>

        {hasMedicalConditions && (
          <div>
            <label className="label">Please describe your medical conditions</label>
            <textarea
              className="input-field"
              rows="3"
              {...register('medical_conditions_description')}
            />
          </div>
        )}

        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            id="tattoos"
            className="w-5 h-5 text-primary-600"
            {...register('tattoos')}
          />
          <label htmlFor="tattoos" className="text-sm font-medium text-gray-700">
            Do you have any tattoos?
          </label>
        </div>

        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            id="previous_injuries"
            className="w-5 h-5 text-primary-600"
            {...register('previous_injuries')}
          />
          <label htmlFor="previous_injuries" className="text-sm font-medium text-gray-700">
            Have you had any major injuries in the past?
          </label>
        </div>
      </div>

      <div className="flex justify-between">
        <button type="button" onClick={onBack} className="btn-secondary">
          Back
        </button>
        <button type="submit" className="btn-primary">
          Next: Education Details
        </button>
      </div>
    </form>
  );
};

export default PhysicalDetailsForm;
