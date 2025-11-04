import React from "react";
import FileUpload from "./components/FileUpload";

function App() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🧹 Data Cleaning Tool</h1>
      <p style={styles.subtitle}>
        Upload your CSV file to get cleaned data and quick summary insights
      </p>
      <FileUpload />
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#0f172a",
    color: "#f1f5f9",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "2rem",
    fontFamily: "Segoe UI, sans-serif",
  },
  title: { fontSize: "2.8rem", marginBottom: "0.8rem" },
  subtitle: { color: "#94a3b8", marginBottom: "2.5rem", fontSize: "1.2rem" },
};

export default App;
