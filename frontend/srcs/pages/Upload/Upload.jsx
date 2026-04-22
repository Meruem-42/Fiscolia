import { Link } from 'react-router-dom';
import { useState, useRef } from "react";

const UPLOAD_URL = "/api/upload";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null);
  const inputRef = useRef(null);

  const handleFile = (f) => {
    if (!f) return;
    setFile(f);
    setStatus(null);
  };

  const handleInputChange = (e) => handleFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setStatus("uploading");

    try {
      const response = await fetch(UPLOAD_URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}`);
      }

      setStatus("success");
    } catch (err) {
      console.error(err);
      setStatus("error");
    }
  };

  return (
    <div style={{ textAlign: "center", alignContent: "center" }}>
      <h1 style={{ color: "#000091" }}>Fiscolia uploading center</h1>

      <div>
        <p>Choose a file</p>
        <input
          ref={inputRef}
          type="file"
          onChange={handleInputChange}
        />
      </div>

      {file && <p>{file.name}</p>}

      {status === "uploading" && <p>Uploading...</p>}
      {status === "success" && <p>File uploaded with success ✓</p>}
      {status === "error" && <p>Failed to upload file. Try again.</p>}

      <div>
        <button type="button" onClick={handleUpload} disabled={!file || status === "uploading"}>
          Send file to server
        </button>
      </div>

      <div>
        <Link to="/">
          <button>Return to home Page</button>
        </Link>
      </div>
    </div>
  );
}