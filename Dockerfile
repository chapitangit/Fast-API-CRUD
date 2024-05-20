# FROM python:3.10.5

# WORKDIR /code

# COPY ./requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt

# COPY ./apps ./apps

# CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "80"]



# Use a specific version of Python
FROM python:3.10.5-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the application port
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
