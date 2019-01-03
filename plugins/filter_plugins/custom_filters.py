#!/usr/bin/python
import pendulum
import socket
import json
import requests

def gethostbyaddr(name, return_info):
    """
    Return tuple like whith fqdn, first ip
    :param name: should be the ip or fqdn
    :param return_info: nature of the info we want "ip" or "fqdn"
    """
    res = socket.gethostbyaddr(name)
    print res
    if return_info == "fqdn":
        return res[0]
    if return_info == "ip":
        return res[2][0]
    
def zabbix_get_id(groups, ids, id_string):
    """
    Return all ids values where ids key name matches the group name
    :param groups: sanitized list of names where key matches in ids
    :param ids: simple list of ids for lookups
    :param id_string: name of the id (ex: groupid or templateid) for zabbix api
    """
    return [{id_string: ids[group]} for group in groups]


def to_host_list(host_list, port, protocol=None):
    """
    List of host/port pairs
    :param host_list: array of hosts
    :param port: string
    :param protocol: e.g. thrift
    :return:
    """
    if protocol:
        new_list = [protocol + '://' + host + ':' + port for host in host_list]
    else:
        new_list = [host + ':' + port for host in host_list]

    return ",".join(new_list)


def to_quoted_host_list(host_list, port, protocol=None):
    """
    List of host/port pairs
    :param host_list: array of hosts
    :param port: string
    :param protocol: e.g. thrift
    :return:
    """
    if protocol:
        new_list = ['"' + protocol + '://' + host + ':' + port + '"' for host in host_list]
    else:
        new_list = ['"' + host + ':' + port + '"' for host in host_list]

    return ",".join(new_list)


def add_days(date_time, days):
    """
    :param date_time:
    :param days:
    :return:
    """
    return pendulum.instance(date_time).add(days=days)


def subtract_days(date_time, days):
    """
    :param date_time:
    :param days:
    :return:
    """
    return pendulum.instance(date_time).subtract(days=days)


def string_to_datetime(date_time):
    """
    :param date_time:
    :return:
    """
    return pendulum.parse(date_time)


def to_bash_list(item_list):
    """
    :param item_list:
    :return:
    """
    return " ".join("'" + item + "'" for item in item_list)


def format_string_datetime(date_time, date_format):
    """
    :param date_time:
    :param date_format:
    :return:
    """
    date_time = string_to_datetime(date_time)
    return date_time.format(date_format)


def format_datetime(date_time, date_format):
    """
    :param date_time:
    :param date_format:
    :return:
    """
    return date_time.format(date_format)


def get_month_partitions(str_start_date, str_end_date):
    """
    :param str_start_date:
    :param str_end_date:
    :return:
    """
    partitions = []
    start_date = pendulum.parse(str_start_date)
    months = (pendulum.parse(str_end_date) - start_date).months
    for month in range(0, months):
        partitions.append(start_date.add(months=month).format("/year=%Y/month=%-m"))

    return partitions


def get_day_partitions(str_start_date, str_end_date):
    """
    :param str_start_date:
    :param str_end_date:
    :return:
    """
    partitions = []
    start_date = pendulum.parse(str_start_date)
    days = (pendulum.parse(str_end_date) - start_date).days
    for day in range(0, days):
        partitions.append(start_date.add(days=day).format("/year=%Y/month=%-m/day=%-d"))

    return partitions


def status_list_equal_to(status_list, string_match):
    for status in status_list:
        if status != string_match:
            return False
    return True


def add_minutes(date_time, minutes):
    """
    :param date_time:
    :param minutes:
    :return:
    """
    return pendulum.instance(date_time).add(minutes=minutes)


def from_timestamp(timestamp):
    """
    :param timestamp:
    :return:
    """
    return pendulum.from_timestamp(timestamp)

def get_active_namenode(host_list):
    """
    :param host_list
    :return:
    """
    for host in host_list:
        url = "http://%s:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus" % (host)
        r = requests.get(url)
        if json.loads(r.text)['beans'][0]['State'] == 'active':
            return host

def get_active_resourcemanager(host_list):
    """
    :param host_list
    :return:
    """
    for host in host_list:
        url = "http://%s:8088/ws/v1/cluster/info" % (host)
        r = requests.get(url)
        if json.loads(r.text)['clusterInfo']['haState'] == 'ACTIVE':
            return host


class FilterModule(object):
    """
    custom Jinja2 filters
    """

    def filters(self):
        return {
            'gethostbyaddr': gethostbyaddr,
            'to_host_list': to_host_list,
            'to_quoted_host_list': to_quoted_host_list,
            'zabbix_get_id': zabbix_get_id,
            'add_days': add_days,
            'subtract_days': subtract_days,
            'string_to_datetime': string_to_datetime,
            'to_bash_list': to_bash_list,
            'format_string_datetime': format_string_datetime,
            'format_datetime': format_datetime,
            'get_month_partitions': get_month_partitions,
            'get_day_partitions': get_day_partitions,
            'status_list_equal_to': status_list_equal_to,
            'add_minutes': add_minutes,
            'from_timestamp': from_timestamp,
            'get_active_namenode': get_active_namenode,
            'get_active_resourcemanager': get_active_resourcemanager
        }
