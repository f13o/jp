#!/bin/sh
open http://localhost:9999
python3 -m http.server 9999 -d "$(dirname "$0")"
