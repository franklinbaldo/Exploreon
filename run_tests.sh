#!/bin/bash
set -e

# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
coverage run -m pytest
coverage report
