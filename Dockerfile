FROM python:2.7
ENV PYTHONUNBUFFERED 1

# Set the file maintainer (your name - the file's author)
MAINTAINER Lauri Junkkari

# Set env variables used in this Dockerfile
ENV SRC=.
ENV SRVHOME=/srv
ENV SRVPROJ=/srv/app

# Create application subdirectories
WORKDIR $SRVHOME
RUN mkdir media static logs
VOLUME ["$SRVHOME/media/","$SRVHOME/static/"]

ENV STATIC_ROOT=$SRVHOME/static
ENV MEDIA_ROOT=$SRVHOME/media

# Copy application source code to SRCDIR
COPY $SRC $SRVPROJ

# Install Python dependencies
RUN pip install -r $SRVPROJ/requirements.txt

# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
WORKDIR $SRVPROJ
COPY $SRC/scripts/docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
