# Base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Ensure the model file is copied
COPY Skin_Disease_Pred-CNN-/backend/saved_model/skin_disease_model.h5 /app/saved_model/skin_disease_model.h5

# Expose the port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
