import React, { useEffect } from "react";
import { Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import CanvasEditor from "./CanvasEditor/CanvasEditor";
import ClassSelector from "./ClassSelector/ClassSelector";
import Header from "./Header/Header";
import useAnnotationStore from "../stores/annotationStore";
import { fetchAnnotations } from "../api/api";

const Editor: React.FC = () => {
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
