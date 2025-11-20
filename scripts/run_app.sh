#!/bin/bash

# 1. Navigate to project directory (assuming script is run from root)
# This variable gets the directory where the script is stored
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$SCRIPT_DIR/.."

cd $PROJECT_DIR

# 2. Activate Virtual Environment (Adjust path if necessary)
# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 3. Run Streamlit in background using nohup
echo "Starting Streamlit App..."
nohup streamlit run main.py --server.port 8501 > streamlit.log 2>&1 &

echo "App is running in background. Logs are in streamlit.log"