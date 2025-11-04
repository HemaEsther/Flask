import React, { useState } from "react";
import axios from "axios";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Please select a CSV file first!");

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(res.data);
    } catch (error) {
      alert("Error uploading file. Check if Flask server is running.");
    } finally {
      setLoading(false);
    }
  };

  const renderTable = () => {
    if (!response?.summary?.columns) return null;

    const columns = Object.entries(response.summary.columns);

    return (
      <table style={styles.table}>
        <thead>
          <tr>
            <th>Column</th>
            <th>Type</th>
            <th>Mean</th>
            <th>Median</th>
            <th>Min</th>
            <th>Max</th>
            <th>Missing</th>
            <th>Unique</th>
          </tr>
        </thead>
        <tbody>
          {columns.map(([name, info]) => (
            <tr key={name}>
              <td>{name}</td>
              <td>{info.dtype}</td>
              <td>{info.mean ? info.mean.toFixed(2) : "-"}</td>
              <td>{info.median ? info.median.toFixed(2) : "-"}</td>
              <td>{info.min ?? "-"}</td>
              <td>{info.max ?? "-"}</td>
              <td>{info.missing_values}</td>
              <td>{info.unique_values}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div style={styles.card}>
      <input type="file" accept=".csv" onChange={handleFileChange} style={styles.input} />
      <button onClick={handleUpload} style={styles.button}>
        {loading ? "Cleaning..." : "Upload & Clean"}
      </button>

      {response && (
        <div style={styles.result}>
          <h2 style={styles.heading}>{response.message}</h2>
          <h3 style={styles.subheading}>📊 Summary Statistics</h3>

          <div style={styles.scrollBox}>{renderTable()}</div>

          <p style={{ marginTop: "1rem", fontSize: "0.95rem", color: "#94a3b8" }}>
            Rows: {response.summary.num_rows} | Columns: {response.summary.num_columns}
          </p>
        </div>
      )}
    </div>
  );
}

const styles = {
  card: {
    backgroundColor: "#1e293b",
    padding: "2rem",
    borderRadius: "1.2rem",
    textAlign: "center",
    width: "70%",
    maxWidth: "850px",
    boxShadow: "0 0 25px rgba(255,255,255,0.08)",
  },
  input: {
    marginBottom: "1rem",
    fontSize: "1.1rem",
    color: "#f1f5f9",
  },
  button: {
    backgroundColor: "#3b82f6",
    color: "white",
    fontSize: "1.2rem",
    padding: "0.7rem 2rem",
    border: "none",
    borderRadius: "0.6rem",
    cursor: "pointer",
  },
  result: {
    marginTop: "2rem",
    textAlign: "center",
    fontSize: "1rem",
  },
  scrollBox: {
    maxHeight: "300px",
    overflowY: "auto",
    backgroundColor: "#0f172a",
    borderRadius: "0.8rem",
    padding: "1rem",
  },
  heading: {
    fontSize: "1.5rem",
    color: "#22c55e",
    marginBottom: "0.6rem",
  },
  subheading: {
    marginBottom: "1rem",
    color: "#f1f5f9",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: "0.95rem",
    color: "#e2e8f0",
  },
  th: {
    backgroundColor: "#334155",
    padding: "0.6rem",
    textAlign: "left",
  },
  td: {
    padding: "0.6rem",
    borderBottom: "1px solid #334155",
  },
};

export default FileUpload;
