# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (including git for gemini-cli if needed, and curl)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Gemini CLI (assuming it's available via pip or a similar method)
# Note: In a real scenario, we'd ensure the gemini-cli is properly authenticated/configured.
RUN pip install gemini-cli

# Copy the current directory contents into the container at /app
COPY . .

# Create logs directory and ensure it can be used for volume mounting
RUN mkdir -p logs && touch logs/gateway.log

# Expose the port the app runs on
EXPOSE 8000

# Run main.py when the container launches
CMD ["python", "src/main.py"]
