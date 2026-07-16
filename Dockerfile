FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create model directory if it doesn't exist
RUN mkdir -p model

# Train the model
RUN python model/train_model.py

# Make port 80 available
EXPOSE 80

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"] 