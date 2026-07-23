const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

/**
 * Mock Data Store for Git Workflow Events and Structured Data
 * In a real application, this would interface with a database (PostgreSQL, MongoDB)
 */
const workflowDataStore = {
    commitHistory: [],
    pullRequests: []
};

/**
 * Service function to process incoming data and structure it.
 * Simulates the core automation logic.
 * @param {object} data - The raw data received (e.g., a commit object).
 * @returns {object} - Structured data.
 */
function structureGitData(data) {
    if (!data || !data.commitHash || !data.message) {
        throw new Error("Missing required fields: commitHash and message are mandatory.");
    }

    const structuredRecord = {
        id: Date.now() + Math.random(), // Simple unique ID generation for demo
        repository: data.repo || 'unknown',
        commitHash: data.commitHash,
        author: data.author || 'unknown_user',
        timestamp: new Date().toISOString(),
        message: data.message,
        status: data.status || 'processed'
    };

    workflowDataStore.commitHistory.push(structuredRecord);
    console.log(`[INFO] Data structured for commit: ${data.commitHash}`);
    return structuredRecord;
}

/**
 * Endpoint 1: Simulate processing a new Git commit event.
 */
app.post('/api/process-commit', (req, res) => {
    try {
        const rawData = req.body;
        const structuredData = structureGitData(rawData);
        res.status(201).json({
            message: 'Commit successfully processed and structured.',
            data: structuredData
        });
    } catch (error) {
        console.error('Error processing commit:', error.message);
        res.status(400).json({ error: error.message });
    }
});

/**
 * Endpoint 2: Simulate fetching structured workflow data.
 */
app.get('/api/workflow-data', (req, res) => {
    res.json({
        commitHistory: workflowDataStore.commitHistory,
        pullRequests: workflowDataStore.pullRequests
    });
});

/**
 * Endpoint 3: Simulate structuring a Pull Request event.
 */
app.post('/api/process-pr', (req, res) => {
    try {
        const rawData = req.body;
        // In a real system, this would involve complex logic for branching and review status
        const structuredData = {
            id: Date.now() + Math.random(),
            repo: rawData.repository || 'unknown',
            pr_number: rawData.number,
            title: rawData.title,
            status: rawData.state || 'open',
            created_at: new Date().toISOString()
        };

        workflowDataStore.pullRequests.push(structuredData);
        res.status(201).json({
            message: 'Pull Request successfully structured.',
            data: structuredData
        });
    } catch (error) {
        console.error('Error processing PR:', error.message);
        res.status(400).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Backend Service running on http://localhost:${PORT}`);
});