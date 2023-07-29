# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies using pip in the virtual environment
RUN python -m venv venv
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# Set the command to run your application
CMD ["python", "app.py"]