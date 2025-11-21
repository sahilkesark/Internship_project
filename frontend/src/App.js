import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import AssessmentPage from './pages/AssessmentPage';
import RecommendationPage from './pages/RecommendationPage';
import StudyPlanPage from './pages/StudyPlanPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/assessment" element={<AssessmentPage />} />
            <Route path="/recommendation/:recommendationId" element={<RecommendationPage />} />
            <Route path="/study-plan/new/:recommendationId" element={<StudyPlanPage />} />
            <Route path="/study-plan/:planId" element={<StudyPlanPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
