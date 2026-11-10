# Use a lightweight official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your server.py and index.html into the container
COPY . .

# Expose port 8000 so other containers can reach it
EXPOSE 8000

# Start the Python web server
CMD ["python", "server.py"]
