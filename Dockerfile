FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip

# Copy entire project first (necessary to install local modules)
COPY . .

# Now install your project locally
RUN pip install -e .  

EXPOSE 7777

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port", "7777", "--server.enableCORS", "false"]
