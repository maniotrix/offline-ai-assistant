import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, LinearProgress, TextField, Button } from '@mui/material';
import { executeCommand, getStatus, getScreenshot, Status } from '../../api/api';
import { useNavigate } from 'react-router-dom';
import './Homepage.css';

const Homepage: React.FC = () => {
  const [status, setStatus] = useState<Status>({ 
    operation: null, 
    status: 'idle', 
    message: '', 
    progress: 0 
  });
  const [command, setCommand] = useState('');
  const [screenshot, setScreenshot] = useState<string | null>(null);
  const navigate = useNavigate();

  // Poll status every 2 seconds
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const currentStatus = await getStatus();
        setStatus(currentStatus);
        
        // Fetch new screenshot when status changes
        if (currentStatus.status === 'completed') {
          const newScreenshot = await getScreenshot();
          setScreenshot(newScreenshot);
        }
      } catch (error) {
        console.error('Failed to fetch status:', error);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const handleCommandSubmit = async () => {
    try {
      await executeCommand(command);
      setCommand('');
    } catch (error) {
      console.error('Failed to execute command:', error);
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: '800px', margin: '0 auto' }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>AI Assistant Status</Typography>
        <Box sx={{ mb: 2 }}>
          <Typography variant="body1">
            Operation: {status.operation || 'None'}
          </Typography>
          <Typography variant="body1">
            Status: {status.status}
          </Typography>
          <Typography variant="body1" gutterBottom>
            {status.message}
          </Typography>
          {status.status === 'running' && (
            <LinearProgress variant="determinate" value={status.progress} />
          )}
        </Box>

        <Box sx={{ mt: 3 }}>
          <TextField
            fullWidth
            label="Enter command"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            margin="normal"
          />
          <Button 
            variant="contained" 
            onClick={handleCommandSubmit}
            disabled={status.status === 'running'}
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