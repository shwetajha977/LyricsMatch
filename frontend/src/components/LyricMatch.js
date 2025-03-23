import React, { useState } from "react";
import axios from "axios";
import "../index.css"; // Import external CSS file

const LyricMatch = () => {
    const [lyric, setLyric] = useState("");
    const [correctTitle, setCorrectTitle] = useState("");
    const [guess, setGuess] = useState("");
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const fetchLyric = async () => {
        setLoading(true);
        setLyric("");
        setGuess("");
        setMessage("");

        try {
            const response = await axios.get("http://127.0.0.1:5000/generate");
            setLyric(response.data.lyric);
            setCorrectTitle(response.data.song_title);
        } catch (error) {
            console.error("Error fetching lyric:", error);
            setMessage("⚠️ Failed to fetch lyric.");
        }
        setLoading(false);
    };

    const checkAnswer = async () => {
        if (!guess.trim()) {
            setMessage("⚠️ Please enter a song title.");
            return;
        }

        try {
            const response = await axios.post("http://127.0.0.1:5000/check", {
                guess,
                correct_title: correctTitle
            });
            if (response.data.result === "correct") {
                setMessage("✅ Correct!");
            } else {
                setMessage(`❌ Incorrect! The correct song is: ${response.data.correct_title.split(" - ")[0]}`);
            }
        } catch (error) {
            console.error("Error checking answer:", error);
            setMessage("⚠️ Error checking answer.");
        }
    };

    return (
        <div className="container">
            <h1>🎵 Lyric Match 🎵</h1>
            <button className="btn" onClick={fetchLyric} disabled={loading}>
                {loading ? "Loading..." : "Generate Lyric Snippet"}
            </button>
            {loading && <div className="loading-spinner"></div>}

            {lyric && (
                <>
                    <p className="lyric"><b>Lyric Snippet:</b> {lyric}</p>
                    <input 
                        type="text" 
                        placeholder="Enter song title" 
                        value={guess} 
                        onChange={(e) => setGuess(e.target.value)} 
                        className="input"
                    />
                    <button className="btn check-btn" onClick={checkAnswer}>Check Answer</button>
                </>
            )}

            <p className="message">{message}</p>
        </div>
    );
};

export default LyricMatch;
