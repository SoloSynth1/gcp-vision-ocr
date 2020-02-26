FROM python:3.7-slim

COPY requirements.txt ./

RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
ENV PORT 8080

WORKDIR $APP_HOME
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD python app.py
