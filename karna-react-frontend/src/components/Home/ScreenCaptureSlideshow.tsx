import React, { useState, useEffect, useCallback } from 'react';
import { Box, IconButton, Paper, Typography, CircularProgress, Tooltip, Button, Checkbox, Snackbar, Alert } from '@mui/material';
import { NavigateBefore, NavigateNext, PlayArrow, Pause, Delete, Save } from '@mui/icons-material';
import useScreenCaptureStore from '../../stores/screenCaptureStore';
import { getAnnotationImageUrl } from '../../utils/urlUtils';
import { websocketService } from '../../api/websocket';

const Slideshow: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isImageLoading, setIsImageLoading] = useState(true);
  const [selectedScreenshots, setSelectedScreenshots] = useState<Set<string>>(new Set());
  const [isSaving, setIsSaving] = useState(false);
  const [notification, setNotification] = useState<{message: string, type: 'success' | 'error' | 'info'} | null>(null);
  
  const { captureResult } = useScreenCaptureStore();

  // Filter and sort screenshots
  const validScreenshots = captureResult?.screenshotEvents
    ?.filter(event => event.annotationPath)
    .sort((a, b) => {
      if (!a.timestamp || !b.timestamp) return 0;
      return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
    }) || [];

  // Reset capturing state if we have valid screenshots but the button still shows "Stop Recording"
  useEffect(() => {
    if (validScreenshots.length > 0 && useScreenCaptureStore.getState().isCapturing) {
      // If we have valid screenshots but isCapturing is still true, reset it to false
      useScreenCaptureStore.getState().setCapturing(false);
    }
  }, [validScreenshots.length]);

  const handleNext = useCallback(() => {
    if (validScreenshots.length) {
      setCurrentIndex((prev) => (prev + 1) % validScreenshots.length);
      setIsImageLoading(true);
    }
  }, [validScreenshots.length]);

  const handlePrevious = useCallback(() => {
    if (validScreenshots.length) {
      setCurrentIndex((prev) => (prev - 1 + validScreenshots.length) % validScreenshots.length);
      setIsImageLoading(true);
    }
  }, [validScreenshots.length]);

  const togglePlayPause = () => {
    setIsPlaying(prev => !prev);
  };
  
  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft') {
        handlePrevious();
      } else if (e.key === 'ArrowRight') {
        handleNext();
      } else if (e.key === ' ') {
        togglePlayPause();
        e.preventDefault();
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleNext, handlePrevious]);
  
  // Auto-play functionality
  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null;
    
    if (isPlaying && validScreenshots.length > 1) {
      intervalId = setInterval(handleNext, 3000);
    }
    
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isPlaying, handleNext, validScreenshots.length]);

  // Toggle screenshot selection
  const toggleScreenshotSelection = (eventId: string) => {
    setSelectedScreenshots(prev => {
      const newSet = new Set(prev);
      if (newSet.has(eventId)) {
        newSet.delete(eventId);
      } else {
        newSet.add(eventId);
      }
      return newSet;
    });
  };

  // Save changes (delete selected screenshots)
  const saveChanges = async () => {
    if (selectedScreenshots.size === 0 || !captureResult) return;
    
    try {
      setIsSaving(true);
      
      // Get the project and command UUIDs from the first screenshot
      const projectUuid = captureResult.projectUuid;
      const commandUuid = captureResult.commandUuid;
      
      if (!projectUuid || !commandUuid) {
        throw new Error('Missing project or command UUID');
      }
      
      // Create an array of selected screenshot event IDs
      const deletedEventIds = Array.from(selectedScreenshots);
      
      // Update the screen capture channel with the deleted event IDs
      await websocketService.updateScreenCapture(projectUuid, commandUuid, deletedEventIds);
      
      // Clear the selection
      setSelectedScreenshots(new Set());
      setNotification({
        message: 'Screenshots updated successfully',
        type: 'success'
      });
    } catch (error) {
      console.error('Failed to save changes:', error);
      setNotification({
        message: `Failed to save changes: ${error instanceof Error ? error.message : String(error)}`,
        type: 'error'
      });
    } finally {
      setIsSaving(false);
    }
  };

  // Close notification
  const handleCloseNotification = () => {
    setNotification(null);
  };

  if (validScreenshots.length === 0 && !captureResult) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100%',
      }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!validScreenshots.length) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100%',
        color: 'text.secondary' 
      }}>
        <Typography variant="body1">No screenshots with annotations available</Typography>
      </Box>
    );
  }

  const currentScreenshot = validScreenshots[currentIndex];

  return (
    <Box sx={{ 
      position: 'relative', 
      width: '100%', 
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      bgcolor: 'background.default'
    }}>
      {/* Main Image Container */}
      <Box sx={{ 
        position: 'relative',
        width: '100%', 
        height: '80%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <Tooltip title="Previous image">
          <IconButton 
            onClick={handlePrevious}
            sx={{ position: 'absolute', left: 16, zIndex: 1 }}
            aria-label="Previous image"
          >
            <NavigateBefore />
          </IconButton>
        </Tooltip>

        <Paper elevation={3} sx={{ 
          position: 'relative',
          maxWidth: '90%',
          maxHeight: '90%',
          overflow: 'hidden'
        }}>
          {isImageLoading && (
            <Box sx={{ 
              position: 'absolute', 
              top: 0, 
              left: 0, 
              right: 0, 
              bottom: 0, 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center',
              backgroundColor: 'rgba(0,0,0,0.1)'
            }}>
              <CircularProgress size={40} />
            </Box>
          )}
          <Box sx={{ position: 'absolute', top: 8, left: 8, zIndex: 2 }}>
            <Tooltip title="Select for deletion">
              <Checkbox 
                checked={selectedScreenshots.has(currentScreenshot.eventId || '')}
                onChange={() => toggleScreenshotSelection(currentScreenshot.eventId || '')}
                color="primary"
                sx={{ 
                  backgroundColor: 'rgba(255, 255, 255, 0.7)',
                  borderRadius: '4px',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)'
                  }
                }}
              />
            </Tooltip>
          </Box>
          <img 
            src={getAnnotationImageUrl(currentScreenshot.annotationPath)}
            alt={`Screenshot from ${currentScreenshot.timestamp}`}
            style={{
              maxWidth: '100%',
              maxHeight: '100%',
              objectFit: 'contain',
              opacity: isImageLoading ? 0.5 : 1,
              transition: 'opacity 0.3s'
            }}
            onLoad={() => setIsImageLoading(false)}
            onError={() => setIsImageLoading(false)}
          />
          <Box sx={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            bgcolor: 'rgba(0,0,0,0.5)',
            color: 'white',
            padding: 1,
            textAlign: 'center'
          }}>
            {new Date(currentScreenshot.timestamp || '').toLocaleString()}
          </Box>
        </Paper>

        <Tooltip title="Next image">
          <IconButton 
            onClick={handleNext}
            sx={{ position: 'absolute', right: 16, zIndex: 1 }}
            aria-label="Next image"
          >
            <NavigateNext />
          </IconButton>
        </Tooltip>
      </Box>

      {/* Controls and Counter */}
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        padding: 1,
        gap: 2
      }}>
        <Tooltip title={isPlaying ? "Pause slideshow" : "Play slideshow"}>
          <IconButton onClick={togglePlayPause} aria-label={isPlaying ? "Pause slideshow" : "Play slideshow"}>
            {isPlaying ? <Pause /> : <PlayArrow />}
          </IconButton>
        </Tooltip>
        <Typography variant="body2">
          {currentIndex + 1} / {validScreenshots.length}
        </Typography>
        
        {/* Save button */}
        <Button
          variant="contained"
          color="primary"
          startIcon={isSaving ? <CircularProgress size={20} color="inherit" /> : <Save />}
          onClick={saveChanges}
          disabled={selectedScreenshots.size === 0 || isSaving}
          sx={{ ml: 2 }}
        >
          {isSaving ? 'Saving...' : 'Delete Selected'}
        </Button>
      </Box>
      
      {/* Selection info */}
      {selectedScreenshots.size > 0 && (
        <Typography variant="body2" color="error" sx={{ mt: 1 }}>
          {selectedScreenshots.size} screenshot(s) selected for deletion
        </Typography>
      )}
      
      {/* Notification */}
      <Snackbar 
        open={notification !== null} 
        autoHideDuration={6000} 
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        {notification ? (
          <Alert 
            onClose={handleCloseNotification} 
            severity={notification.type} 
            sx={{ width: '100%' }}
          >
            {notification.message}
          </Alert>
        ) : <div />}
      </Snackbar>
    </Box>
  );
};

export default Slideshow;