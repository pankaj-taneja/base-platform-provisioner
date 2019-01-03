#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from pyhive import hive
from TCLIService.ttypes import TOperationState

DOCUMENTATION = '''
---
module: hive

short_description: Run a sql file in Hive

description:
    - "Run a sql file in Hive"

options:
    host:
        description:
            - Hive host
        required: true
    port:
        description:
            - Hive port
        required: false
    database:
        description:
            - Hive database
        required: false
    files:
        description:
            - List of files containing ';' separated sql queries
        required: true

requirements:
  - "python >= 2.7"
  - "pyhive[hive] >= 0.2.1"

author:
    - Vanessa Vuibert (@vvuibert)
'''

EXAMPLES = '''
# Test a sql file
- name: Test sql file
  hive:
    host: "data012-vip-01.devops.guavus.mtl"
    port: "10000"
    database: "carereflex"
    files: ["/opt/guavus/carereflex/srx-data/schemas/hive/test.sql"]
'''

RETURN = '''
sql_queries:
    description: List of queries that were ran
    type: list
'''


def run_module():
    module_args = dict(
        host=dict(type='str', required=True),
        port=dict(type='int', required=False, default=10000),
        database=dict(type='str', required=False, default='default'),
        files=dict(type='list', required=True)
    )

    result = dict(
        changed=False,
        sql_queries=[]
    )

    ansible_module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if ansible_module.check_mode:
        return result

    cursor = None
    try:
        cursor = hive.connect(
            host=ansible_module.params['host'],
            port=ansible_module.params['port'],
            database=ansible_module.params['database']).cursor()
        for file in ansible_module.params['files']:
            with open(file, 'r') as file_handle:
                queries = file_handle.read()
                for query in queries.split(";"):
                    clean_query = query.strip()
                    if clean_query:
                        result['sql_queries'].append(clean_query)
                        cursor.execute(clean_query)

        while cursor.poll().operationState in (
                TOperationState.INITIALIZED_STATE,
                TOperationState.RUNNING_STATE):
            time.sleep(1)

        result['changed'] = True
    except Exception as e:
        ansible_module.fail_json(msg=str(e))
    finally:
        if cursor:
            cursor.close()
    ansible_module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
