# ontap / cluster_peer

This role is used to create cluster peer relationships.

## tasks

- create : create a cluster peer relationship (required credentials : ontap)

## Input

- cluster_peer[0].management_ip
- cluster_peer[0].intercluster_ips
- cluster_peer[0].name
- cluster_peer[1].name
- cluster_peer[1].intercluster_ips
- cluster_peer[1].management_ip

## Notes


The cluster_peer variable is a list of 2 dictionaries. Each dictionary contains the following keys:

- management_ip : the management IP of the cluster
- intercluster_ips : the intercluster LIFs of the cluster
- name : the name of the cluster

The order is not relevant, the first dictionary can be the local cluster or the remote cluster.