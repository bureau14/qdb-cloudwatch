
from functools import partial
from enum import Enum

def nanos_to_micros(x):
    return x / 1000

class MetricType(Enum):
    COUNTER = 1
    GAUGE = 2
    STRING = 3

    def lookup_fn(self, conn):
        if self.value is self.COUNTER.value or self.value is self.GAUGE.value:
            return conn.integer
        elif self.value is self.STRING.value:
            return conn.blob
        else:
            raise RuntimeError("Invalid value: ", str(self))

METRICS = {'cpu.idle': {'type': MetricType.COUNTER,
                        'unit': 'Microseconds',
                        'parser': nanos_to_micros},
           'cpu.system': {'type': MetricType.COUNTER,
                          'unit': 'Microseconds',
                          'parser': nanos_to_micros},
           'cpu.user': {'type': MetricType.COUNTER,
                        'unit': 'Microseconds',
                        'parser': nanos_to_micros},
           'disk.bytes_free': {'type': MetricType.GAUGE,
                               'unit': 'Bytes'},
           'disk.bytes_total': {'type': MetricType.GAUGE,
                                'unit': 'Bytes'},
           'disk.path': {'type': MetricType.STRING,
                         'unit': None},
           'engine_build_date': {'type': MetricType.STRING,
                                 'unit': None},
           'engine_version': {'type': MetricType.STRING,
                              'unit': None},
           'hardware_concurrency': {'type': MetricType.GAUGE,
                                    'unit': 'Count'},
           'memory.bytes_resident_size': {'type': MetricType.GAUGE,
                                          'unit': 'Bytes'},
           'memory.physmem.bytes_total': {'type': MetricType.GAUGE,
                                          'unit': 'Bytes'},
           'memory.physmem.bytes_used': {'type': MetricType.GAUGE,
                                         'unit': 'Bytes'},
           'memory.resident_count': {'type': MetricType.GAUGE,
                                     'unit': 'Count'},
           'memory.vm.bytes_total': {'type': MetricType.GAUGE,
                                     'unit': 'Bytes'},
           'memory.vm.bytes_used': {'type': MetricType.GAUGE,
                                    'unit': 'Bytes'},
           'network.current_users_count': {'type': MetricType.GAUGE,
                                           'unit': 'Count'},
           'network.sessions.available_count': {'type': MetricType.GAUGE,
                                                'unit': 'Count'},
           'network.sessions.max_count': {'type': MetricType.GAUGE,
                                          'unit': 'Count'},
           'network.sessions.unavailable_count': {'type': MetricType.GAUGE,
                                                  'unit': 'Count'},
           'node_id': {'type': MetricType.STRING,
                       'unit': None},
           'operating_system': {'type': MetricType.STRING,
                                'unit': None},
           'partitions_count': {'type': MetricType.GAUGE,
                                'unit': 'Count'},
           'perf.blob.update.content_writing.total_ns': {'type': MetricType.COUNTER,
                                                         'unit': 'Microseconds',
                                                         'parser': nanos_to_micros},
           'perf.blob.update.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                         'unit': 'Microseconds',
                                                         'parser': nanos_to_micros},
           'perf.blob.update.entry_trimming.total_ns': {'type': MetricType.COUNTER,
                                                        'unit': 'Microseconds',
                                                        'parser': nanos_to_micros},
           'perf.blob.update.entry_writing.total_ns': {'type': MetricType.COUNTER,
                                                       'unit': 'Microseconds',
                                                       'parser': nanos_to_micros},
           'perf.blob.update.processing.total_ns': {'type': MetricType.COUNTER,
                                                    'unit': 'Microseconds',
                                                    'parser': nanos_to_micros},
           'perf.common.get.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                        'unit': 'Microseconds',
                                                        'parser': nanos_to_micros},
           'perf.common.get.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                        'unit': 'Microseconds',
                                                        'parser': nanos_to_micros},
           'perf.common.get.processing.total_ns': {'type': MetricType.COUNTER,
                                                   'unit': 'Microseconds',
                                                   'parser': nanos_to_micros},
           'perf.common.get_by_affix.affix_search.total_ns': {'type': MetricType.COUNTER,
                                                              'unit': 'Microseconds',
                                                              'parser': nanos_to_micros},
           'perf.common.get_by_affix.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                                 'unit': 'Microseconds',
                                                                 'parser': nanos_to_micros},
           'perf.common.get_by_affix.processing.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.common.get_metadata.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                                 'unit': 'Microseconds',
                                                                 'parser': nanos_to_micros},
           'perf.common.get_metadata.processing.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.common.get_range.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                              'unit': 'Microseconds',
                                                              'parser': nanos_to_micros},
           'perf.common.get_range.processing.total_ns': {'type': MetricType.COUNTER,
                                                         'unit': 'Microseconds',
                                                         'parser': nanos_to_micros},
           'perf.common.get_versions.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                                 'unit': 'Microseconds',
                                                                 'parser': nanos_to_micros},
           'perf.common.get_versions.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                                 'unit': 'Microseconds',
                                                                 'parser': nanos_to_micros},
           'perf.common.get_versions.processing.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.common.set_transaction_state.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                                          'unit': 'Microseconds',
                                                                          'parser': nanos_to_micros},
           'perf.common.set_transaction_state.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                                          'unit': 'Microseconds',
                                                                          'parser': nanos_to_micros},
           'perf.common.set_transaction_state.entry_trimming.total_ns': {'type': MetricType.COUNTER,
                                                                         'unit': 'Microseconds',
                                                                         'parser': nanos_to_micros},
           'perf.common.set_transaction_state.entry_writing.total_ns': {'type': MetricType.COUNTER,
                                                                        'unit': 'Microseconds',
                                                                        'parser': nanos_to_micros},
           'perf.common.set_transaction_state.processing.total_ns': {'type': MetricType.COUNTER,
                                                                     'unit': 'Microseconds',
                                                                     'parser': nanos_to_micros},
           'perf.control.system.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.control.system.processing.total_ns': {'type': MetricType.COUNTER,
                                                       'unit': 'Microseconds',
                                                       'parser': nanos_to_micros},
           'perf.control.status.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.control.status.processing.total_ns': {'type': MetricType.COUNTER,
                                                       'unit': 'Microseconds',
                                                       'parser': nanos_to_micros},
           'perf.integer.update.content_writing.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.integer.update.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.integer.update.entry_trimming.total_ns': {'type': MetricType.COUNTER,
                                                           'unit': 'Microseconds',
                                                           'parser': nanos_to_micros},
           'perf.integer.update.entry_writing.total_ns': {'type': MetricType.COUNTER,
                                                          'unit': 'Microseconds',
                                                          'parser': nanos_to_micros},
           'perf.integer.update.processing.total_ns': {'type': MetricType.COUNTER,
                                                       'unit': 'Microseconds',
                                                       'parser': nanos_to_micros},
           'perf.placeholder.put.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                             'unit': 'Microseconds',
                                                             'parser': nanos_to_micros},
           'perf.placeholder.put.entry_writing.total_ns': {'type': MetricType.COUNTER,
                                                           'unit': 'Microseconds',
                                                           'parser': nanos_to_micros},
           'perf.placeholder.put.processing.total_ns': {'type': MetricType.COUNTER,
                                                        'unit': 'Microseconds',
                                                        'parser': nanos_to_micros},
           'perf.tag.leaf_insert.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                             'unit': 'Microseconds',
                                                             'parser': nanos_to_micros},
           'perf.tag.leaf_insert.entry_writing.total_ns': {'type': MetricType.COUNTER,
                                                           'unit': 'Microseconds',
                                                           'parser': nanos_to_micros},
           'perf.tag.leaf_insert.processing.total_ns': {'type': MetricType.COUNTER,
                                                        'unit': 'Microseconds',
                                                        'parser': nanos_to_micros},
           'perf.ts.aggregate_table.affix_search.total_ns': {'type': MetricType.COUNTER,
                                                             'unit': 'Microseconds',
                                                             'parser': nanos_to_micros},
           'perf.ts.aggregate_table.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                                'unit': 'Microseconds',
                                                                'parser': nanos_to_micros},
           'perf.ts.aggregate_table.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                                'unit': 'Microseconds',
                                                                'parser': nanos_to_micros},
           'perf.ts.aggregate_table.directory_reading.total_ns': {'type': MetricType.COUNTER,
                                                                  'unit': 'Microseconds',
                                                                  'parser': nanos_to_micros},
           'perf.ts.aggregate_table.processing.total_ns': {'type': MetricType.COUNTER,
                                                           'unit': 'Microseconds',
                                                           'parser': nanos_to_micros},
           'perf.ts.aggregate_table.serialization.total_ns': {'type': MetricType.COUNTER,
                                                              'unit': 'Microseconds',
                                                              'parser': nanos_to_micros},
           'perf.ts.blob_insert.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.blob_insert.content_writing.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.blob_insert.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.blob_insert.directory_writing.total_ns': {'type': MetricType.COUNTER,
                                                              'unit': 'Microseconds',
                                                              'parser': nanos_to_micros},
           'perf.ts.blob_insert.entry_trimming.total_ns': {'type': MetricType.COUNTER,
                                                           'unit': 'Microseconds',
                                                           'parser': nanos_to_micros},
           'perf.ts.blob_insert.entry_writing.total_ns': {'type': MetricType.COUNTER,
                                                          'unit': 'Microseconds',
                                                          'parser': nanos_to_micros},
           'perf.ts.blob_insert.processing.total_ns': {'type': MetricType.COUNTER,
                                                       'unit': 'Microseconds',
                                                       'parser': nanos_to_micros},
           'perf.ts.blob_insert.ts_bucket_updating.total_ns': {'type': MetricType.COUNTER,
                                                               'unit': 'Microseconds',
                                                               'parser': nanos_to_micros},
           'perf.ts.create_root.content_writing.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.create_root.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.create_root.entry_writing.total_ns': {'type': MetricType.COUNTER,
                                                          'unit': 'Microseconds',
                                                          'parser': nanos_to_micros},
           'perf.ts.create_root.processing.total_ns': {'type': MetricType.COUNTER,
                                                       'unit': 'Microseconds',
                                                       'parser': nanos_to_micros},
           'perf.ts.double_aggregate.affix_search.total_ns': {'type': MetricType.COUNTER,
                                                              'unit': 'Microseconds',
                                                              'parser': nanos_to_micros},
           'perf.ts.double_aggregate.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                                 'unit': 'Microseconds',
                                                                 'parser': nanos_to_micros},
           'perf.ts.double_aggregate.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                                 'unit': 'Microseconds',
                                                                 'parser': nanos_to_micros},
           'perf.ts.double_aggregate.directory_reading.total_ns': {'type': MetricType.COUNTER,
                                                                   'unit': 'Microseconds',
                                                                   'parser': nanos_to_micros},
           'perf.ts.double_aggregate.processing.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.double_aggregate.serialization.total_ns': {'type': MetricType.COUNTER,
                                                               'unit': 'Microseconds',
                                                               'parser': nanos_to_micros},
           'perf.ts.get_column_info.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                                'unit': 'Microseconds',
                                                                'parser': nanos_to_micros},
           'perf.ts.get_column_info.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                                'unit': 'Microseconds',
                                                                'parser': nanos_to_micros},
           'perf.ts.get_column_info.processing.total_ns': {'type': MetricType.COUNTER,
                                                           'unit': 'Microseconds',
                                                           'parser': nanos_to_micros},
           'perf.ts.get_columns.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.get_columns.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.get_columns.processing.total_ns': {'type': MetricType.COUNTER,
                                                       'unit': 'Microseconds',
                                                       'parser': nanos_to_micros},
           'perf.ts.get_range.affix_search.total_ns': {'type': MetricType.COUNTER,
                                                       'unit': 'Microseconds',
                                                       'parser': nanos_to_micros},
           'perf.ts.get_range.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                          'unit': 'Microseconds',
                                                          'parser': nanos_to_micros},
           'perf.ts.get_range.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                          'unit': 'Microseconds',
                                                          'parser': nanos_to_micros},
           'perf.ts.get_range.directory_reading.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.get_range.processing.total_ns': {'type': MetricType.COUNTER,
                                                     'unit': 'Microseconds',
                                                     'parser': nanos_to_micros},
           'perf.ts.get_range.serialization.total_ns': {'type': MetricType.COUNTER,
                                                        'unit': 'Microseconds',
                                                        'parser': nanos_to_micros},
           'perf.ts.int64_aggregate.affix_search.total_ns': {'type': MetricType.COUNTER,
                                                             'unit': 'Microseconds',
                                                             'parser': nanos_to_micros},
           'perf.ts.int64_aggregate.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                                'unit': 'Microseconds',
                                                                'parser': nanos_to_micros},
           'perf.ts.int64_aggregate.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                                'unit': 'Microseconds',
                                                                'parser': nanos_to_micros},
           'perf.ts.int64_aggregate.directory_reading.total_ns': {'type': MetricType.COUNTER,
                                                                  'unit': 'Microseconds',
                                                                  'parser': nanos_to_micros},
           'perf.ts.int64_aggregate.processing.total_ns': {'type': MetricType.COUNTER,
                                                           'unit': 'Microseconds',
                                                           'parser': nanos_to_micros},
           'perf.ts.int64_aggregate.serialization.total_ns': {'type': MetricType.COUNTER,
                                                              'unit': 'Microseconds',
                                                              'parser': nanos_to_micros},
           'perf.ts.table_insert.content_reading.total_ns': {'type': MetricType.COUNTER,
                                                             'unit': 'Microseconds',
                                                             'parser': nanos_to_micros},
           'perf.ts.table_insert.content_writing.total_ns': {'type': MetricType.COUNTER,
                                                             'unit': 'Microseconds',
                                                             'parser': nanos_to_micros},
           'perf.ts.table_insert.deserialization.total_ns': {'type': MetricType.COUNTER,
                                                             'unit': 'Microseconds',
                                                             'parser': nanos_to_micros},
           'perf.ts.table_insert.directory_writing.total_ns': {'type': MetricType.COUNTER,
                                                               'unit': 'Microseconds',
                                                               'parser': nanos_to_micros},
           'perf.ts.table_insert.entry_trimming.total_ns': {'type': MetricType.COUNTER,
                                                            'unit': 'Microseconds',
                                                            'parser': nanos_to_micros},
           'perf.ts.table_insert.entry_writing.total_ns': {'type': MetricType.COUNTER,
                                                           'unit': 'Microseconds',
                                                           'parser': nanos_to_micros},
           'perf.ts.table_insert.processing.total_ns': {'type': MetricType.COUNTER,
                                                        'unit': 'Microseconds',
                                                        'parser': nanos_to_micros},
           'persistence.bytes_capacity': {'type': MetricType.GAUGE,
                                          'unit': 'Bytes'},
           'persistence.bytes_read': {'type': MetricType.COUNTER,
                                      'unit': 'Bytes'},
           'persistence.bytes_utilized': {'type': MetricType.GAUGE,
                                          'unit': 'Bytes'},
           'persistence.bytes_written': {'type': MetricType.COUNTER,
                                         'unit': 'Bytes'},
           'persistence.entries_count': {'type': MetricType.GAUGE,
                                         'unit': 'Count'},
           'requests.bytes_out': {'type': MetricType.COUNTER,
                                  'unit': 'Bytes'},
           'requests.errors_count': {'type': MetricType.COUNTER,
                                     'unit': 'Count'},
           'requests.successes_count': {'type': MetricType.COUNTER,
                                        'unit': 'Count'},
           'requests.total_count': {'type': MetricType.COUNTER,
                                    'unit': 'Count'},
           'startup': {'type': MetricType.COUNTER,
                       'unit': 'None'}}

def key_to_metric(x):
    try:
        return METRICS[x]
    except KeyError:
        print("unrecognized key: ", x)
