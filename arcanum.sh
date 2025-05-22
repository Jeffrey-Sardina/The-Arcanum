#! /bin/bash

cam_id=$1
python -u arcanum.py $cam_id -db 1> logs/arcanum.cmd.log 2> logs/arcanum.err.log &
python -m keep_presence
