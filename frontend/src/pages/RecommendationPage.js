import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';
import { recommendationService } from '../services/api';

const RecommendationPage = () => {
  const { recommendationId } = useParams();
  const navigate = useNavigate();
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadRecommendation();
  }, [recommendationId]);

  const loadRecommendation = async () => {
    try {
      const data = await recommendationService.getRecommendation(recommendationId);
      setRecommendation(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load recommendations');
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    try {
      const blob = await recommendationService.exportPDF(recommendationId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `career_recommendation_${recommendationId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      alert('Failed to export PDF');
    }
  };

  const handleCreateStudyPlan = () => {
    navigate(`/study-plan/new/${recommendationId}`);
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <LoadingSpinner message="Loading your recommendations..." />
      </div>
    );
  }

  if (error || !recommendation) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <p className="text-red-600 mb-4">{error || 'Recommendation not found'}</p>
        <button onClick={() => navigate('/')} className="btn-primary">
          Go Home
        </button>
      </div>
    );
  }

  const getOLQCategory = (score) => {
    if (score >= 80) return { label: 'Excellent', color: 'bg-green-500' };
    if (score >= 65) return { label: 'Very Good', color: 'bg-blue-500' };
    if (score >= 50) return { label: 'Good', color: 'bg-yellow-500' };
    if (score >= 35) return { label: 'Average', color: 'bg-orange-500' };
    return { label: 'Below Average', color: 'bg-red-500' };
  };

  const olqCategory = getOLQCategory(recommendation.olq_score);

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Your Career Recommendations
        </h1>
        <p className="text-gray-600">
          Based on your assessment, here are your personalized career recommendations
        </p>
      </div>

      {/* OLQ Score Card */}
      <div className="card mb-8">
        <h2 className="text-2xl font-semibold mb-4">Officer Like Qualities (OLQ) Assessment</h2>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-5xl font-bold text-primary-600 mb-2">
              {recommendation.olq_score.toFixed(1)}%
            </div>
            <div className="flex items-center space-x-2">
              <span className={`inline-block px-3 py-1 rounded-full text-white text-sm font-semibold ${olqCategory.color}`}>
                {olqCategory.label}
              </span>
            </div>
          </div>
          <div className="flex-1 ml-8">
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className="bg-primary-600 h-4 rounded-full transition-all duration-500"
                style={{ width: `${recommendation.olq_score}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Explanation */}
      <div className="card mb-8 bg-primary-50 border border-primary-200">
        <h3 className="text-xl font-semibold mb-3 text-primary-800">Career Path Analysis</h3>
        <p className="text-gray-700 leading-relaxed">{recommendation.explanation}</p>
      </div>

      {/* Recommendations */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-6">Recommended Career Opportunities</h2>
        <div className="space-y-6">
          {recommendation.recommendations.map((rec, index) => (
            <div key={index} className="card border-l-4 border-primary-600">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">{rec.role_name}</h3>
                  <p className="text-primary-600 font-medium">{rec.entry_scheme}</p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-primary-600">
                    {rec.match_score.toFixed(0)}%
                  </div>
                  <p className="text-sm text-gray-500">Match Score</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-sm text-gray-600">Age Range</p>
                  <p className="font-semibold">{rec.min_age} - {rec.max_age} years</p>
                </div>
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-sm text-gray-600">Education Required</p>
                  <p className="font-semibold">{rec.education_requirement}</p>
                </div>
              </div>

              <div className="mb-4">
                <h4 className="font-semibold mb-2">Selection Process:</h4>
                <ul className="space-y-1">
                  {rec.selection_process.map((step, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-primary-600 mr-2">•</span>
                      <span className="text-gray-700">{step}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mb-4 p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold mb-2 text-blue-800">Why This Role:</h4>
                <p className="text-gray-700">{rec.reasoning}</p>
              </div>

              {rec.feature_importance && Object.keys(rec.feature_importance).length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Key Factors:</h4>
                  <div className="space-y-2">
                    {Object.entries(rec.feature_importance).map(([feature, importance]) => (
                      <div key={feature}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-700">{feature}</span>
                          <span className="font-semibold">{(importance * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full"
                            style={{ width: `${importance * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="card bg-gray-50">
        <h3 className="text-xl font-semibold mb-4">Next Steps</h3>
        <div className="flex flex-wrap gap-4">
          <button onClick={handleCreateStudyPlan} className="btn-primary">
            Create Study Plan
          </button>
          <button onClick={handleExportPDF} className="btn-outline">
            Download PDF Report
          </button>
          <button onClick={() => navigate('/')} className="btn-secondary">
            Back to Home
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecommendationPage;
