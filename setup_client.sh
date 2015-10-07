#!/bin/bash
eval `ssh-agent`
ssh-add id_rackspace


ssh -l root $1 killall -9 java
ssh -l root $1 apt-get update 
ssh -l root $1 apt-get -y install software-properties-common python-software-properties
ssh -l root $1 add-apt-repository ppa:webupd8team/java
ssh -l root $1 apt-get update
ssh -l root $1 apt-get -y install oracle-java8-installer

#scp -C -r client/* root@$1:~/
ssh -l root $1 rm -rf YCSB*
ssh -l root $1 wget https://www.dropbox.com/s/6h6dlykkzdm416d/YCSB.tar.gz?dl=1 
ssh -l root $1 tar -xvzf YCSB.tar.gz?dl=1 
