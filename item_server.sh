#!/bin/bash
echo 'Starting two gunicorn workers...'
gunicorn -w 2 -b 0.0.0.0:8080 pathofexile.forum.item_server:app &
echo 'Done! App is running on http://0.0.0.0:8080'
