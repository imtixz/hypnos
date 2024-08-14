# Start with the latest Docker image
FROM docker:latest

# Set the working directory
WORKDIR /hypnos

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    curl \
    bash \
    github-cli

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Copy the rest of the content
COPY . .

# Create the necessary directories
RUN mkdir -p playbook
RUN mkdir -p apps