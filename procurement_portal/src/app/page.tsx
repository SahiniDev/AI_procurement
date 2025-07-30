"use client";

import React, { useEffect, useState } from "react";
import PdfUpload from "../components/pdfUpload";
import EntriesList from "../components/entriesList";

export default function Home() {
  const [msg, setMsg] = useState("…loading…");
  const [entries, setEntries] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:5000/")
      .then((r) => r.json())
      .then((d) => setMsg(d.message))
      .catch(() => setMsg("Backend not reachable"));
  }, []);

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Procurement Portal</h1>
      <p>{msg}</p>
      <PdfUpload setEntries={setEntries} />
      <EntriesList entries={entries} />
    </main>
  );
}
