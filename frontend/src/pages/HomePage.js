import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: 'Comprehensive Assessment',
      description: 'Multi-step evaluation covering personal details, physical attributes, education, and Officer Like Qualities (OLQ)',
    },
    {
      title: 'AI-Powered Recommendations',
      description: 'Hybrid deterministic and machine learning system for accurate career path suggestions',
    },
    {
      title: 'Personalized Study Plan',
      description: 'Customized syllabus and timetable based on your target date and available study hours',
    },
    {
      title: 'Curated Resources',
      description: 'Access to books, courses, and materials specific to your recommended roles',
    },
    {
      title: 'Transparent Analysis',
      description: 'Detailed explanation of recommendations with feature importance and reasoning',
    },
    {
      title: 'PDF Export',
      description: 'Download your complete career recommendation report for offline reference',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-700 to-primary-900 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold mb-6">
              Find Your Ideal Career in Defence & Civil Services
            </h1>
            <p className="text-xl mb-8 text-primary-100">
              AI-powered career recommendation system that evaluates your profile and suggests the best career paths with personalized study plans
            </p>
            <button
              onClick={() => navigate('/assessment')}
              className="bg-white text-primary-700 font-bold py-4 px-8 rounded-lg text-lg hover:bg-primary-50 transition-colors duration-200 shadow-lg"
            >
              Start Your Assessment
            </button>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
            How It Works
          </h2>
          
          <div className="max-w-5xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary-700 text-2xl font-bold">1</span>
                </div>
                <h3 className="font-semibold text-lg mb-2">Complete Assessment</h3>
                <p className="text-gray-600 text-sm">
                  Fill multi-step form with personal, physical, and education details
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary-700 text-2xl font-bold">2</span>
                </div>
                <h3 className="font-semibold text-lg mb-2">Take OLQ Test</h3>
                <p className="text-gray-600 text-sm">
                  Answer 10 situational questions to assess leadership qualities
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary-700 text-2xl font-bold">3</span>
                </div>
                <h3 className="font-semibold text-lg mb-2">Get Recommendations</h3>
                <p className="text-gray-600 text-sm">
                  Receive AI-powered career suggestions with detailed analysis
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary-700 text-2xl font-bold">4</span>
                </div>
                <h3 className="font-semibold text-lg mb-2">Start Preparing</h3>
                <p className="text-gray-600 text-sm">
                  Access personalized study plan and curated resources
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
            Key Features
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {features.map((feature, index) => (
              <div key={index} className="card">
                <h3 className="text-xl font-semibold mb-3 text-primary-700">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Career Paths Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
            Career Paths We Cover
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="card text-center">
              <div className="text-4xl mb-4">🎖️</div>
              <h3 className="text-xl font-semibold mb-3">Defence Officer</h3>
              <p className="text-gray-600 text-sm mb-4">
                NDA, CDS, AFCAT, TGC, and other officer entry schemes
              </p>
              <ul className="text-sm text-gray-600 text-left space-y-1">
                <li>• Indian Army</li>
                <li>• Indian Navy</li>
                <li>• Indian Air Force</li>
              </ul>
            </div>
            
            <div className="card text-center">
              <div className="text-4xl mb-4">🪖</div>
              <h3 className="text-xl font-semibold mb-3">Enlisted Roles</h3>
              <p className="text-gray-600 text-sm mb-4">
                Soldier, Sailor, Airman positions and Agniveer scheme
              </p>
              <ul className="text-sm text-gray-600 text-left space-y-1">
                <li>• Soldier GD</li>
                <li>• Technical Entries</li>
                <li>• Agniveer</li>
              </ul>
            </div>
            
            <div className="card text-center">
              <div className="text-4xl mb-4">🏛️</div>
              <h3 className="text-xl font-semibold mb-3">Civil Services</h3>
              <p className="text-gray-600 text-sm mb-4">
                UPSC CSE and State Civil Services examinations
              </p>
              <ul className="text-sm text-gray-600 text-left space-y-1">
                <li>• IAS, IPS, IFS</li>
                <li>• State Services</li>
                <li>• Administrative Roles</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary-700 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">
            Ready to Discover Your Ideal Career Path?
          </h2>
          <p className="text-xl mb-8 text-primary-100 max-w-2xl mx-auto">
            Take the assessment now and receive personalized recommendations with a complete study plan
          </p>
          <button
            onClick={() => navigate('/assessment')}
            className="bg-white text-primary-700 font-bold py-4 px-8 rounded-lg text-lg hover:bg-primary-50 transition-colors duration-200 shadow-lg"
          >
            Begin Assessment
          </button>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
