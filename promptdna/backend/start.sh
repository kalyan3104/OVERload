#!/bin/bash
# simple start script
export PYTHONPATH=/app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
