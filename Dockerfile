# Start from a base Python image
FROM python:3.10-slim

# Install Git LFS
RUN apt-get update && \
    apt-get install -y --no-install-recommends git-lfs && \
    rm -rf /var/lib/apt/lists/* && \
    git lfs install

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available outside this container
EXPOSE 8000

# Execute the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
