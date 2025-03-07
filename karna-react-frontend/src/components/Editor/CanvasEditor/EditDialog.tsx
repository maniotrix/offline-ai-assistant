import React, { useState, useEffect } from "react";
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, IconButton, Select, MenuItem, FormControl, InputLabel } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import useVisionDetectStore from "../../../stores/visionDetectStore";

interface EditDialogProps {
  open: boolean;
  onClose: () => void;
  bboxId: string | null;
}

const EditDialog: React.FC<EditDialogProps> = ({ open, onClose, bboxId }) => {
  const { currentImageId, images, setAnnotations, pushToHistory } = useVisionDetectStore();
  const [newLabel, setNewLabel] = useState("");
  const [availableClasses, setAvailableClasses] = useState<string[]>([]);

  const currentImage = currentImageId ? images[currentImageId] : null;
  const annotations = currentImage?.annotations || [];

  /**
   * Adds mandatory class names to the list of classes if they don't already exist
   * @param classes - The current list of class names
   * @returns The updated list with mandatory class names included
   */
  const addMandatoryClasses = (classes: string[]): string[] => {
    const mandatoryClasses = [
      'ignore', 
      'button', 
      'field', 
      'heading', 
      'iframe', 
      'image', 
      'label', 
      'link', 
      'text'
    ];
    
    const updatedClasses = [...classes];
    
    mandatoryClasses.forEach(className => {
      if (!updatedClasses.includes(className)) {
        updatedClasses.push(className);
      }
    });
    
    return updatedClasses;
  };

  useEffect(() => {
    const uniqueClasses = [...new Set(annotations.map((bbox) => bbox.class))];
    const classesWithMandatory = addMandatoryClasses(uniqueClasses);
    setAvailableClasses(classesWithMandatory);
    
    if (bboxId) {
      const selectedBbox = annotations.find((bbox) => bbox.id === bboxId);
      if (selectedBbox) {
        setNewLabel(selectedBbox.class);
      }
    }
  }, [annotations, bboxId]);

  const handleSave = () => {
    if (bboxId && currentImageId) {
      pushToHistory(currentImageId);
      const updatedAnnotations = annotations.map((bbox) =>
        bbox.id === bboxId ? { ...bbox, class: newLabel } : bbox
      );
      setAnnotations(currentImageId, updatedAnnotations);
      onClose();
    }
  };

  const handleDelete = () => {
    if (bboxId && currentImageId) {
      pushToHistory(currentImageId);
      const updatedAnnotations = annotations.filter((bbox) => bbox.id !== bboxId);
      setAnnotations(currentImageId, updatedAnnotations);
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Edit Bbox</DialogTitle>
      <DialogContent>
        <FormControl fullWidth margin="dense">
          <InputLabel>Class</InputLabel>
          <Select
            value={newLabel}
            onChange={(e) => setNewLabel(e.target.value as string)}
            label="New Label"
          >
            {availableClasses.map((cls) => (
              <MenuItem key={cls} value={cls}>
                {cls}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <IconButton onClick={handleDelete} color="error">
          <DeleteIcon />
        </IconButton>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={handleSave} color="primary">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditDialog;