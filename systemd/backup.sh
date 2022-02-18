#!/usr/bin/env bash

set -e

LOCKFILE=/tmp/diplomacy_backup.lock
SERVERDIR=/home/shade
CORRALDIR=/corral/projects/DARPA-SHADE/Admin/backups/shade.tacc.utexas.edu/

# Check existence of Corral directory
[ -d "$CORRALDIR" ] || exit 1

echo cwd $SERVERDIR
echo using lockfile $LOCKFILE
exec 200>$LOCKFILE || exit 1
flock -n 200 || exit 1
/usr/bin/rsync -av $SERVERDIR $CORRALDIR
flock -u 200

set +e

