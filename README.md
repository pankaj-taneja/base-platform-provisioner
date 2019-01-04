# Decomposition Approach

## Goals
1. Flexibility to choose components stack to be installed like ELK or K8s or HWX or full stack etc.
2. Flexibility to choose installation targets nodes for each component stack.
3. Flexibility to overwrite variables default values used in desired stack.

For requirements for BPL decomposition refer [Base Platform Stack](https://guavus.atlassian.net/wiki/spaces/GA/pages/304841985/Base+Platform+Stack)

## Steps to be followed in sequence to install decomposed BPL stack
1. Install RPM package of desired stack on control machine.
2. Install ansible on contorl machine from packages comes with rpm installed in first step.
3. Choose the host machines from the available setup for desired stack components.
4. Setup the variables values for the setup in hand. 
5. Choose the desired playbooks from the available list. 
6. Execute the playbook using ansible-playbook command.

## base-platform-provisioner github repo

### Skeleton
1. This is a sample skeleton contains manifests, playbooks and inventory for ELK, redis and full stack. 
2. This repo also contains required packages and command to setup ansible on control machine.
3. This repo also contains ansible libraries and plugins to be used in different components roles.
```
# tree
.
├── ansible.cfg
├── extra_vars
│   └── all.yml
├── inventory
│   ├── group_vars
│   │   └── all
│   │       ├── common
│   │       │   └── default.yml
│   │       ├── elasticsearch_stack
│   │       │   └── default.yml
│   │       ├── redis
│   │       │   └── default.yml
│   │       └── scaffold
│   │           └── default.yml
│   └── hosts
│       ├── elasticsearch_stack
│       │   ├── es-curator-nodes
│       │   ├── es-nodes
│       │   └── kibana-nodes
│       └── redis
│           └── redis-nodes
├── library
│   ├── hdfs_file.py
│   ├── hdfs_file.pyc
│   ├── hdfs_file.pyo
│   ├── hive.py
│   ├── hive.pyc
│   ├── hive.pyo
│   ├── impala.py
│   ├── impala.pyc
│   ├── impala.pyo
│   ├── kibana_artifacts.py
│   ├── kibana_artifacts.pyc
│   ├── kibana_artifacts.pyo
│   ├── kube.py
│   ├── kube.pyc
│   ├── kube.pyo
│   ├── kube_status.py
│   ├── kube_status.pyc
│   ├── kube_status.pyo
│   ├── opennebula_vm.py
│   ├── opennebula_vm.pyc
│   ├── opennebula_vm.pyo
│   ├── postgres.py
│   ├── postgres.pyc
│   ├── postgres.pyo
│   ├── rundeck
│   │   ├── rdeck_job_import.py
│   │   ├── rdeck_job_import.pyc
│   │   ├── rdeck_job_import.pyo
│   │   ├── rdeck_project.py
│   │   ├── rdeck_project.pyc
│   │   └── rdeck_project.pyo
│   ├── zabbix_config.py
│   ├── zabbix_config.pyc
│   └── zabbix_config.pyo
├── logs
│   └── ansible.log
├── manifests
│   ├── elasticsearch_stack
│   │   ├── curator.yml
│   │   ├── elasticsearch.yml
│   │   ├── es-kibana-curator.yml
│   │   └── kibana.yml
│   ├── full_stack
│   │   └── full_stack.yml
│   ├── redis
│   │   ├── redis_stack.yml
│   │   └── redis.yml
│   └── scaffold
│       └── scaffold.yml
├── playbooks
│   ├── all
│   │   ├── curator
│   │   │   ├── deploy.yml
│   │   │   └── undeploy.yml
│   │   ├── elasticsearch
│   │   │   ├── deploy.yml
│   │   │   └── undeploy.yml
│   │   ├── kibana
│   │   │   ├── deploy.yml
│   │   │   └── undeploy.yml
│   │   ├── redis
│   │   │   ├── deploy.yml
│   │   │   └── undeploy.yml
│   │   └── scaffold
│   │       └── main.yml
│   ├── elasticsearch_stack
│   │   ├── deploy-es-kibana-curator.yml
│   │   └── undeploy-es-kibana-curator.yml
│   ├── full_stack
│   │   ├── deploy_full_stack.yml
│   │   └── undeploy_full_stack.yml
│   └── redis
│       ├── deploy-redis.yml
│       └── undeploy-redis.yml
├── plugins
│   ├── callback_plugins
│   │   ├── skippy.py
│   │   ├── skippy.pyc
│   │   └── skippy.pyo
│   └── filter_plugins
│       ├── collections.py
│       ├── collections.pyc
│       ├── collections.pyo
│       ├── custom_filters.py
│       ├── custom_filters.pyc
│       └── custom_filters.pyo
├── README.md
├── roles
└── tmp
    └── facts_cache
```

## Manifests
Manifest files are used by the ansible-galaxy cli tool to import ansible roles for a desired stack.

1. Manifests files contains github repository current stable version of a component role.
2. There is a manifest file for each ansible role (one role can have multiple role directories in it.)
3. A stack manifest stack file includes individual component manifest files which are part of that stack.

### Example (Elasticsearch Stack)
```
# cat manifests/scaffold/scaffold.yml
# Manifest file for scaffold ansible roles repos

- src: https://github.com/pankaj-taneja/ansible-role-scaffold
  version: master
  name: ansible-role-scaffold

# cat manifests/elasticsearch_stack/elasticsearch.yml
# Manifest file for elasticsearch ansible roles repos

- src: https://github.com/pankaj-taneja/ansible-role-elasticsearch
  version: master
  name: ansible-role-elasticsearch
  
# cat manifests/elasticsearch_stack/curator.yml
# Manifest file for curator ansible roles repos

- src: https://github.com/pankaj-taneja/ansible-role-elasticsearch-curator
  version: master
  name: ansible-role-elasticsearch-curator
  
# cat manifests/elasticsearch_stack/kibana.yml
# Manifest file for kibana ansible roles repos

- src: https://github.com/pankaj-taneja/ansible-role-kibana
  version: master
  name: ansible-role-kibana
 
# cat manifests/elasticsearch_stack/es-kibana-curator.yml
# This file should contain github repos versions used for elasticsearch stack

- include: manifests/scaffold/scaffold.yml

- include: manifests/elasticsearch_stack/elasticsearch.yml

- include: manifests/elasticsearch_stack/curator.yml

- include: manifests/elasticsearch_stack/kibana.yml
```
`ansible-role-scaffold` role is a common role required to be executed in each stack.
Each role break down is documented in [Roles Breakdown](https://guavus.atlassian.net/wiki/spaces/BPL/pages/289899101/Roles+Breakdown)

## Playbooks
1. Playbooks for each component deployment exists in this base-platform-provisioner repository. 
2. Playbooks of a stack includes playbooks of individual components part of that stack.

Playbook creation best practices documented in [Ansible Guideline](https://guavus.atlassian.net/wiki/spaces/BPL/pages/279117907/Ansible+Guideline)

### Example (Elasticsearch Stack)
```# cat playbooks/all/elasticsearch/deploy.yml
---

- name: Retrieve facts all host
  hosts:
    - all
  gather_facts: true
  any_errors_fatal: True
  tags:
    - 'always'
  tasks: []

- name: install es
  hosts: es-nodes
  roles:
    - ansible-role-elasticsearch

# cat playbooks/all/curator/deploy.yml
---

- name: Retrieve facts all host
  hosts:
    - all
  gather_facts: true
  any_errors_fatal: True
  tags:
    - 'always'
  tasks: []

- name: install es-curator
  hosts: es-curator-nodes
  roles:
    - ansible-role-elasticsearch-curator

# cat playbooks/elasticsearch_stack/deploy-es-kibana-curator.yml
---

- import_playbook: ../all/scaffold/main.yml

- import_playbook: ../all/elasticsearch/deploy.yml

- import_playbook: ../all/curator/deploy.yml

- import_playbook: ../all/kibana/deploy.yml

# cat playbooks/full_stack/deploy_full_stack.yml
---

- import_playbook: ../all/scaffold/main.yml

- import_playbook: ../all/elasticsearch/deploy.yml

- import_playbook: ../all/curator/deploy.yml

- import_playbook: ../all/kibana/deploy.yml

- import_playbook: ../all/redis/deploy.yml
```
`scaffold/main.yml` is a common playbook required to be executed with all stacks.

## Inventory
Inventory directory consist of hosts and group_vars directories.

### Inventory hosts
Inventory hosts contains template hosts file to different stacks.
#### Example Inventory hosts file for elasticsearch stack
```
# cat inventory/hosts/elasticsearch_stack/es-nodes
[es-nodes]
devops002-pankaj-mst-01.gvs.ggn

# cat inventory/hosts/elasticsearch_stack/es-curator-nodes
[es-curator-nodes]
devops002-pankaj-mst-01.gvs.ggn

# cat inventory/hosts/elasticsearch_stack/kibana-nodes
[kibana-nodes]
devops002-pankaj-mst-01.gvs.ggn
```
Invidual inventory hosts files to be kept for each component. 

### Inventory group_vars
Inventory group vars contains directories for individual component stacks. These directories should contain those variables which are required in multiple roles. 
#### Example Inventory group_vars for elasticsearch stack
```
# cat inventory/group_vars/all/elasticsearch_stack/default.yml
---

elasticsearch__ip: 'devops002-pankaj-mst-01.gvs.ggn'

elasticsearch__port: '9200'
```
Inventory group_vars creation best practices documented in [Ansible Guideline](https://guavus.atlassian.net/wiki/spaces/BPL/pages/279117907/Ansible+Guideline)
## Roles
## Packaging
## CI/CD
