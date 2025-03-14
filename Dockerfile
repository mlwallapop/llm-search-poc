# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 7777
EXPOSE 7777

# Run the Streamlit app on port 7777
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port", "7777", "--server.enableCORS", "false"]
