#!/bin/bash
echo "Copying custom pg_hba.conf to $PGDATA/pg_hba.conf"
cp /tmp/pg_hba.conf $PGDATA/pg_hba.conf
chmod 0600 $PGDATA/pg_hba.conf