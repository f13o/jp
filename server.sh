#!/bin/sh
open http://localhost:9999
python3 "$(dirname "$0")/server.py" 9999
