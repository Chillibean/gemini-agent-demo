# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application file into the container at /app
COPY example_agent/ example_agent/
COPY api.py .
COPY example_agent/ .

EXPOSE 4000

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "4000"]