import React, { useEffect } from "react";
import { Box } from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";
import CanvasEditor from "./CanvasEditor/CanvasEditor";
import ClassSelector from "./ClassSelector/ClassSelector";
import Header from "./Header/Header";
import useAnnotationStore from "../stores/annotationStore";
import { fetchAnnotations } from "../api/api";

interface LocationState {
  projectUuid?: string;
  commandUuid?: string;
}

const Editor: React.FC = () => {
  const location = useLocation();
  const { projectUuid, commandUuid } = (location.state as LocationState) || {};
  const { setAnnotations } = useAnnotationStore();
  const [imageUrl, setImageUrl] = React.useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const loadAnnotations = async () => {

      try {
        const data = await fetchAnnotations();
        setAnnotations(data.boundingBoxes);
        setImageUrl(data.imageUrl);
      } catch (error) {
        console.error("Error fetching annotations:", error);
      }
    };
    loadAnnotations();
  }, [setAnnotations]);

  useEffect(() => {
    // Only log once when the component mounts
    if (projectUuid && commandUuid) {
      console.log("Editor initialized with:", {
        project_uuid: projectUuid,
        command_uuid: commandUuid
      });
    } else {
      console.warn("Editor initialized without required parameters, using defaults");
    }
  }, [projectUuid, commandUuid]);

  const handleCancel = () => {
    console.log("Cancel button clicked");
  };

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

export default Editor;
