#!/bin/bash
eval `ssh-agent`
ssh-add id_rackspace

#ssh -l root $1 bash -c "'echo "deb http://download.rethinkdb.com/apt trusty main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list'"
#ssh -l root $1 bash -c "'wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -'"
#ssh -l root $1 apt-get update
#ssh -l root $1 apt-get -y install rethinkdb
ssh -l root $1 wget https://www.dropbox.com/s/hwl43qi1kwhp9sw/rethinkdb?dl=1
ssh -l root $1 mv -f rethinkdb?dl=1 rethinkdb
ssh -l root $1 chmod +x rethinkdb

ssh -l root $1 mkfs.ext4 -F /dev/sdb
ssh -l root $1 mount /dev/sdb /mnt
