# Set the base image to Alpine Linux
FROM alpine:3.17.3

# Update package list and install bash, Python, and required dependencies
RUN apk update && \
    apk add --no-cache bash python3 py3-pip && \
    apk add build-base python3-dev libffi-dev

# Copy your aichan application and other necessary files
COPY ./app /app

# Add this line to copy the .env file if required (not needed if volume is mapped)
COPY .env /app/.env

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the startup script into the container
COPY startup.sh /startup.sh

# Give execution rights on the startup script
RUN chmod +x /startup.sh

# Use the startup script as the entry point
ENTRYPOINT ["/startup.sh"]
