#!/bin/bash

#launch model server
/model/src/model_server/run_model_server.sh &

#launch dipnet script
python /model/src/model_server/research/run_dipnet.py $@
