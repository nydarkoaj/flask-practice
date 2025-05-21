# Use the python image that is compatible with the current version of Flask
FROM python:3.13  

# create a directory for the app
WORKDIR /code

# Copy requirements to the directory and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . . 

# Expose the port the app runs on
EXPOSE 5000

# command to run the app
CMD ["flask","run","--host=0.0.0.0"]