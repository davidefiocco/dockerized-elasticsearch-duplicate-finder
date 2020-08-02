# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn:python3.7

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt --trusted-host pypi.python.org

# Copy the current directory contents into the container at /app
ADD . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

