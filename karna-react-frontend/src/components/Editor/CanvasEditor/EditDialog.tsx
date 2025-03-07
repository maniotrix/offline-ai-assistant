import React, { useState, useEffect } from "react";
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, IconButton, Select, MenuItem, FormControl, InputLabel } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import useAnnotationStore from "../../../stores/annotationStore";

interface EditDialogProps {
  open: boolean;
  onClose: () => void;
  bboxId: string | null;
}

const EditDialog: React.FC<EditDialogProps> = ({ open, onClose, bboxId }) => {
  const { annotations, setAnnotations, pushToHistory } = useAnnotationStore();
  const [newLabel, setNewLabel] = useState("");
  const [availableClasses, setAvailableClasses] = useState<string[]>([]);

  useEffect(() => {
    const uniqueClasses = [...new Set(annotations.map((bbox) => bbox.class))];
    setAvailableClasses([...uniqueClasses, "ignore"]);
    if (bboxId) {
      const selectedBbox = annotations.find((bbox) => bbox.id === bboxId);
      if (selectedBbox) {
        setNewLabel(selectedBbox.class);
      }
    }
  }, [annotations, bboxId]);

  const handleSave = () => {
    if (bboxId) {
      pushToHistory(); // Store previous state before modifying
      const updatedAnnotations = annotations.map((bbox) =>
        bbox.id === bboxId ? { ...bbox, class: newLabel } : bbox
      );
      setAnnotations(updatedAnnotations);
      onClose();
    }
  };

  const handleDelete = () => {
    if (bboxId) {
      pushToHistory(); // Store previous state before modifying
      const updatedAnnotations = annotations.filter((bbox) => bbox.id !== bboxId);
      setAnnotations(updatedAnnotations);
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