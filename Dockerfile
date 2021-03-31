FROM ubuntu:18.04

# Update Software repository
RUN apt-get update

RUN apt-get install -y python3 python3-pip libsm6 libxext6 libxrender-dev

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
ENV PORT 8080

WORKDIR $APP_HOME
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD python3 app.py
