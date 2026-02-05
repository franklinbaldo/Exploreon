#!/bin/bash
set -e

# Install dependencies if requirements.txt has changed or packages are missing
# For simplicity in this env, we just run pip install
echo "Checking dependencies..."
pip install -r requirements.txt > /dev/null

echo "Running tests with coverage..."
export PYTHONPATH=.
coverage run -m pytest

echo "Generating coverage report..."
# This will fail the script if coverage is under 70%
coverage report --fail-under=70
coverage html

echo "Success! Tests passed and coverage is above 70%."
echo "View detailed report at htmlcov/index.html"
