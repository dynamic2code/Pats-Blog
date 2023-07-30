# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /flaskapp

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies using pip in the virtual environment
RUN python -m venv venv
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Set the command to run your application
CMD ["python3", "app.py"]
