const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

// --- Mock Data Store (Simulating the Unified DB) ---
let talentRecords = [
    { id: 1, name: "Alice Smith", role: "Software Engineer", department: "Engineering" },
    { id: 2, name: "Bob Johnson", role: "DevOps Specialist", department: "DevOps" }
];

let workflowStatuses = [
    { id: 101, talentId: 1, task: "Onboarding Process", status: "In Progress", assignedTo: "Alice Smith" },
    { id: 102, talentId: 2, task: "CI/CD Pipeline Setup", status: "Pending Review", assignedTo: "Bob Johnson" }
];

// --- API Endpoints ---

/**
 * HR Endpoint: Talent Management
 */
app.get('/api/talent', (req, res) => {
    res.json(talentRecords);
});

app.post('/api/talent', (req, res) => {
    const newTalent = { id: talentRecords.length + 1, ...req.body };
    talentRecords.push(newTalent);
    res.status(201).json(newTalent);
});

/**
 * DevOps Endpoint: Workflow Management
 */
app.get('/api/workflow', (req, res) => {
    res.json(workflowStatuses);
});

app.post('/api/workflow', (req, res) => {
    const newWorkflow = { id: workflowStatuses.length + 1, ...req.body };
    workflowStatuses.push(newWorkflow);
    res.status(201).json(newWorkflow);
});

// --- Unified Endpoint Example (Conceptual Linkage) ---
app.get('/api/unified/:talentId', (req, res) => {
    const talent = talentRecords.find(t => t.id === parseInt(req.params.talentId));
    const workflows = workflowStatuses.filter(w => w.talentId === talent.id);

    if (!talent) {
        return res.status(404).json({ message: "Talent record not found" });
    }

    res.json({
        talent: talent,
        workflows: workflows
    });
});


app.listen(PORT, () => {
    console.log(`Unified Platform Backend running on http://localhost:${PORT}`);
});