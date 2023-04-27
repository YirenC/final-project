import React, { useState } from "react";
import axios from "axios";
import Dropzone from "react-dropzone";
import "./style.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [genre, setGenre] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  axios.defaults.headers.post["Content-Type"] = "multipart/form-data";

  const handleDrop = (files) => {
    setSelectedFile(files[0]);
  };

  const MUSIC_API_URL = "http://127.0.0.1:5000";

  const handleUpload = () => {
    const formData = new FormData();
    formData.append("file", selectedFile);
    try {
      axios
        .post(MUSIC_API_URL, formData)
        .then((response) => {
          console.log(response.data);
          setGenre(response.data.genre);
          setRecommendations(response.data.recommendations);
        })
        .catch((error) => {
          console.error(error);
        });
    } catch (error) {
      console.error("Error matching music:", error);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Music Recommender</h1>
      </header>
      <main>
        <div className="upload-container">
          <Dropzone onDrop={handleDrop}>
            {({ getRootProps, getInputProps }) => (
              <button {...getRootProps()} className="dropzone">
                <input {...getInputProps()} />
                <p>
                  Drag and drop a music file here, or click to select a file
                </p>
              </button>
            )}
          </Dropzone>
          {selectedFile && (
            <div className="file-info">
              <p>Selected file: {selectedFile.name}</p>
              <button onClick={handleUpload}>Upload and Recommend</button>
            </div>
          )}
        </div>
        {genre && (
          <div className="genre">
            <p>
              Maybe you like <b>{genre}</b>?
            </p>
          </div>
        )}
        {recommendations.length > 0 && (
          <div className="recommendations">
            <h3>Recommendations For You:</h3>
            <ul>
              {recommendations.map((recommendation) => (
                <li>
                  <p>{recommendation}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
