import React, { useState } from 'react';
import { Button, CircularProgress, Badge } from '@mui/material';
import VideocamIcon from '@mui/icons-material/Videocam';
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';
import useScreenCaptureStore from '../../stores/screenCaptureStore';
import useCommandStore from '../../stores/commandStore';
import { websocketService } from '../../api/websocket';

const ScreenCaptureButton: React.FC = () => {
  const [isStarting, setIsStarting] = useState(false);
  const { isCapturing } = useScreenCaptureStore();
  const { commandResponse } = useCommandStore();
  
  // Extract command UUID and domain from the command text
  const extractCommandInfo = () => {
    if (!commandResponse || !commandResponse.commandText) return { projectUuid: 'default', commandUuid: `command-${Date.now()}` };
    
    try {
      // Try to parse the command text as it might contain structured data
      const commandText = commandResponse.commandText;
      
      // Extract UUID using regex
      const uuidMatch = commandText.match(/uuid='([^']+)'/);
      const commandUuid = uuidMatch ? uuidMatch[1] : `command-${Date.now()}`;
      
      // Extract domain using regex
      const domainMatch = commandText.match(/domain='([^']+)'/);
      const projectUuid = domainMatch ? domainMatch[1] : 'default';
      
      return { projectUuid, commandUuid };
    } catch (error) {
      console.error('Error parsing command text:', error);
      return { projectUuid: 'default', commandUuid: `command-${Date.now()}` };
    }
  };
  
  const handleStartCapture = async () => {
    if (!commandResponse) return;
    
    try {
      setIsStarting(true);
      const { projectUuid, commandUuid } = extractCommandInfo();
      
      await websocketService.startScreenCapture(projectUuid, commandUuid);
      setIsStarting(false);
    } catch (error) {
      console.error('Failed to start screen capture:', error);
      setIsStarting(false);
    }
  };

  const handleStopCapture = async () => {
    if (!commandResponse) return;
    
    try {
      const { projectUuid, commandUuid } = extractCommandInfo();
      await websocketService.stopScreenCapture(projectUuid, commandUuid);
    } catch (error) {
      console.error('Failed to stop screen capture:', error);
    }
  };

  // Only show the button when command is completed
  if (!commandResponse) {
    return null;
  }

  return (
    <Badge
      variant="dot"
      color="error"
      overlap="circular"
      invisible={!isCapturing}
      anchorOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      sx={{
        '& .MuiBadge-badge': {
          animation: isCapturing ? 'pulse 1.5s infinite' : 'none',
          '@keyframes pulse': {
            '0%': { opacity: 1 },
            '50%': { opacity: 0.5 },
            '100%': { opacity: 1 },
          },
        },
      }}
    >
      <Button
        variant="contained"
        color={isCapturing ? "error" : "secondary"}
        onClick={isCapturing ? handleStopCapture : handleStartCapture}
        startIcon={isStarting ? 
          <CircularProgress size={20} color="inherit" /> : 
          isCapturing ? <FiberManualRecordIcon /> : <VideocamIcon />
        }
        sx={{ mt: 2, ml: 2 }}
        disabled={isStarting}
      >
        {isCapturing ? 'Stop Recording' : 'Start Screen Capture'}
      </Button>
    </Badge>
  );
};

export default ScreenCaptureButton;