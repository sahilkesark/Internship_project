import React, { useState, useEffect } from 'react';
import { assessmentService } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const OLQTestForm = ({ onSubmit, onBack }) => {
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await assessmentService.getOLQQuestions();
      // Handle new API format with session_id and questions
      if (data.questions && data.session_id) {
        setQuestions(data.questions);
        setSessionId(data.session_id);
      } else {
        // Fallback for old format (array of questions)
        setQuestions(data);
      }
      setLoading(false);
    } catch (err) {
      setError('Failed to load questions');
      setLoading(false);
    }
  };

  const handleOptionSelect = (questionId, optionIndex) => {
    setResponses({
      ...responses,
      [questionId]: optionIndex
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Check if all questions are answered
    if (Object.keys(responses).length < questions.length) {
      alert('Please answer all questions before submitting');
      return;
    }

    // Format responses
    const formattedResponses = questions.map((q) => ({
      question_id: q.question_id,
      selected_option: responses[q.question_id]
    }));

    // Pass both responses and session_id
    onSubmit(formattedResponses, sessionId);
  };

  if (loading) {
    return <LoadingSpinner message="Loading questions..." />;
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">{error}</p>
        <button onClick={loadQuestions} className="btn-primary">
          Retry
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-6">
        <h3 className="font-semibold text-primary-800 mb-2">
          Officer Like Qualities (OLQ) Assessment
        </h3>
        <p className="text-sm text-primary-700">
          This test evaluates your leadership qualities, decision-making abilities, and situational awareness. 
          There are no right or wrong answers - choose the option that best reflects what you would do in each situation.
        </p>
      </div>

      {questions.map((question, index) => (
        <div key={question.question_id} className="border border-gray-200 rounded-lg p-6">
          <div className="mb-4">
            <span className="inline-block bg-primary-600 text-white text-sm font-semibold px-3 py-1 rounded-full mb-3">
              Question {index + 1} of {questions.length}
            </span>
            <p className="text-lg font-medium text-gray-800">{question.question}</p>
          </div>

          <div className="space-y-3">
            {question.options.map((option, optionIndex) => (
              <label
                key={optionIndex}
                className={`flex items-start p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  responses[question.question_id] === optionIndex
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-200 hover:border-primary-300'
                }`}
              >
                <input
                  type="radio"
                  name={`question-${question.question_id}`}
                  value={optionIndex}
                  checked={responses[question.question_id] === optionIndex}
                  onChange={() => handleOptionSelect(question.question_id, optionIndex)}
                  className="mt-1 mr-3"
                />
                <span className="text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        </div>
      ))}

      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-sm text-yellow-800">
          Please review your answers before submitting. Once submitted, recommendations will be generated based on your responses.
        </p>
      </div>

      <div className="flex justify-between">
        <button type="button" onClick={onBack} className="btn-secondary">
          Back
        </button>
        <button type="submit" className="btn-primary">
          Submit & Get Recommendations
        </button>
      </div>
    </form>
  );
};

export default OLQTestForm;
