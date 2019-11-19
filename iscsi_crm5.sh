#!/bin/bash
# Excuting this script takes about 15 sec
# Parameters needed for crm configuration
lun_name=$1
target_iqn=$2 #iqn.2019-10.feixitek.com:test0 ## iqn.2019-10:feixitek.com:test will cause the resource not started as expected
lun=$3 #0,1
path=$4 #/dev/sdc
group_name=$5
p_off_name=$6 #p_iscsi_portblock_off_drbd0

echo $lun_name $target_iqn $lun $path $group_name $p_off_name

# Steps
crm conf primitive $lun_name iSCSILogicalUnit params target_iqn=$target_iqn implementation=lio-t lun=$lun path=$path op monitor interval=10s meta target-role=Stopped

crm configure modgroup $group_name add $lun_name before $p_off_name

crm res start $lun_name

crm res ref
sleep 10
#crm res ref
#sleep 20

#crm status
crm res show
