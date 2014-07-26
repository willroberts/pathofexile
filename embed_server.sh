#!/bin/bash
gunicorn -w 2 -b 0.0.0.0:8080 pathofexile.forum.embed_server:app
