# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code and templates into the container` 
COPY app.py requirements.txt ./ 
COPY templates ./templates

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the app runs
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
