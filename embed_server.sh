#!/bin/bash
echo 'Starting two gunicorn workers...'
source env/bin/activate || {
    echo 'Missing virtualenv in env/'
    exit 1
}
gunicorn -w 2 -b 0.0.0.0:8080 pathofexile.forum.embed_server:app &
echo 'Done! App is running on http://0.0.0.0:8080'
