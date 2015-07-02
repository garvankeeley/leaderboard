#!/bin/sh
gunicorn leaderboard.main:app --bind 127.0.0.1:8050
