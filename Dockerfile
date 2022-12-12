FROM python:3.9

# create the app user
RUN addgroup --system app && adduser --system --group app

WORKDIR /app/

# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# ensures that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application (e.g. django logs)
# in real time. Equivalent to python -u: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
      libprotobuf-dev \
      # libgtk2.0-dev \
      # pkg-config \
      protobuf-compiler\
      cmake \
      build-essential \
      && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./app /app
RUN chmod +x start.sh
RUN chmod +x start-reload.sh

ENV PYTHONPATH=/app

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
# Switch to a non-root user, which is recommended by Heroku.
USER app

CMD ["./start.sh"]

