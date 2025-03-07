import React, { useState } from "react";
import { Button, Box, Select, MenuItem, FormControl, InputLabel } from "@mui/material";
import { saveAnnotations } from "../../../api/api";
import useVisionDetectStore from "../../../stores/visionDetectStore";
import EditDialog from "../CanvasEditor/EditDialog";
import { v4 as uuidv4 } from 'uuid';
import AddBboxDialog from '../CanvasEditor/AddBboxDialog';

interface ToolbarProps {
  imageUrl: string | null;
  onCancel: () => void;
}

const Toolbar: React.FC<ToolbarProps> = ({ imageUrl, onCancel }) => {
  const { 
    currentImageId,
    images,
    setCurrentImage,
    undo,
    redo
  } = useVisionDetectStore();

  const currentImage = currentImageId ? images[currentImageId] : null;
  const selectedAnnotationId = currentImage?.selectedAnnotationId || null;

  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isAddBboxDialogOpen, setIsAddBboxDialogOpen] = useState(false);

  const handleAddBboxOpen = () => {
    setIsAddBboxDialogOpen(true);
  };

  const handleAddBboxClose = () => {
    setIsAddBboxDialogOpen(false);
  };

  const handleUndo = () => {
    if (currentImageId) {
      undo(currentImageId);
    }
  };

  const handleRedo = () => {
    if (currentImageId) {
      redo(currentImageId);
    }
  };

  const handleSave = async () => {
    if (!imageUrl || !currentImageId) {
      alert("Error: No image selected.");
      return;
    }

    const currentImage = images[currentImageId];
    if (!currentImage) {
      alert("Error: Current image not found.");
      return;
    }

    try {
      await saveAnnotations(imageUrl, currentImage.annotations);
      alert("Annotations saved successfully!");
    } catch (error) {
      alert("Error saving annotations.");
      console.error(error);
    }
  };

  const handleEdit = () => {
    setIsEditDialogOpen(true);
  };

  const handleCloseEditDialog = () => {
    setIsEditDialogOpen(false);
  };

  const handleImageChange = (event: any) => {
    setCurrentImage(event.target.value);
  };

  return (
    <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
      <FormControl sx={{ minWidth: 200 }}>
        <InputLabel>Select Image</InputLabel>
        <Select
          value={currentImageId || ""}
          onChange={handleImageChange}
          label="Select Image"
        >
          {Object.entries(images).map(([id, image]) => (
            <MenuItem key={id} value={id}>
              {image.originalImagePath?.split("/").pop() || id}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Button
        variant="contained"
        color="primary"
        onClick={handleUndo}
        disabled={!currentImageId}
      >
        Undo
      </Button>

      <Button
        variant="contained"
        color="primary"
        onClick={handleRedo}
        disabled={!currentImageId}
      >
        Redo
      </Button>

      <Button
        variant="contained"
        color="primary"
        onClick={handleAddBboxOpen}
        disabled={!currentImageId}
      >
        Add Bbox
      </Button>

      <Button
        variant="contained"
        color="primary"
        onClick={handleEdit}
        disabled={!currentImageId || !selectedAnnotationId}
      >
        Edit
      </Button>

      <Button
        variant="contained"
        color="primary"
        onClick={handleSave}
        disabled={!currentImageId}
      >
        Save
      </Button>

      <Button variant="contained" color="secondary" onClick={onCancel}>
        Cancel
      </Button>

      {isEditDialogOpen && selectedAnnotationId && (
        <EditDialog
          open={isEditDialogOpen}
          onClose={handleCloseEditDialog}
          bboxId={selectedAnnotationId}
        />
      )}

      {isAddBboxDialogOpen && (
        <AddBboxDialog
          open={isAddBboxDialogOpen}
          onClose={handleAddBboxClose}
        />
      )}
    </Box>
  );
};

export default Toolbar;
