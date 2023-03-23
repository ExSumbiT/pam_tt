# Use the official Selenium Chrome image
FROM selenium/standalone-chrome:4.1.3

# Install Python and other dependencies
USER root
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .
COPY .env .

# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY wlogin.py .

# Run the Python script
CMD ["python3", "wlogin.py"]
