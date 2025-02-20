import React, { useState } from "react";
import { Button, Box } from "@mui/material";
import { saveAnnotations } from "../../api/api";
import useAnnotationStore from "../../stores/annotationStore";
import EditDialog from "../CanvasEditor/EditDialog";
import { v4 as uuidv4 } from 'uuid';
import AddBboxDialog from '../CanvasEditor/AddBboxDialog';

interface ToolbarProps {
  imageUrl: string | null;
  onCancel: () => void;
}

const Toolbar: React.FC<ToolbarProps> = ({ imageUrl, onCancel }) => {
  const { annotations, history, redoStack, setAnnotations, selectedAnnotationId } = useAnnotationStore();
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isAddBboxDialogOpen, setIsAddBboxDialogOpen] = useState(false);

  const handleAddBboxOpen = () => {
    setIsAddBboxDialogOpen(true);
  };

  const handleAddBboxClose = () => {
    setIsAddBboxDialogOpen(false);
  };

  const handleUndo = () => {
    if (history.length === 0) return;

    // Move current state to redo stack
    const updatedRedoStack = [annotations, ...redoStack];

    // Get the last state from history
    const prevAnnotations = history[history.length - 1];

    // Update history and annotations
    useAnnotationStore.setState((state) => ({
      history: state.history.slice(0, -1),
      redoStack: updatedRedoStack,
    }));

    setAnnotations(prevAnnotations); // ✅ Force state update
  };

  const handleRedo = () => {
    if (redoStack.length === 0) return;

    // Move current state to history
    const updatedHistory = [...history, annotations];

    // Get the next state from redoStack
    const nextAnnotations = redoStack[0];

    // Update redo stack and annotations
    useAnnotationStore.setState((state) => ({
      history: updatedHistory,
      redoStack: state.redoStack.slice(1),
    }));

    setAnnotations(nextAnnotations); // ✅ Force state update
  };

  const handleSave = async () => {
    if (!imageUrl) {
      alert("Error: No image URL found.");
      return;
    }

    // convert annotaions to math round values to avoid floating point errors
    const annotations = useAnnotationStore.getState().annotations.map((bbox) => ({
      ...bbox,
      x: Math.round(bbox.x),
      y: Math.round(bbox.y),
      width: Math.round(bbox.width),
      height: Math.round(bbox.height),
    }));

    try {
      await saveAnnotations(imageUrl, annotations);
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

  return (
    <Box sx={{ display: "flex", gap: 2 }}>
      {/* Undo Button */}
      <Button
        variant="contained"
        color="primary"
        onClick={handleUndo}
        disabled={history.length === 0} // Disable when no undo actions available
        sx={{ minWidth: "120px" }}
      >
        Undo
      </Button>

      {/* Redo Button */}
      <Button
        variant="contained"
        color="secondary"
        onClick={handleRedo}
        disabled={redoStack.length === 0} // Disable when no redo steps available
        sx={{ minWidth: "120px" }}
      >
        Redo
      </Button>

      {/* Edit Button */}
      <Button
        variant="contained"
        color="warning"
        onClick={handleEdit}
        disabled={selectedAnnotationId === null || selectedAnnotationId === undefined} // Disable when no annotation is selected
        sx={{ minWidth: "120px" }}
      >
        Edit Bbox
      </Button>

      {/* Add Bbox Button */}
      <Button
        variant="contained"
        color="info"
        onClick={handleAddBboxOpen}
        sx={{ minWidth: "120px" }}
      >
        Add Bbox
      </Button>

      {/* Save Button */}
      <Button
        variant="contained"
        color="success"
        onClick={handleSave}
        sx={{ minWidth: "120px" }}
      >
        Save
      </Button>

      {/* Cancel Button */}
      <Button
        variant="contained"
        color="error"
        onClick={onCancel}
        sx={{ minWidth: "120px" }}
      >
        Cancel
      </Button>

      {/* Edit Dialog */}
      <EditDialog
        open={isEditDialogOpen}
        onClose={handleCloseEditDialog}
        bboxId={selectedAnnotationId}
      />

      {/* Add Bbox Dialog */}
      <AddBboxDialog
        open={isAddBboxDialogOpen}
        onClose={handleAddBboxClose}
      />
    </Box>
  );
};

export default Toolbar;
