const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

/**
 * Mock database/state for workflow orchestration simulation.
 * In a real scenario, this would involve API calls to Jira and Git services.
 */
const workflowState = {
    'JIRA-123': { status: 'In Progress', gitBranch: 'feature/new-feature', lastCommit: 'abc1234' },
    'JIRA-456': { status: 'Ready for Review', gitBranch: 'develop', lastCommit: 'def5678' }
};

/**
 * Orchestrates the workflow between Jira and Git.
 * Endpoint: POST /api/orchestrate/:jiraId/git
 * Purpose: Simulates triggering a Git action based on Jira status.
 */
app.post('/api/orchestrate/:jiraId/git', (req, res) => {
    const { jiraId } = req.params;
    const { gitAction } = req.body;

    if (!workflowState[jiraId]) {
        return res.status(404).json({ error: `Jira ticket ${jiraId} not found.` });
    }

    const currentTicket = workflowState[jiraId];

    // Simple Orchestration Logic Simulation
    if (gitAction === 'commit_pending' && currentTicket.status === 'In Progress') {
        // Simulate Git operation success
        const newCommitHash = `new-commit-${Date.now()}`;
        workflowState[jiraId].lastCommit = newCommitHash;
        return res.json({
            success: true,
            message: `Successfully triggered commit pending for ${jiraId}. New state: ${currentTicket.gitBranch} committed as ${newCommitHash}`,
            updatedState: workflowState[jiraId]
        });
    } else if (gitAction === 'review_requested' && currentTicket.status === 'Ready for Review') {
         return res.json({
            success: true,
            message: `Successfully requested review for ${jiraId}. Branch is ${currentTicket.gitBranch}`,
            updatedState: workflowState[jiraId]
        });
    } else {
        return res.status(400).json({ error: `Invalid transition or state mismatch for Jira ticket ${jiraId}` });
    }
});

/**
 * Endpoint to check the current orchestration status.
 * Endpoint: GET /api/workflow/:jiraId
 */
app.get('/api/workflow/:jiraId', (req, res) => {
    const { jiraId } = req.params;
    if (!workflowState[jiraId]) {
        return res.status(404).json({ error: `Jira ticket ${jiraId} not found.` });
    }
    res.json({
        ticketId: jiraId,
        workflowStatus: workflowState[jiraId].status,
        gitBranch: workflowState[jiraId].gitBranch,
        lastCommitHash: workflowState[jiraId].lastCommit
    });
});

app.listen(port, () => {
    console.log(`Jira-Git Workflow Orchestrator API running at http://localhost:${port}`);
});