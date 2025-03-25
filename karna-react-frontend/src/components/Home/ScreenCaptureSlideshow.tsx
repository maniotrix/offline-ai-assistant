import React, { useState, useEffect, useCallback } from 'react';
import { Box, IconButton, Paper, Typography, CircularProgress, Tooltip, Button, Checkbox, Snackbar, Alert, TextField } from '@mui/material';
import { NavigateBefore, NavigateNext, PlayArrow, Pause, Delete, Save, Edit } from '@mui/icons-material';
import useScreenCaptureStore from '../../stores/screenCaptureStore';
import { getAnnotationImageUrl } from '../../utils/urlUtils';
import { websocketService } from '../../api/websocket';

/**
 * Helper function to get mouse button tooltip with fallback for backward compatibility
 * @param event Screenshot event
 * @returns Mouse button tooltip string
 */
const getMouseButtonTooltip = (event: any): string => {
  // Check for the snake_case version (backend format)
  if (event.mouse_event_tool_tip) {
    return event.mouse_event_tool_tip;
  }
  
  // Check for the camelCase version (frontend format)
  if (event.mouseEventToolTip) {
    return event.mouseEventToolTip;
  }
  
  // If mouse coordinates exist but no tooltip, default to "Left Click"
  if (event.mouseX !== null && event.mouseX !== undefined && 
      event.mouseY !== null && event.mouseY !== undefined) {
    return "Left Click";
  }
  
  // No mouse event
  return "";
};

/**
 * Set mouse button tooltip, handling both snake_case and camelCase
 * @param event Screenshot event to modify
 * @param tooltip New tooltip string
 */
const setMouseButtonTooltip = (event: any, tooltip: string): void => {
  // Update both versions for compatibility
  event.mouse_event_tool_tip = tooltip;
  event.mouseEventToolTip = tooltip;
};

const Slideshow: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isImageLoading, setIsImageLoading] = useState(true);
  const [selectedScreenshots, setSelectedScreenshots] = useState<Set<string>>(new Set());
  const [isSaving, setIsSaving] = useState(false);
  const [notification, setNotification] = useState<{message: string, type: 'success' | 'error' | 'info'} | null>(null);
  const [isEditingTooltip, setIsEditingTooltip] = useState(false);
  const [tooltipText, setTooltipText] = useState<string>("");
  const [editedScreenshots, setEditedScreenshots] = useState<Set<string>>(new Set());
  
  const { captureResult, setScreenshotEvents } = useScreenCaptureStore();

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

  // Update tooltip text when current screenshot changes
  useEffect(() => {
    if (currentIndex >= 0 && currentIndex < validScreenshots.length) {
      const currentScreenshot = validScreenshots[currentIndex];
      setTooltipText(getMouseButtonTooltip(currentScreenshot));
    }
  }, [currentIndex, validScreenshots]);

  const handleNext = useCallback(() => {
    if (validScreenshots.length) {
      setCurrentIndex((prev) => (prev + 1) % validScreenshots.length);
      setIsImageLoading(true);
      setIsEditingTooltip(false);
    }
  }, [validScreenshots.length]);

  const handlePrevious = useCallback(() => {
    if (validScreenshots.length) {
      setCurrentIndex((prev) => (prev - 1 + validScreenshots.length) % validScreenshots.length);
      setIsImageLoading(true);
      setIsEditingTooltip(false);
    }
  }, [validScreenshots.length]);

  const togglePlayPause = () => {
    setIsPlaying(prev => !prev);
    if (isEditingTooltip) {
      saveTooltipChanges();
    }
  };
  
  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Skip processing when editing (let the TextField handle keys normally)
      if (isEditingTooltip) {
        // Only handle global shortcuts if the event didn't originate from an input
        const isFromInput = (e.target as HTMLElement)?.tagName === 'INPUT';
        if (!isFromInput) {
          // Only handle Escape globally if not from an input
          if (e.key === 'Escape') {
            setIsEditingTooltip(false);
            e.preventDefault();
          }
        }
        // Don't handle any other keys when editing
        return;
      }
      
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
  }, [handleNext, handlePrevious, isEditingTooltip, togglePlayPause]);
  
  // Auto-play functionality
  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null;
    
    if (isPlaying && validScreenshots.length > 1 && !isEditingTooltip) {
      intervalId = setInterval(handleNext, 3000);
    }
    
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isPlaying, handleNext, validScreenshots.length, isEditingTooltip]);

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
  
  // Start editing tooltip
  const startEditingTooltip = () => {
    setIsEditingTooltip(true);
    setIsPlaying(false); // Pause slideshow while editing
  };
  
  // Save tooltip changes to current screenshot
  const saveTooltipChanges = () => {
    if (!isEditingTooltip || !validScreenshots.length) return;
    
    // Get the current value from the text field
    const inputField = document.getElementById('tooltip-edit-field') as HTMLInputElement;
    const newTooltipText = inputField ? inputField.value : tooltipText;
    
    // Mark this screenshot as edited
    const currentScreenshot = validScreenshots[currentIndex];
    setEditedScreenshots(prev => {
      const newSet = new Set(prev);
      newSet.add(currentScreenshot.eventId || '');
      return newSet;
    });
    
    // Update the tooltip in the current screenshot
    setMouseButtonTooltip(currentScreenshot, newTooltipText);
    
    // Update local state to stay in sync
    setTooltipText(newTooltipText);
    
    // Update the events in the store (creates a new array to trigger reactivity)
    if (captureResult && captureResult.screenshotEvents) {
      const updatedEvents = [...captureResult.screenshotEvents];
      setScreenshotEvents(updatedEvents);
    }
    
    setIsEditingTooltip(false);
  };

  // Save changes (delete selected screenshots and update edited ones)
  const saveChanges = async () => {
    if (!captureResult || !captureResult.screenshotEvents) return;
    
    try {
      setIsSaving(true);
      
      // Get the project and command UUIDs
      const projectUuid = captureResult.projectUuid;
      const commandUuid = captureResult.commandUuid;
      
      if (!projectUuid || !commandUuid) {
        throw new Error('Missing project or command UUID');
      }
      
      // Filter out screenshots selected for deletion
      let updatedScreenshots = captureResult.screenshotEvents.filter(
        event => !selectedScreenshots.has(event.eventId || '')
      );
      
      // Send the updated list to the backend
      await websocketService.updateScreenCapture(projectUuid, commandUuid, updatedScreenshots);
      
      // Clear selections
      setSelectedScreenshots(new Set());
      setEditedScreenshots(new Set());
      
      setNotification({
        message: `Screenshots updated successfully${selectedScreenshots.size > 0 ? ` (${selectedScreenshots.size} deleted)` : ''}`,
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
  // Check if the current screenshot has been edited
  const isCurrentEdited = editedScreenshots.has(currentScreenshot.eventId || '');

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
            disabled={isEditingTooltip}
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
                disabled={isEditingTooltip}
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
          
          {/* Mouse tooltip and metadata */}
          {(currentScreenshot.mouseX !== null || currentScreenshot.keyChar !== null) && (
            <Box sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              bgcolor: 'rgba(255, 255, 255, 0.8)',
              color: 'text.primary',
              padding: 1,
              borderRadius: 1,
              maxWidth: '250px',
              fontSize: '0.8rem',
              zIndex: 2,
              border: isCurrentEdited ? '2px solid #4caf50' : 'none'
            }}>
              {currentScreenshot.mouseX !== null && currentScreenshot.mouseY !== null && (
                <Typography variant="caption" display="block">
                  <strong>Mouse Position:</strong> ({currentScreenshot.mouseX}, {currentScreenshot.mouseY})
                  
                  {/* Editable tooltip field */}
                  {isEditingTooltip ? (
                    <Box component="form" onSubmit={(e) => { e.preventDefault(); saveTooltipChanges(); }} 
                      sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                      <TextField
                        id="tooltip-edit-field"
                        variant="outlined"
                        size="small"
                        defaultValue={tooltipText}
                        autoFocus
                        fullWidth
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault();
                            saveTooltipChanges();
                          } else if (e.key === 'Escape') {
                            e.preventDefault();
                            setIsEditingTooltip(false);
                          }
                        }}
                        inputProps={{
                          style: { fontSize: '0.8rem' }
                        }}
                        sx={{ 
                          '& .MuiOutlinedInput-root': {
                            fontSize: '0.8rem',
                            height: '32px'
                          }
                        }}
                        placeholder="Enter tooltip text"
                      />
                      <IconButton size="small" onClick={saveTooltipChanges} color="primary">
                        <Save fontSize="small" />
                      </IconButton>
                    </Box>
                  ) : (
                    <Box 
                      component="span" 
                      sx={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        mt: 0.5,
                        cursor: 'pointer',
                        '&:hover': { backgroundColor: 'rgba(0,0,0,0.05)' },
                        padding: '2px 4px',
                        borderRadius: '4px'
                      }}
                      onClick={startEditingTooltip}
                    >
                      <strong style={{ marginRight: '4px' }}>Click Tooltip:</strong> 
                      {getMouseButtonTooltip(currentScreenshot)}
                      <IconButton size="small" sx={{ ml: 1, p: 0.5 }}>
                        <Edit fontSize="small" />
                      </IconButton>
                    </Box>
                  )}
                </Typography>
              )}
              {currentScreenshot.keyChar && (
                <Typography variant="caption" display="block" sx={{ mt: 0.5 }}>
                  <strong>Key Pressed:</strong> {currentScreenshot.keyChar}
                </Typography>
              )}
            </Box>
          )}
          
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
            disabled={isEditingTooltip}
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
          <IconButton 
            onClick={togglePlayPause} 
            aria-label={isPlaying ? "Pause slideshow" : "Play slideshow"}
            disabled={isEditingTooltip}
          >
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
          disabled={(selectedScreenshots.size === 0 && editedScreenshots.size === 0) || isSaving || isEditingTooltip}
          sx={{ ml: 2 }}
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </Button>
      </Box>
      
      {/* Selection and changes info */}
      {(selectedScreenshots.size > 0 || editedScreenshots.size > 0) && (
        <Typography variant="body2" color="info.main" sx={{ mt: 1 }}>
          {selectedScreenshots.size > 0 && `${selectedScreenshots.size} screenshot(s) selected for deletion. `}
          {editedScreenshots.size > 0 && `${editedScreenshots.size} screenshot(s) with edited tooltips. `}
          Press "Save Changes" to apply.
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