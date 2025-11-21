import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import LoadingSpinner from '../components/LoadingSpinner';
import { studyPlanService, recommendationService } from '../services/api';

const StudyPlanPage = () => {
  const { recommendationId, planId } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { errors } } = useForm();
  
  const [studyPlan, setStudyPlan] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(true);
  const [availableExams, setAvailableExams] = useState([]);

  useEffect(() => {
    if (planId) {
      loadStudyPlan();
    } else if (recommendationId) {
      loadRecommendation();
    }
    loadAvailableExams();
  }, [planId, recommendationId]);

  const loadAvailableExams = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/study-plan/exams');
      const data = await response.json();
      setAvailableExams(data.exams || []);
    } catch (err) {
      console.error('Failed to load exams:', err);
    }
  };

  const loadRecommendation = async () => {
    try {
      const data = await recommendationService.getRecommendation(recommendationId);
      setRecommendation(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load recommendation');
      setLoading(false);
    }
  };

  const loadStudyPlan = async () => {
    try {
      const data = await studyPlanService.getStudyPlan(planId);
      setStudyPlan(data);
      setShowForm(false);
      setLoading(false);
    } catch (err) {
      setError('Failed to load study plan');
      setLoading(false);
    }
  };

  const onSubmit = async (data) => {
    setGenerating(true);
    setError(null);
    try {
      const planData = await studyPlanService.generateStudyPlan({
        recommendation_id: recommendationId,
        target_date: data.target_date,
        hours_per_day: parseFloat(data.hours_per_day),
        preferred_study_times: [],
        exam_type: data.exam_type || null
      });
      setStudyPlan(planData);
      setShowForm(false);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate study plan');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <LoadingSpinner message="Loading..." />
      </div>
    );
  }

  if (error && !showForm) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <p className="text-red-600 mb-4">{error}</p>
        <button onClick={() => navigate(-1)} className="btn-primary">
          Go Back
        </button>
      </div>
    );
  }

  if (showForm) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="card">
          <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
            Create Your Study Plan
          </h1>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="label">Target Exam Date *</label>
              <input
                type="date"
                className="input-field"
                min={new Date(Date.now() + 86400000).toISOString().split('T')[0]}
                {...register('target_date', { required: 'Target date is required' })}
              />
              {errors.target_date && <p className="error-text">{errors.target_date.message}</p>}
            </div>

            <div>
              <label className="label">Hours Available Per Day *</label>
              <input
                type="number"
                step="0.5"
                className="input-field"
                placeholder="e.g., 5"
                {...register('hours_per_day', {
                  required: 'Hours per day is required',
                  min: { value: 1, message: 'Minimum 1 hour per day' },
                  max: { value: 16, message: 'Maximum 16 hours per day' }
                })}
              />
              {errors.hours_per_day && <p className="error-text">{errors.hours_per_day.message}</p>}
              <p className="text-sm text-gray-500 mt-1">
                Be realistic about how many hours you can dedicate daily
              </p>
            </div>

            <div>
              <label className="label">Select Exam *</label>
              <select
                className="input-field"
                {...register('exam_type', { required: 'Please select an exam' })}
              >
                <option value="">-- Choose Exam --</option>
                {availableExams.map((exam) => (
                  <option key={exam.exam_code} value={exam.exam_code}>
                    {exam.exam_name} ({exam.conducting_body})
                  </option>
                ))}
              </select>
              {errors.exam_type && <p className="error-text">{errors.exam_type.message}</p>}
              <p className="text-sm text-gray-500 mt-1">
                Study plan will be customized for your selected exam
              </p>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-semibold text-blue-800 mb-2">What you'll get:</h3>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Complete syllabus breakdown by topics</li>
                <li>• Day-by-day study schedule</li>
                <li>• Weekly milestones and goals</li>
                <li>• Time allocation for each subject</li>
                <li>• Revision and practice schedules</li>
              </ul>
            </div>

            <div className="flex justify-between">
              <button
                type="button"
                onClick={() => navigate(-1)}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={generating}
                className="btn-primary"
              >
                {generating ? 'Generating...' : 'Generate Study Plan'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  // Add safety check
  if (!studyPlan) {
    return (
      <div className="container mx-auto px-4 py-8">
        <LoadingSpinner message="Loading study plan..." />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Your Personalized Study Plan
        </h1>
        <p className="text-gray-600">
          A comprehensive roadmap to help you achieve your goals
        </p>
      </div>

      {/* Overview Card */}
      <div className="card mb-8 bg-gradient-to-r from-primary-600 to-primary-700 text-white">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
          <div>
            <div className="text-3xl font-bold mb-2">{studyPlan.total_days || 0}</div>
            <div className="text-primary-100">Days</div>
          </div>
          <div>
            <div className="text-3xl font-bold mb-2">{studyPlan.hours_per_day || 0}</div>
            <div className="text-primary-100">Hours/Day</div>
          </div>
          <div>
            <div className="text-3xl font-bold mb-2">{studyPlan.total_hours || 0}</div>
            <div className="text-primary-100">Total Hours</div>
          </div>
          <div>
            <div className="text-3xl font-bold mb-2">{studyPlan.modules?.length || 0}</div>
            <div className="text-primary-100">Modules</div>
          </div>
        </div>
      </div>

      {/* Study Modules */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-6">Study Modules</h2>
        <div className="space-y-4">
          {studyPlan.modules && studyPlan.modules.length > 0 ? (
            studyPlan.modules.map((module, index) => (
              <div key={index} className="card border-l-4 border-primary-600">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-800">{module.module_name}</h3>
                    <p className="text-sm text-gray-500">Week {module.week_number}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-primary-600">
                      {module.estimated_hours}h
                    </div>
                    <p className="text-sm text-gray-500">Study Time</p>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-semibold mb-2 text-gray-700">Topics:</h4>
                  <div className="flex flex-wrap gap-2">
                    {module.topics && module.topics.map((topic, idx) => (
                      <span
                        key={idx}
                        className="bg-primary-50 text-primary-700 px-3 py-1 rounded-full text-sm"
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No modules available</p>
          )}
        </div>
      </div>

      {/* Milestones */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-6">Key Milestones</h2>
        <div className="space-y-4">
          {studyPlan.milestones && studyPlan.milestones.length > 0 ? (
            studyPlan.milestones.map((milestone, index) => (
              <div key={index} className="card flex items-start space-x-4">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                  milestone.type === 'exam' ? 'bg-red-500' :
                  milestone.type === 'assessment' ? 'bg-yellow-500' :
                  milestone.type === 'final_prep' ? 'bg-orange-500' :
                  'bg-primary-500'
                } text-white font-bold`}>
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-lg text-gray-800">{milestone.title}</h3>
                  <p className="text-gray-600 text-sm mb-1">{milestone.description}</p>
                  <p className="text-primary-600 font-medium text-sm">
                    {new Date(milestone.date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </p>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No milestones available</p>
          )}
        </div>
      </div>

      {/* Daily Schedule Preview */}
      <div className="card">
        <h2 className="text-2xl font-semibold mb-6">Daily Schedule (First 7 Days)</h2>
        <div className="space-y-3">
          {studyPlan.daily_schedule && studyPlan.daily_schedule.length > 0 ? (
            studyPlan.daily_schedule.slice(0, 7).map((day, index) => (
              <div key={index} className="bg-gray-50 p-4 rounded-lg">
                <div className="flex justify-between items-start mb-2">
                  <div className="font-semibold text-gray-800">
                    Day {index + 1} - {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </div>
                  <div className="text-sm text-gray-600">{day.hours_allocated}h</div>
                </div>
                <div className="text-sm text-gray-600">
                  <div className="font-medium mb-1">Topics:</div>
                  <ul className="list-disc list-inside space-y-1">
                    {day.topics_covered && day.topics_covered.slice(0, 3).map((topic, idx) => (
                      <li key={idx}>{topic}</li>
                    ))}
                    {day.topics_covered && day.topics_covered.length > 3 && (
                      <li className="text-gray-500">... and {day.topics_covered.length - 3} more</li>
                    )}
                  </ul>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No daily schedule available</p>
          )}
        </div>
        <p className="text-sm text-gray-500 mt-4 text-center">
          Complete schedule includes all {studyPlan.total_days || 0} days
        </p>
      </div>

      {/* Action Buttons */}
      <div className="card bg-gray-50 mt-8">
        <div className="flex flex-wrap gap-4 justify-center">
          <button onClick={() => navigate(-1)} className="btn-primary">
            View Recommendations
          </button>
          <button onClick={() => navigate('/')} className="btn-secondary">
            Back to Home
          </button>
        </div>
      </div>
    </div>
  );
};

export default StudyPlanPage;
