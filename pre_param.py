# coding:utf-8
import re

strA = '''node 1: server1 \
        attributes standby=off
node 2: server2 \
        attributes standby=off
primitive drbd_res ocf:linbit:drbd \
        params drbd_resource=r0 \
        op monitor interval=29s role=Master \
        op monitor interval=31s role=Slave
primitive l_hi iSCSILogicalUnit \
        params target_iqn="iqn.2019-10.feixitek.com:test0" implementation=lio-t lun=1 path="/dev/sdc" \
        op monitor interval=10s \
        meta target-role=Started
primitive l_test0 iSCSILogicalUnit \
        params target_iqn="iqn.2019-10.feixitek.com:test0" implementation=lio-t lun=0 path="/dev/drbd1" \
        op monitor interval=10s \
        meta target-role=Started
primitive p_iscsi_portblock_off_drbd0 portblock \
        params ip=10.203.1.53 portno=3260 protocol=tcp action=unblock \
        op start timeout=20 interval=0 \
        op stop timeout=20 interval=0 \
        op monitor timeout=20 interval=20
primitive p_iscsi_portblock_on_drbd0 portblock \
        params ip=10.203.1.53 portno=3260 protocol=tcp action=block \
        op start timeout=20 interval=0 \
        op stop timeout=20 interval=0 \
        op monitor timeout=20 interval=20 \
        meta target-role=Started
primitive t_test0 iSCSITarget \
        params iqn="iqn.2019-10.feixitek.com:test0" implementation=lio-t allowed_initiators="iqn.1993-08.org.debian:01:78ddb2d6247e iqn.1993-08.org.debian:01:e3589b7c9ce" portals="10.203.1.53:3260" \
        op start timeout=20 interval=0 \
        op stop timeout=20 interval=0 \
        op monitor interval=20 timeout=40 \
        meta target-role=Started
primitive vip IPaddr2 \
        params ip=10.203.1.53 cidr_netmask=24 \
        op monitor interval=10 timeout=20 \
        meta target-role=Started
group g_service p_iscsi_portblock_on_drbd0 vip t_test0 l_test0 l_hi p_iscsi_portblock_off_drbd0
ms drbd_master_slave drbd_res \
        meta master-max=1 master-node-max=1 clone-max=2 clone-node-max=1 notify=true
colocation fs_with_DRBD inf: g_service drbd_master_slave:Master
order o_g_service inf: drbd_master_slave:promote g_service:start
property cib-bootiap-options: \
        have-watchdog=false \
        dc-version=1.1.18-2b07d5c5a9 \
'''


strB = '''        params iqn="iqn.2019-10.feixitek.com:test0" implementation=lio-t allowed_initiators="iqn.1993-08.org.debian:01:78ddb2d6247e iqn.1993-08.org.debian:01:e3589b7c9ce" portals="10.203.1.53:3260" \
'''

strC = '''group g_service p_iscsi_portblock_on_drbd0 vip t_test0 l_test0 l_hi p_iscsi_portblock_off_drbd0
'''

strD = '''params iqn="iqn.2019-10.feixitek.com:test0" implementation=lio-t allowed_initiators="iqn.1993-08.org.debian:01:78ddb2d6247e iqn.1993-08.org.debian:01:e3589b7c9ce" portals="10.203.1.53:3260" \
'''

strE = '''primitive p_iscsi_portblock_off_drbd0 portblock \
        params ip=10.203.1.53 portno=3260 protocol=tcp action=unblock \
        op start timeout=20 interval=0 \
        op stop timeout=20 interval=0 \
        op monitor timeout=20 interval=20'''

strF = '''primitive p_iscsi_portblock_off_drbd0 portblock \
primitive p_iscsi_portblock_on_drbd0 portblock \
group g_service p_iscsi_portblock_on_drbd0 vip t_test0 l_test0 l_hi p_iscsi_portblock_off_drbd0'''

strG = '''        params target_iqn="iqn.2019-10.feixitek.com:test0" implementation=lio-t lun=1 path="/dev/sdc" \
        params target_iqn="iqn.2019-10.feixitek.com:test0" implementation=lio-t lun=0 path="/dev/drbd1" \
        '''
strH = '''        params iqn=iqn.2019-09.org.iscsitarget implementation=lio-t allowed_initiators="iqn.1993-08.org.debian:01:e3589b7c9ce" portals="10.203.1.33:3260" \
'''
strI = '''
Last updated: Thu Nov  7 12:44:55 2019          Last change: Thu Nov  7 12:44:32 2019 by root via cibadmin on klay1
Stack: corosync
Current DC: klay1 (version 1.1.14-70404b0) - partition with quorum
2 nodes and 9 resources configured

Online: [ klay1 klay2 ]

Full list of resources:

 Master/Slave Set: ms_drbd_linstordb [p_drbd_linstordb]
     Masters: [ klay2 ]
     Slaves: [ klay1 ]
 Resource Group: g_linstor
     p_iscsi_portblock_on_drbd0 (ocf::heartbeat:portblock):     Started klay2
     p_fs_linstordb     (ocf::heartbeat:Filesystem):    Started klay2
     p_linstor-controller       (systemd:linstor-controller):   Started klay2
     vip        (ocf::heartbeat:IPaddr2):       Started klay2
     iscsi_target_test  (ocf::heartbeat:iSCSITarget):   Started klay2
     l_test1    (ocf::heartbeat:iSCSILogicalUnit):      Stopped
     p_iscsi_portblock_off_drbd0        (ocf::heartbeat:portblock):     Stopped
     l_test2    (ocf::heartbeat:iSCSILogicalUnit):      Started klay1
'''

status = 'off'
re_iqn = re.compile('(?<=params iqn=).*(?= implementation)')
re_group_name = re.compile('(?<=group )[\w]*\\b')
re_p_off_name = re.compile('(?<=primitive )[\w]*'+ status +'[\w]*\\b')
re_IP = re.compile('(?<=portals=")((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)')
re_lun = re.compile('(?<=lun=)(\d*)')

def get_iqn(i):
    result = re_iqn.search(i)
    if result:
        print result.group().strip('"')
        return result.group().strip('"')
    else:
        print('get_iqn fail')


def get_group_name(i):
    result = re_group_name.search(i)
    if result:
        print result.group().strip('"')
        return result.group().strip('"')
    else:
        print('get_group fail')

def get_p_off_name(i):
    result = re_p_off_name.search(i)
    if result:
        print result.group().strip('"')
        return result.group().strip('"')
    else:
        print('get_p_off fail')

def get_IP(i):
    result = re_IP.search(i)
    if result:
        print result.group().strip('"')
        return result.group().strip('"')
    else:
        print('get_IP fail')
        
def get_lun_list(i):
    result = re_lun.findall(i)
    if result:
        for m in range(len(result)):
            result[m] = int(result[m])
        print result
        return result
    else:
        print('get_lun_list fail')

def get_iscsi_st(i,name):
    re_n = re.compile('\\b' + name + '.*')
    re_iscsi_staus = re.compile('(?<=ocf::heartbeat:iSCSILogicalUnit\):)\s*\w*')
    if re_n.search(i):
        stra = re_n.search(i).group()
        result = re_iscsi_staus.search(stra).group().strip(' ')
        print result.strip()
        return result.strip()
    else: 
        return None

if __name__ == '__main__':
    # tests
    get_iqn(strB)
    get_iqn(strH)
    get_group_name(strC)
    get_p_off_name(strA)
    get_IP(strD)
    get_lun_list(strG)
    get_iscsi_st(strI,"l_test1")
