import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, TextField, Button, CircularProgress } from '@mui/material';
import { getScreenshot } from '../../api/api';
import { useNavigate } from 'react-router-dom';
import { karna } from '../../generated/messages';
import './Homepage.css';
import useStatusStore from '../../stores/statusStore';
import useCommandStore from '../../stores/commandStore';
import { websocketService } from '../../api/websocket';
import ScreenCaptureButton from './ScreenCaptureButton';

export const Homepage: React.FC = () => {
  // Get status and command state from Zustand stores
  const { status, connected: statusConnected, error: statusError } = useStatusStore();
  const { commandResponse, connected: commandConnected, error: commandError, pendingCommands } = useCommandStore();
  
  const [command, setCommand] = useState('');
  const [domain, setDomain] = useState('');
  const [screenshot, setScreenshot] = useState<string | null>(null);
  const navigate = useNavigate();

  // Check if any commands are pending
  const isExecuting = pendingCommands.size > 0;

  useEffect(() => {
    // Request initial status
    if (statusConnected) {
      websocketService.requestStatus().catch(console.error);
    }

    // Load initial screenshot
    fetchScreenshot();
  }, [statusConnected]);

  const fetchScreenshot = async () => {
    try {
      const screenshotData = await getScreenshot();
      setScreenshot(screenshotData);
    } catch (error) {
      console.error('Failed to fetch screenshot:', error);
    }
  };

  const handleCommandSubmit = async () => {
    if (!command.trim()) return;
    
    try {
      await websocketService.sendCommand(command.trim(), domain.trim() || 'default');
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

  // Get the error to display (either from status or command channel)
  const displayError = statusError || commandError;

  // Check conditions to show screen capture button:
  // 1. Command has completed successfully
  // 2. is_in_cache is false in the command text (needs training data collection)
  const shouldShowCaptureButton = () => {
    if (!commandResponse || commandResponse.status !== karna.command.CommandExecutionStatus.COMPLETED) {
      return false;
    }
    
    // Check if command text contains is_in_cache=False
    if (commandResponse.commandText) {
      const commandText = commandResponse.commandText.toLowerCase();
      return commandText.includes('is_in_cache=false') || 
             (commandText.includes('is_in_cache') && !commandText.includes('is_in_cache=true'));
    }
    
    return false;
  };

  return (
    <Box sx={{ p: 3, maxWidth: '800px', margin: '0 auto' }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>AI Assistant Status</Typography>
        
        {/* Display connection status */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Typography variant="body2" sx={{ mr: 1 }}>
            Status Connection: {statusConnected ? 'Connected' : 'Disconnected'}
          </Typography>
          <Typography variant="body2">
            Command Connection: {commandConnected ? 'Connected' : 'Disconnected'}
          </Typography>
        </Box>
        
        {/* Display error if any */}
        {displayError && (
          <Typography color="error" variant="body2" sx={{ mb: 2 }}>
            Error: {displayError.message}
          </Typography>
        )}

        <Box sx={{ mb: 2 }}>
          <Typography variant="body1">
            Vision Status: {status?.vision || 'Idle'}
          </Typography>
          <Typography variant="body1">
            Language Status: {status?.language || 'Idle'}
          </Typography>
          <Typography variant="body1" gutterBottom>
            Command Status: {status?.command || 'No active command'}
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
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Button 
              variant="contained" 
              onClick={handleCommandSubmit}
              disabled={!command.trim() || isExecuting || !commandConnected}
              sx={{ mt: 2 }}
              startIcon={isExecuting ? <CircularProgress size={20} color="inherit" /> : null}
            >
              {isExecuting ? 'Executing...' : 'Execute Command'}
            </Button>
            
            {/* Show screen capture button only when command has completed successfully AND needs training data */}
            {shouldShowCaptureButton() && (
              <ScreenCaptureButton 
                refreshScreenshot={fetchScreenshot}
              />
            )}
          </Box>
        </Box>

        {commandResponse && (
          <Box sx={{ mt: 3, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
            <Typography variant="h6" gutterBottom>
              Command Response
            </Typography>
            <Typography 
              color={commandResponse.status === karna.command.CommandExecutionStatus.COMPLETED 
                ? "success.main" 
                : commandResponse.status === karna.command.CommandExecutionStatus.FAILED 
                  ? "error.main" 
                  : "info.main"
              }
            >
              {commandResponse.message || (
                commandResponse.status === karna.command.CommandExecutionStatus.COMPLETED 
                  ? 'Command executed successfully'
                  : 'Command execution in progress'
              )}
            </Typography>
            {commandResponse.actions && commandResponse.actions.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle1">Actions:</Typography>
                {commandResponse.actions.map((action, index) => (
                  <Typography key={index} variant="body2">
                    {action.type}: {action.text ?? JSON.stringify(action.coordinates)}
                  </Typography>
                ))}
              </Box>
            )}
          </Box>
        )}
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