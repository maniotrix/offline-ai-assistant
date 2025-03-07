import React, { useEffect } from "react";
import { Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import CanvasEditor from "./CanvasEditor/CanvasEditor";
import ClassSelector from "./ClassSelector/ClassSelector";
import Header from "./Header/Header";
import useVisionDetectStore from "../../stores/visionDetectStore";
import useScreenCaptureStore from "../../stores/screenCaptureStore";
import { websocketService } from "../../api/websocket";

const BboxEditor: React.FC = () => {
  const { currentImageId, images } = useVisionDetectStore();
  const { captureResult } = useScreenCaptureStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (captureResult?.projectUuid && captureResult?.commandUuid) {
      const { projectUuid, commandUuid } = captureResult;
      
      console.log("Requesting vision detect results for:", {
        project_uuid: projectUuid,
        command_uuid: commandUuid
      });
      
      // getVisionDetectResults requires screenshotEvents parameter
      const screenshotEvents = captureResult.screenshotEvents || [];
      websocketService.getVisionDetectResults(projectUuid, commandUuid, screenshotEvents)
        .catch(error => {
          console.error("Error requesting vision detect results:", error);
        });
    } else {
      console.error("Editor initialized without required parameters in captureResult");
    }
  }, [captureResult]);

  const handleCancel = () => {
    console.log("Cancel button clicked");
    navigate('/');
  };

  const currentImage = currentImageId ? images[currentImageId] : null;
  const imageUrl = currentImage?.croppedImage ? URL.createObjectURL(new Blob([currentImage.croppedImage], { type: 'image/png' })) : null;

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
