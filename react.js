import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {
        fetchSummary();
    }, []);

    const fetchSummary = async () => {
        setLoading(true);
        try {
            const response = await axios.get('/http://192.168.117.17:5500//api/summary');
            setSummary(response.data.summary);
        } catch (error) {
            setSummary('Error fetching summary. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>Student CAT Performance</h1>
            <button className="floating-button" onClick={() => setShowModal(true)}>Deep Insights</button>
            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <button className="close-button" onClick={() => setShowModal(false)}>X</button>
                        {loading ? (
                            <p>Loading...</p>
                        ) : (
                            <p>{summary}</p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
