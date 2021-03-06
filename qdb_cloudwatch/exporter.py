# -*- coding: utf-8 -*-

import argparse
import quasardb
import boto3
import requests

from functools import reduce
from .metrics import key_to_metric
from .metrics import MetricType

def get_args():
    parser = argparse.ArgumentParser(
        description=(
            'Fetch QuasarDB metrics for local node and export to CloudWatch.'))
    parser.add_argument(
        '--cluster',
        dest='cluster_uri',
        help='QuasarDB cluster uri to connect to. Defaults to qdb://127.0.0.1:2836',
        default="qdb://127.0.0.1:2836")

    parser.add_argument(
        '--node-id',
        dest='node_id',
        help='Node id to collect metrics from, e.g. 0-0-0-1')

    parser.add_argument(
        '--namespace',
        dest='namespace',
        help='Cloudwatch namespace for metrics. Defaults to \'QuasarDB\'',
        default="QuasarDB")

    parser.add_argument(
        '--instance-id',
        dest='instance_id',
        help='EC2 instance id to add to the dimensions. By default tries to look up from AWS instance metadata.')

    parser.add_argument(
        '--region',
        dest='region_name',
        help='AWS region to export metrics in. Defaults to $AWS_DEFAULT_REGION.')

    return parser.parse_args()

def get_qdb_conn(uri):
    return quasardb.Cluster(uri)

def get_boto_client(region_name=None):
    if region_name is not None:
        return boto3.client('cloudwatch', region_name=region_name)
    else:
        return boto3.client('cloudwatch')

def parse_key(key):
    return key.split('.', 3)[-1]

def collect_keys(conn, node_id):
    return conn.prefix_get(str('$qdb.statistics.' + node_id), 200)

def collect_metric(conn, metric_type, key):

    if metric_type is None:
        return None

    fn = metric_type.lookup_fn(conn)
    return fn(key).get()

def collect_metrics(conn, keys):
    res = dict()

    for key in keys:
        # $qdb.statistics.<node_id>.foo.bar -> foo.bar
        parsed = parse_key(key)
        metric = key_to_metric(parsed)

        if metric is not None and metric['type'].value is not MetricType.STRING.value:
            val = collect_metric(conn, metric['type'], key)
            if 'parser' in metric:
                val = metric['parser'](val)

            metric['value'] = val

            res[parsed] = metric

    return res

def _chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]

def put_metrics(client, namespace, metrics, instance_id=None):

    dimensions = []
    if instance_id is not None:
        dimensions.append({'Name': 'InstanceId',
                           'Value': instance_id})

    xs = []
    for k in metrics:
        v = metrics[k]

        xs.append({'Dimensions': dimensions,
                   'MetricName': k,
                   'Value': v['value'],
                   'Unit': v['unit']})

    # create chunks of at most 20 metrics
    results = list()
    for chunk in _chunks(xs, 20):
        results.append(client.put_metric_data(Namespace=namespace,
                                              MetricData=chunk))

    return results

def main():
    args = get_args()

    conn = get_qdb_conn(args.cluster_uri)
    keys = collect_keys(conn, args.node_id)
    metrics = collect_metrics(conn, keys)

    result = put_metrics(get_boto_client(args.region_name), args.namespace, metrics, args.instance_id)

    print("result = ", result)
