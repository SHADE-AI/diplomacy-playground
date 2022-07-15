#!/bin/bash

SDIR=$1
LOG=$2
cp ${SDIR}/tmp/server.json ${SDIR}/data/
#python -m diplomacy.server.run --server_dir $SDIR >> ${SDIR}/logs/$LOG 2>&1

python -m diplomacy.server.run --server_dir $SDIR
