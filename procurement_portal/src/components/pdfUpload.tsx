import { useState, ChangeEvent } from "react";
import { Button, CircularProgress, Paper, Typography } from "@mui/material";
import { extractPdf } from "../api";

interface PdfUploadProps {
  setEntries: React.Dispatch<React.SetStateAction<any[]>>;
}

export default function PdfUpload({ setEntries }: PdfUploadProps) {
  const [file, setFile] = useState<File>();
  const [busy, setBusy] = useState(false);

  const onChoose = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) setFile(e.target.files[0]);
  };

  const refreshEntries = async () => {
    try {
      const response = await fetch("http://localhost:5000/entries");
      if (!response.ok) {
        throw new Error("Failed to fetch updated entries");
      }
      const updatedEntries = await response.json();
      setEntries(updatedEntries);
    } catch (error) {
      console.error("Error refreshing entries:", error);
    }
  };

  const onUpload = async () => {
    if (!file) return;
    setBusy(true);
    try {
      await extractPdf(file);
      await refreshEntries(); // Refresh the entries after uploading
    } finally {
      setBusy(false);
    }
  };

  return (
    <Paper style={{ padding: "1rem", marginTop: "1rem" }}>
      <Typography variant="h6">Upload a PDF</Typography>
      <input
        type="file"
        accept="application/pdf"
        onChange={onChoose}
        style={{ margin: "1rem 0" }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={onUpload}
        disabled={!file || busy}
      >
        {busy ? <CircularProgress size={24} /> : "Upload"}
      </Button>
    </Paper>
  );
}
