import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, TextField, Button } from '@mui/material';
import { executeCommand, getScreenshot, Status, subscribeToStatus } from '../../api/api';
import { useNavigate } from 'react-router-dom';
import './Homepage.css';

const Homepage: React.FC = () => {
  const [status, setStatus] = useState<Status>({ 
    vision: '',
    language: '',
    command: ''
  });
  const [command, setCommand] = useState('');
  const [domain, setDomain] = useState('default');
  const [screenshot, setScreenshot] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const unsubscribe = subscribeToStatus((newStatus) => {
      console.log('Status update received:', newStatus);
      setStatus(newStatus);
    });

    // Cleanup subscription on unmount
    return () => unsubscribe();
  }, []);

  const handleCommandSubmit = async () => {
    if (!command.trim()) return;
    
    try {
      await executeCommand(command.trim(), domain.trim() || 'default');
      setCommand('');
    } catch (error) {
      console.error('Failed to execute command:', error);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleCommandSubmit();
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: '800px', margin: '0 auto' }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>AI Assistant Status</Typography>
        <Box sx={{ mb: 2 }}>
          <Typography variant="body1">
            Vision Status: {status.vision || 'Idle'}
          </Typography>
          <Typography variant="body1">
            Language Status: {status.language || 'Idle'}
          </Typography>
          <Typography variant="body1" gutterBottom>
            Command Status: {status.command || 'No active command'}
          </Typography>
        </Box>

        <Box sx={{ mt: 3 }}>
          <TextField
            fullWidth
            label="Domain (optional)"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            margin="normal"
            placeholder="e.g., youtube.com, default"
          />
          <TextField
            fullWidth
            multiline
            rows={2}
            label="Enter command"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            onKeyPress={handleKeyPress}
            margin="normal"
            placeholder="Type your command here..."
          />
          <Button 
            variant="contained" 
            onClick={handleCommandSubmit}
            disabled={!command.trim()}
            sx={{ mt: 2 }}
          >
            Execute Command
          </Button>
        </Box>
      </Paper>

      {screenshot && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Current Screen</Typography>
          <img 
            src={`data:image/png;base64,${screenshot}`} 
            alt="Current screen" 
            style={{ maxWidth: '100%' }} 
          />
        </Paper>
      )}

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
    </Box>
  );
};

export default Homepage;