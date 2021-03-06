clusters:
  - plugin_name: vanilla
    plugin_version: 2.7.1
    image: ${vanilla_two_six_image}
    node_group_templates:
      - name: worker-dn-nm
        flavor: ${ci_flavor_id}
        node_processes:
          - datanode
          - nodemanager
        volumes_per_node: 2
        volumes_size: 2
        auto_security_group: true
        node_configs:
          &ng_configs
          MapReduce:
            yarn.app.mapreduce.am.resource.mb: 256
            yarn.app.mapreduce.am.command-opts: -Xmx256m
          YARN:
            yarn.scheduler.minimum-allocation-mb: 256
            yarn.scheduler.maximum-allocation-mb: 1024
            yarn.nodemanager.vmem-check-enabled: false
      - name: worker-nm
        flavor: ${ci_flavor_id}
        node_processes:
          - nodemanager
        auto_security_group: true
        node_configs:
          *ng_configs
      - name: worker-dn
        flavor: ${ci_flavor_id}
        node_processes:
          - datanode
        volumes_per_node: 2
        volumes_size: 2
        auto_security_group: true
        node_configs:
          *ng_configs
      - name: master-rm-nn-hvs
        flavor: ${ci_flavor_id}
        node_processes:
          - namenode
          - resourcemanager
          - hiveserver
        auto_security_group: true
        node_configs:
          *ng_configs
      - name: master-oo-hs-sn
        flavor: ${ci_flavor_id}
        node_processes:
          - oozie
          - historyserver
          - secondarynamenode
        auto_security_group: true
        node_configs:
          *ng_configs
    cluster_template:
      name: vanilla271
      node_group_templates:
        master-rm-nn-hvs: 1
        master-oo-hs-sn: 1
        worker-dn-nm: 2
        worker-dn: 1
        worker-nm: 1
      cluster_configs:
        HDFS:
          dfs.replication: 1
    cluster:
      name: ${cluster_name}
    scaling:
      - operation: resize
        node_group: worker-dn-nm
        size: 1
      - operation: resize
        node_group: worker-dn
        size: 0
      - operation: resize
        node_group: worker-nm
        size: 0
      - operation: add
        node_group: worker-dn
        size: 1
      - operation: add
        node_group: worker-nm
        size: 1
    edp_jobs_flow: hadoop_2
