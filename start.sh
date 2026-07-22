#!/bin/bash
cd /Users/felipeflose/Startup_Flose
# Load environment variables if needed
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Run backend in the background and log to backend.log
npm run backend > backend.log 2>&1 &

# Run frontend in the background and log to frontend.log
npm run dev > frontend.log 2>&1 &

# Wait for background processes
wait
