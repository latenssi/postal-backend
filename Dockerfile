FROM python:2.7

# Set the file maintainer (your name - the file's author)
MAINTAINER Lauri Junkkari

# Set env variables used in this Dockerfile
ENV POSTAL_SRC=.
ENV POSTAL_SRVHOME=/srv
ENV POSTAL_SRVPROJ=/srv/postal

# Create application subdirectories
WORKDIR $POSTAL_SRVHOME
RUN mkdir media static logs
VOLUME ["$POSTAL_SRVHOME/media/", "$POSTAL_SRVHOME/static/", "$POSTAL_SRVHOME/logs/"]

ENV POSTAL_STATIC_ROOT=$POSTAL_SRVHOME/static
ENV POSTAL_MEDIA_ROOT=$POSTAL_SRVHOME/media

# Copy application source code to SRCDIR
COPY $POSTAL_SRC $POSTAL_SRVPROJ

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r $POSTAL_SRVPROJ/requirements.txt -U

# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
WORKDIR $POSTAL_SRVPROJ
COPY $POSTAL_SRC/scripts/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
