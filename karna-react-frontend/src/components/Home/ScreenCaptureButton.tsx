import React, { useState } from 'react';
import { Button, CircularProgress, Badge } from '@mui/material';
import VideocamIcon from '@mui/icons-material/Videocam';
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';
import useScreenCaptureStore from '../../stores/screenCaptureStore';
import useCommandStore from '../../stores/commandStore';
import { websocketService } from '../../api/websocket';
import { getScreenshot } from '../../api/api';

interface ScreenCaptureButtonProps {
  onCaptureStopped?: () => void;
  refreshScreenshot?: () => void;
}

const ScreenCaptureButton: React.FC<ScreenCaptureButtonProps> = ({ 
  onCaptureStopped,
  refreshScreenshot
}) => {
  const [isStarting, setIsStarting] = useState(false);
  const { isCapturing, setCapturing } = useScreenCaptureStore();
  const { commandResponse } = useCommandStore();
  
  const handleStartCapture = async () => {
    if (!commandResponse) return;
    
    try {
      setIsStarting(true);
      // Generate a UUID for the project (could be improved to be more specific)
      const projectUuid = 'default';
      // Use the command text as the command UUID to track this session
      const commandUuid = commandResponse.commandText || `command-${Date.now()}`;
      
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
      // Use the same projectUuid and commandUuid to stop the current session
      const projectUuid = 'default';
      const commandUuid = commandResponse.commandText || `command-${Date.now()}`;
      
      await websocketService.stopScreenCapture(projectUuid, commandUuid);
      
      // Trigger any callbacks
      if (onCaptureStopped) onCaptureStopped();
      
      // Refresh the screenshot after stopping capture
      if (refreshScreenshot) {
        setTimeout(refreshScreenshot, 500); // Small delay to ensure server has time to process
      }
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