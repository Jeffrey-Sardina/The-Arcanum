#! /bin/bash

cam_id=$1 # if not provided, your default webcam will be used.
python -u arcanum.py $cam_id 1> logs/arcanum.cmd.log 2> logs/arcanum.err.log &
python -m keep_presence # https://github.com/carrot69/keep-presence/
# p=$(ps -ef | grep "python -m keep_presence" | grep -v "grep" | awk '{print $2}')

