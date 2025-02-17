# Receipts API

Receipts API built for Fetch's Receipt Processor Challenge

# Instructions

Run ./build_and_run_api.sh to build and run the Docker container
The Receipts API will then start running at 0.0.0.0:5000

# Code

- api contains the Flask app.py as well as verify_json.py, which is used to ensure incoming receipts are valid
- tests contains json files for testing purposes
- test.py uses the files in the tests folder to test the API
