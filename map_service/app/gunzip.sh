#!/bin/bash
# not actually used, add to app.py to automatically log files
find data -type f -iname '*gz' -exec gunzip {} +
