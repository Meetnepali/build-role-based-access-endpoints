#!/bin/bash
set -e
source venv/bin/activate
docker run -p 8000:8000 fastapi-profile-app
