import React from 'react';

const ProgressBar = ({ currentStep, totalSteps, steps }) => {
  return (
    <div className="w-full mb-8">
      <div className="flex justify-between mb-2">
        {steps.map((step, index) => (
          <div
            key={index}
            className={`text-sm font-medium ${
              index < currentStep
                ? 'text-primary-600'
                : index === currentStep
                ? 'text-primary-700 font-semibold'
                : 'text-gray-400'
            }`}
          >
            {step}
          </div>
        ))}
      </div>
      
      <div className="relative">
        <div className="overflow-hidden h-2 text-xs flex rounded-full bg-gray-200">
          <div
            style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
            className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-primary-600 transition-all duration-500"
          />
        </div>
        
        <div className="flex justify-between absolute top-0 w-full" style={{ marginTop: '-4px' }}>
          {steps.map((_, index) => (
            <div
              key={index}
              className={`w-4 h-4 rounded-full border-2 ${
                index <= currentStep
                  ? 'bg-primary-600 border-primary-600'
                  : 'bg-white border-gray-300'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProgressBar;
