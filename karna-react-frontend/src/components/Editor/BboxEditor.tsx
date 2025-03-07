import React, { useEffect } from "react";
import { Box } from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";
import CanvasEditor from "./CanvasEditor/CanvasEditor";
import ClassSelector from "./ClassSelector/ClassSelector";
import Header from "./Header/Header";
import useVisionDetectStore from "../../stores/visionDetectStore";
import { websocketService } from "../../api/websocket";

interface LocationState {
  projectUuid?: string;
  commandUuid?: string;
}

const BboxEditor: React.FC = () => {
  const location = useLocation();
  const { projectUuid, commandUuid } = (location.state as LocationState) || {};
  const { currentImageId, images } = useVisionDetectStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (projectUuid && commandUuid) {
      console.log("Requesting vision detect results for:", {
        project_uuid: projectUuid,
        command_uuid: commandUuid
      });
      websocketService.getVisionDetectResults(projectUuid, commandUuid)
        .catch(error => {
          console.error("Error requesting vision detect results:", error);
        });
    } else {
      console.error("Editor initialized without required parameters");
    }
  }, [projectUuid, commandUuid]);

  const handleCancel = () => {
    console.log("Cancel button clicked");
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
