#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch $SRVHOME/logs/gunicorn.log
touch $SRVHOME/logs/access.log
tail -n 0 -f $SRVHOME/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn postal.wsgi:application \
    --name postal \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=$SRVHOME/logs/gunicorn.log \
    --access-logfile=$SRVHOME/logs/access.log \
    "$@"
