# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY service/ ./service/

# Set environment variables
ENV FLASK_APP=service:app
ENV PORT=8080

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--log-level", "info", "service:app"]
