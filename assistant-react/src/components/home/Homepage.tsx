import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Homepage.css';

const Homepage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="homepage">
      <section className="hero">
        <h1>Your AI Assistant</h1>
        <p>Your personal assistant to help you with your daily tasks.</p>
        <button onClick={() => navigate('/editor')}>Open Editor</button>
      </section>

      <section className="features">
        <div className="feature">
          <i className="fas fa-comments"></i>
          <h3>Natural Language Understanding</h3>
          <p>Understands and responds to your queries in a natural way.</p>
        </div>
        <div className="feature">
          <i className="fas fa-tasks"></i>
          <h3>Task Management</h3>
          <p>Helps you manage your tasks and stay organized.</p>
        </div>
        <div className="feature">
          <i className="fas fa-info-circle"></i>
          <h3>Information Retrieval</h3>
          <p>Provides you with relevant information quickly and efficiently.</p>
        </div>
      </section>
    </div>
  );
};

export default Homepage;