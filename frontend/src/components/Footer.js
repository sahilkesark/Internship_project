import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-800 text-gray-300 mt-12">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">About</h3>
            <p className="text-sm">
              AI-powered career recommendation system designed to help candidates find the right path in Defence and Civil Services.
            </p>
          </div>
          
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="https://www.upsc.gov.in" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
                  UPSC Official Website
                </a>
              </li>
              <li>
                <a href="https://joinindianarmy.nic.in" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
                  Indian Army Recruitment
                </a>
              </li>
              <li>
                <a href="https://indianairforce.nic.in" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
                  Indian Air Force
                </a>
              </li>
              <li>
                <a href="https://www.indiannavy.nic.in" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
                  Indian Navy
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Disclaimer</h3>
            <p className="text-sm">
              This is a recommendation system. Always verify eligibility criteria and requirements from official sources before applying.
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-sm">
          <p>&copy; {currentYear} Career Recommendation System. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
