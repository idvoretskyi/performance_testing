#!/bin/bash
eval `ssh-agent`
ssh-add id_rackspace

ssh -l root $1 echo next
