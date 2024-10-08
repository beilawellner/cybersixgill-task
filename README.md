# README

## Overview
This project is designed to processes files containing leaked credentials and extracts all email-password pairs. The project uses a combination of Python, Boto3, Pandas to achieve this functionality. The extracted data is then saved into a CSV file.

## Prerequisites
- Docker

### Building and Running the Docker Image

docker build -t email-processor:latest .

docker run --env-file .env email-processor:latest

### Check the Logs
Logs will be generated in the app.log file and also printed to the console.

### Notes
 - The script currently supports .json, .csv, and .sql file formats for processing.