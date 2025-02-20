import React, { useEffect, useState } from 'react';
import { Drawer, List, ListItem, ListItemText, Checkbox, IconButton, Typography, Paper, Divider } from '@mui/material';
import MenuOpenIcon from '@mui/icons-material/MenuOpen';
import MenuIcon from '@mui/icons-material/Menu';
import useAnnotationStore from '../../stores/annotationStore';

const ClassSelector: React.FC = () => {
  const { annotations, selectedClasses, toggleSelectedClass, isSidebarOpen, toggleSidebar, setSelectedClasses } = useAnnotationStore();
  const [availableClasses, setAvailableClasses] = useState<string[]>([]);
  const [userMadeSelection, setUserMadeSelection] = useState(false);

  useEffect(() => {
    const uniqueClasses = [...new Set(annotations.map((bbox) => bbox.class))];
    if (!uniqueClasses.includes('ignore')) {
      uniqueClasses.push('ignore');
    }
    setAvailableClasses(uniqueClasses);

    // ✅ Ensure classes are only auto-selected on initial load, not when the user unchecks all
    if (!userMadeSelection && selectedClasses.size === 0 && uniqueClasses.length > 1) {
      setSelectedClasses(new Set(uniqueClasses));
    }
  }, [annotations, selectedClasses, setSelectedClasses, userMadeSelection]);

  const areAllClassesSelected = (): boolean => selectedClasses.size === availableClasses.length;
  const areNoClassesSelected = (): boolean => selectedClasses.size === 0;

  const handleToggleAll = () => {
    setUserMadeSelection(true);

    if (areAllClassesSelected()) {
      setSelectedClasses(new Set());
    } else {
      setSelectedClasses(new Set(availableClasses));
    }
  };

  const handleToggleClass = (cls: string) => {
    setUserMadeSelection(true);

    const updatedClasses = new Set(selectedClasses);
    if (updatedClasses.has(cls)) {
      updatedClasses.delete(cls);
    } else {
      updatedClasses.add(cls);
    }

    setSelectedClasses(updatedClasses);
  };

  return (
    <>
      <IconButton
        sx={{
          position: 'absolute',
          left: isSidebarOpen ? 260 : 10,
          top: 10,
          backgroundColor: '#1976d2',
          color: 'white',
          '&:hover': { backgroundColor: '#1565c0' },
        }}
        onClick={toggleSidebar}
      >
        {isSidebarOpen ? <MenuOpenIcon /> : <MenuIcon />}
      </IconButton>

      <Drawer anchor="left" open={isSidebarOpen} onClose={toggleSidebar} sx={{ width: 300 }}>
        <Paper
          elevation={8}
          sx={{
            width: 260,
            height: '90vh',
            margin: '20px auto',
            padding: 3,
            borderRadius: 4,
            background: 'linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%)',
            boxShadow: '0px 8px 24px rgba(0, 0, 0, 0.2)',
          }}
        >
          <Typography variant="h6" sx={{ textAlign: 'center', fontWeight: 'bold', color: '#333', paddingBottom: 1 }}>
            Select Classes
          </Typography>
          <Divider sx={{ marginBottom: 2 }} />

          <List>
            <ListItem key="all" component="div" onClick={handleToggleAll} sx={{ cursor: 'pointer' }}>
              <Checkbox checked={areAllClassesSelected()} />
              <ListItemText primary="All Classes" sx={{ fontWeight: 'bold', color: '#1976d2' }} />
            </ListItem>

            {availableClasses.map((cls) => (
              <ListItem key={cls} component="div" onClick={() => handleToggleClass(cls)} sx={{ cursor: 'pointer' }}>
                <Checkbox checked={selectedClasses.has(cls)} />
                <ListItemText
                  primary={cls}
                  sx={{ fontWeight: selectedClasses.has(cls) ? 'bold' : 'normal', color: selectedClasses.has(cls) ? '#1976d2' : '#333' }}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Drawer>
    </>
  );
};

export default ClassSelector;
