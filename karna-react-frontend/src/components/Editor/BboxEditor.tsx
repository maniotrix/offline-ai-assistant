import React, { useEffect, useCallback, useRef } from "react";
import { Box, CircularProgress, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import CanvasEditor from "./CanvasEditor/CanvasEditor";
import ClassSelector from "./ClassSelector/ClassSelector";
import Header from "./Header/Header";
import useVisionDetectStore from "../../stores/visionDetectStore";
import useScreenCaptureStore from "../../stores/screenCaptureStore";
import { websocketService } from "../../api/websocket";

const BboxEditor: React.FC = () => {
  const { currentImageId, images, isProcessing } = useVisionDetectStore();
  const { captureResult } = useScreenCaptureStore();
  const navigate = useNavigate();
  
  // This ref prevents duplicate requests when the component mounts twice
  // (which happens in development mode due to React.StrictMode in main.tsx)
  const hasRequestedRef = useRef(false);

  // Use useCallback to create a stable function reference that won't change on re-renders
  const requestVisionDetectResults = useCallback((projectUuid: string, commandUuid: string, screenshotEvents: any[]) => {
    console.log("Requesting vision detect results for:", {
      project_uuid: projectUuid,
      command_uuid: commandUuid
    });
    
    return websocketService.getVisionDetectResults(projectUuid, commandUuid, screenshotEvents)
      .catch(error => {
        console.error("Error requesting vision detect results:", error);
      });
  }, []);

  useEffect(() => {
    // Only make the request if we haven't already and we have the required parameters
    if (!hasRequestedRef.current) {
      if (captureResult?.projectUuid && captureResult?.commandUuid) {
        const { projectUuid, commandUuid } = captureResult;
        const screenshotEvents = captureResult.screenshotEvents || [];
        
        // Set the flag before making the request
        hasRequestedRef.current = true;
        
        // Make the request
        requestVisionDetectResults(projectUuid, commandUuid, screenshotEvents);
      } else {
        console.error("Editor initialized without required parameters in captureResult");
      }
    } else {
      console.log("Skipping duplicate request - already requested once");
    }
    // We intentionally only want this to run once on mount
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleCancel = () => {
    console.log("Cancel button clicked");
    navigate('/');
  };

  const currentImage = currentImageId ? images[currentImageId] : null;
  const imageUrl = currentImage?.croppedImage ? URL.createObjectURL(new Blob([currentImage.croppedImage], { type: 'image/png' })) : null;

  // If no data is available, show loading state
  if (Object.keys(images).length === 0) {
    return (
      <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
        <Header imageUrl={null} onCancel={handleCancel} />
        <Box 
          sx={{ 
            display: 'flex', 
            flexDirection: 'column',
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100%', 
            width: '100%',
            padding: 4,
            marginTop: "64px"
          }}
        >
          <CircularProgress size={60} sx={{ mb: 3 }} />
          <Typography variant="h6" sx={{ mb: 2 }}>
            No annotation data available
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
            Capture screenshots or upload images to start annotating.
          </Typography>
          <Button 
            variant="contained" 
            color="primary"
            onClick={handleCancel}
          >
            Return to Home
          </Button>
        </Box>
      </Box>
    );
  }

  // Render the editor when data is available
  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <Header imageUrl={imageUrl} onCancel={handleCancel} />
      <Box sx={{ display: "flex", flexGrow: 1, marginTop: "64px" }}>
        <ClassSelector />
        <CanvasEditor />
      </Box>
    </Box>
  );
};

export default BboxEditor;
