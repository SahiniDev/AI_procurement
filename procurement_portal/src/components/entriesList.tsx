import React, { useEffect, useState } from "react";
import {
  Paper,
  Typography,
  CircularProgress,
  List,
  ListItemText,
  ListItemButton,
  Button,
  Menu,
  MenuItem,
} from "@mui/material";
import { Entry } from "@/types"; // Consolidated Entry interface

const statusMap: { [key: number]: string } = { 0: "Open", 1: "In Progress", 2: "Closed" };

interface EntriesListProps {
  entries: Entry[];
}

export default function EntriesList({ entries: initialEntries }: EntriesListProps) {
  const [entries, setEntries] = useState<Entry[]>(initialEntries);
  const [selectedEntry, setSelectedEntry] = useState<Entry | null>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  useEffect(() => {
    if (initialEntries.length > 0) {
      setEntries(initialEntries);
    }
  }, [initialEntries]);

  const handleMenuOpen = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => setAnchorEl(null);

  const handleStatusChange = async (status: number) => {
    if (!selectedEntry) return;

    try {
      const response = await fetch(`http://localhost:5000/update/${selectedEntry.id}/${status}`, {
        method: "PUT",
      });

      if (!response.ok) {
        throw new Error("Failed to update status");
      }

      setEntries((prevEntries) =>
        prevEntries?.map((entry) =>
          entry.id === selectedEntry.id ? { ...entry, status } : entry
        ) || []
      );
      setSelectedEntry({ ...selectedEntry, status });
    } catch (error) {
      console.error(error);
    } finally {
      handleMenuClose();
    }
  };

  const handleDelete = async () => {
    if (!selectedEntry) return;

    try {
      const response = await fetch(`http://localhost:5000/delete/${selectedEntry.id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete entry");
      }

      setEntries((prevEntries) =>
        prevEntries?.filter((entry) => entry.id !== selectedEntry.id) || []
      );
      setSelectedEntry(null);
    } catch (error) {
      console.error(error);
    }
  };

  const getStatusColor = (status: number) => {
    switch (status) {
      case 0:
        return { text: "#000", background: "#f0f0f0" };
      case 1:
        return { text: "#fff", background: "#ffa500" };
      case 2:
        return { text: "#fff", background: "#008000" };
      default:
        return { text: "#000", background: "#d3d3d3" };
    }
  };

  if (!entries) {
    return <CircularProgress />;
  }

  if (entries.length === 0) {
    return <Typography>No entries found.</Typography>;
  }

  return (
    <Paper style={{ padding: "1rem", marginTop: "1rem" }}>
      <Typography variant="h6">Database Entries</Typography>
      <List>
        {entries.map((entry) => (
          <ListItemButton
            key={entry.id}
            onClick={() => setSelectedEntry(entry)}
          >
            <ListItemText
              primary={`ID: ${entry.id}, Filename: ${entry.filename}`}
              secondary={
                <span
                  style={{
                    fontWeight: "bold",
                    color: getStatusColor(entry.status).text,
                    backgroundColor: getStatusColor(entry.status).background,
                    padding: "0.2rem 0.5rem",
                    borderRadius: "4px",
                  }}
                >
                  {statusMap[entry.status] || entry.status}
                </span>
              }
            />
          </ListItemButton>
        ))}
      </List>

      {selectedEntry && (
        <Paper
          style={{
            padding: "1rem",
            marginTop: "1rem",
          }}
        >
          <Typography variant="h6">Selected Entry Details</Typography>
          <Typography variant="body1">ID: {selectedEntry.id}</Typography>
          <Typography variant="body1">Filename: {selectedEntry.filename}</Typography>
          <Typography
            variant="body1"
            style={{ fontWeight: "bold" }}
          >
            Status: {" "}
            <span
              style={{
                color: getStatusColor(selectedEntry.status).text,
                backgroundColor: getStatusColor(selectedEntry.status).background,
                padding: "0.2rem 0.5rem",
                borderRadius: "4px",
              }}
            >
              {statusMap[selectedEntry.status] || selectedEntry.status}
            </span>
          </Typography>
          <Typography variant="body1">Extracted Data:</Typography>
          <pre>{JSON.stringify(selectedEntry.extracted_data, null, 2)}</pre>

          <Button
            variant="contained"
            color="primary"
            onClick={handleMenuOpen}
            style={{ marginTop: "1rem" }}
          >
            Change Status
          </Button>

          <Button
            variant="contained"
            color="secondary"
            onClick={handleDelete}
            style={{ marginTop: "1rem", marginLeft: "1rem" }}
          >
            Delete Entry
          </Button>

          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            {Object.entries(statusMap).map(([key, value]) => (
              <MenuItem
                key={key}
                onClick={() => handleStatusChange(Number(key))}
              >
                {value}
              </MenuItem>
            ))}
          </Menu>
        </Paper>
      )}
    </Paper>
  );
}
