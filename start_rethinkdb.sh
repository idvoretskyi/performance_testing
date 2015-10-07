#!/bin/bash

eval `ssh-agent`
ssh-add id_rackspace

#nohup rethinkdb --bind all -d /mnt/rethinkdb_data -j 104.130.21.31 --cache-size 64000 &

ssh -oStrictHostKeyChecking=no -l root $1 bash -c "'echo 524240 > /proc/sys/vm/max_map_count'"
ssh -oStrictHostKeyChecking=no -l root $1 killall rethinkdb
sleep 60
ssh -oStrictHostKeyChecking=no -l root $1 killall -9 rethinkdb
ssh -oStrictHostKeyChecking=no -l root $1 ./rethinkdb --bind all -d /mnt/rethinkdb_data -j 104.130.21.31 --cache-size 64000 --daemon



