# Use an official Python image
FROM mcr.microsoft.com/devcontainers/python:3.11

# Set the working directory
WORKDIR /workspace

# Copy the requirements file
COPY requirements.txt /workspace/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default user
USER vscode