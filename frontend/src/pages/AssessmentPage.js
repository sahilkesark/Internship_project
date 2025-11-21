import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProgressBar from '../components/ProgressBar';
import LoadingSpinner from '../components/LoadingSpinner';
import PersonalDetailsForm from '../components/PersonalDetailsForm';
import PhysicalDetailsForm from '../components/PhysicalDetailsForm';
import EducationDetailsForm from '../components/EducationDetailsForm';
import OLQTestForm from '../components/OLQTestForm';
import { assessmentService, recommendationService } from '../services/api';

const AssessmentPage = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [assessmentId, setAssessmentId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const steps = ['Personal', 'Physical', 'Education', 'OLQ Test'];

  const handlePersonalSubmit = async (data) => {
    setLoading(true);
    setError(null);
    try {
      const response = await assessmentService.startAssessment(data);
      setAssessmentId(response.assessment_id);
      setCurrentStep(1);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start assessment');
    } finally {
      setLoading(false);
    }
  };

  const handlePhysicalSubmit = async (data) => {
    setLoading(true);
    setError(null);
    try {
      await assessmentService.updatePhysical(assessmentId, data);
      setCurrentStep(2);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save physical details');
    } finally {
      setLoading(false);
    }
  };

  const handleEducationSubmit = async (data) => {
    setLoading(true);
    setError(null);
    try {
      await assessmentService.updateEducation(assessmentId, data);
      setCurrentStep(3);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save education details');
    } finally {
      setLoading(false);
    }
  };

  const handleOLQSubmit = async (responses, sessionId) => {
    setLoading(true);
    setError(null);
    try {
      // Submit OLQ responses with session_id
      await assessmentService.submitOLQ({
        assessment_id: assessmentId,
        responses: responses,
      }, sessionId);

      // Generate recommendations
      const recommendation = await recommendationService.generateRecommendations(assessmentId);
      
      // Navigate to recommendation page
      navigate(`/recommendation/${recommendation.recommendation_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="card">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Career Assessment
        </h1>

        <ProgressBar currentStep={currentStep} totalSteps={steps.length} steps={steps} />

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {loading ? (
          <LoadingSpinner message="Processing..." />
        ) : (
          <>
            {currentStep === 0 && <PersonalDetailsForm onSubmit={handlePersonalSubmit} />}
            {currentStep === 1 && (
              <PhysicalDetailsForm onSubmit={handlePhysicalSubmit} onBack={handleBack} />
            )}
            {currentStep === 2 && (
              <EducationDetailsForm onSubmit={handleEducationSubmit} onBack={handleBack} />
            )}
            {currentStep === 3 && (
              <OLQTestForm onSubmit={handleOLQSubmit} onBack={handleBack} />
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default AssessmentPage;
