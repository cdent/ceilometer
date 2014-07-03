#
# Copyright 2014 Red Hat, Inc
#
# Author: Chris Dent <chdent@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Tests for producing IPMI sample messages from notification events.
"""

from ceilometer.hardware.notifications import ipmi
from ceilometer.openstack.common import test
from ceilometer import sample


SENSOR_DATA = {
    'event_type': 'sensordata',
    'timestamp': '2013-12-1706: 12: 11.554607',
    'message_id:' '3eca2746-9d81-42cd-b0b3-4bdec52e109x',
    'instance_uuid': '96e11f69-f12a-485e-abfa-526cd04169c4',
    'node_uuid': '96e11f69-f12a-485e-abfa-526cd04169c4',
    'payload': {
        'Fan': {
            'FAN MOD 1A RPM (0x30)': {
                'Status': 'ok',
                'Sensor Reading': '8400 (+/- 75) RPM',
                'Entity ID': '7.1 (System Board)',
                'Normal Minimum': '10425.000',
                'Positive Hysteresis': '375.000',
                'Normal Maximum': '14775.000',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '4275.000',
                'Negative Hysteresis': '375.000',
                'Sensor ID': 'FAN MOD 1A RPM (0x30)',
                'Nominal Reading': '5325.000'
            },
            'FAN MOD 1B RPM (0x31)': {
                'Status': 'ok',
                'Sensor Reading': '8550 (+/- 75) RPM',
                'Entity ID': '7.1 (System Board)',
                'Normal Minimum': '10425.000',
                'Positive Hysteresis': '375.000',
                'Normal Maximum': '14775.000',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '4275.000',
                'Negative Hysteresis': '375.000',
                'Sensor ID': 'FAN MOD 1B RPM (0x31)',
                'Nominal Reading': '7800.000'
            }
        },
        'Temperature': {
            'Temp (0x1)': {
                'Status': 'ok',
                'Sensor Reading': '-58 (+/- 1) degrees C',
                'Entity ID': '3.1 (Processor)',
                'Normal Minimum': '11.000',
                'Positive Hysteresis': '1.000',
                'Upper non-critical': '85.000',
                'Normal Maximum': '69.000',
                'Sensor Type (Analog)': 'Temperature',
                'Negative Hysteresis': '1.000',
                'Upper critical': '90.000',
                'Sensor ID': 'Temp (0x1)',
                'Nominal Reading': '50.000'
            },
            'Temp (0x2)': {
                'Status': 'ok',
                'Sensor Reading': '50 (+/- 1) degrees C',
                'Entity ID': '3.2 (Processor)',
                'Normal Minimum': '11.000',
                'Positive Hysteresis': '1.000',
                'Upper non-critical': '85.000',
                'Normal Maximum': '69.000',
                'Sensor Type (Analog)': 'Temperature',
                'Negative Hysteresis': '1.000',
                'Upper critical': '90.000',
                'Sensor ID': 'Temp (0x2)',
                'Nominal Reading': '50.000'
            },
        },
    },
}

# XXX nothing past here

class TestNotifications(test.BaseTestCase):

    def test_process_notification(self):
        info = list(instance.Instance(None).process_notification(
            INSTANCE_CREATE_END
        ))[0]
        for name, actual, expected in [
                ('counter_name', info.name, 'instance'),
                ('counter_type', info.type, sample.TYPE_GAUGE),
                ('counter_volume', info.volume, 1),
                ('timestamp', info.timestamp,
                 INSTANCE_CREATE_END['timestamp']),
                ('resource_id', info.resource_id,
                 INSTANCE_CREATE_END['payload']['instance_id']),
                ('instance_type_id',
                 info.resource_metadata['instance_type_id'],
                 INSTANCE_CREATE_END['payload']['instance_type_id']),
                ('host', info.resource_metadata['host'],
                 INSTANCE_CREATE_END['publisher_id']),
        ]:
            self.assertEqual(expected, actual, name)

    @staticmethod
    def _find_counter(counters, name):
        return filter(lambda counter: counter.name == name, counters)[0]

    def _verify_user_metadata(self, metadata):
        self.assertIn('user_metadata', metadata)
        user_meta = metadata['user_metadata']
        self.assertEqual(user_meta.get('server_group'), 'Group_A')
        self.assertNotIn('AutoScalingGroupName', user_meta)
        self.assertIn('foo_bar', user_meta)
        self.assertNotIn('foo.bar', user_meta)

    def test_instance_create_instance(self):
        ic = instance.Instance(None)
        counters = list(ic.process_notification(INSTANCE_CREATE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_instance_create_flavor(self):
        ic = instance.InstanceFlavor(None)
        counters = list(ic.process_notification(INSTANCE_CREATE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_instance_create_memory(self):
        ic = instance.Memory(None)
        counters = list(ic.process_notification(INSTANCE_CREATE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(INSTANCE_CREATE_END['payload']['memory_mb'], c.volume)

    def test_instance_create_vcpus(self):
        ic = instance.VCpus(None)
        counters = list(ic.process_notification(INSTANCE_CREATE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(INSTANCE_CREATE_END['payload']['vcpus'], c.volume)

    def test_instance_create_root_disk_size(self):
        ic = instance.RootDiskSize(None)
        counters = list(ic.process_notification(INSTANCE_CREATE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(INSTANCE_CREATE_END['payload']['root_gb'], c.volume)

    def test_instance_create_ephemeral_disk_size(self):
        ic = instance.EphemeralDiskSize(None)
        counters = list(ic.process_notification(INSTANCE_CREATE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(INSTANCE_CREATE_END['payload']['ephemeral_gb'],
                         c.volume)

    def test_instance_exists_instance(self):
        ic = instance.Instance(None)
        counters = list(ic.process_notification(INSTANCE_EXISTS))
        self.assertEqual(1, len(counters))

    def test_instance_exists_metadata_list(self):
        ic = instance.Instance(None)
        counters = list(ic.process_notification(INSTANCE_EXISTS_METADATA_LIST))
        self.assertEqual(1, len(counters))

    def test_instance_exists_flavor(self):
        ic = instance.Instance(None)
        counters = list(ic.process_notification(INSTANCE_EXISTS))
        self.assertEqual(1, len(counters))

    def test_instance_delete_instance(self):
        ic = instance.Instance(None)
        counters = list(ic.process_notification(INSTANCE_DELETE_START))
        self.assertEqual(1, len(counters))

    def test_instance_delete_flavor(self):
        ic = instance.Instance(None)
        counters = list(ic.process_notification(INSTANCE_DELETE_START))
        self.assertEqual(1, len(counters))

    def test_instance_finish_resize_instance(self):
        ic = instance.Instance(None)
        counters = list(ic.process_notification(INSTANCE_FINISH_RESIZE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_finish_resize_flavor(self):
        ic = instance.InstanceFlavor(None)
        counters = list(ic.process_notification(INSTANCE_FINISH_RESIZE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)
        self.assertEqual('instance:m1.small', c.name)
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_finish_resize_memory(self):
        ic = instance.Memory(None)
        counters = list(ic.process_notification(INSTANCE_FINISH_RESIZE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(INSTANCE_FINISH_RESIZE_END['payload']['memory_mb'],
                         c.volume)
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_finish_resize_vcpus(self):
        ic = instance.VCpus(None)
        counters = list(ic.process_notification(INSTANCE_FINISH_RESIZE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(INSTANCE_FINISH_RESIZE_END['payload']['vcpus'],
                         c.volume)
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_resize_finish_instance(self):
        ic = instance.Instance(None)
        counters = list(ic.process_notification(INSTANCE_FINISH_RESIZE_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_resize_finish_flavor(self):
        ic = instance.InstanceFlavor(None)
        counters = list(ic.process_notification(INSTANCE_RESIZE_REVERT_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)
        self.assertEqual('instance:m1.tiny', c.name)
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_resize_finish_memory(self):
        ic = instance.Memory(None)
        counters = list(ic.process_notification(INSTANCE_RESIZE_REVERT_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(INSTANCE_RESIZE_REVERT_END['payload']['memory_mb'],
                         c.volume)
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_resize_finish_vcpus(self):
        ic = instance.VCpus(None)
        counters = list(ic.process_notification(INSTANCE_RESIZE_REVERT_END))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(INSTANCE_RESIZE_REVERT_END['payload']['vcpus'],
                         c.volume)
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_delete_samples(self):
        ic = instance.InstanceDelete(None)
        counters = list(ic.process_notification(INSTANCE_DELETE_SAMPLES))
        self.assertEqual(2, len(counters))
        names = [c.name for c in counters]
        self.assertEqual(['sample-name1', 'sample-name2'], names)
        c = counters[0]
        self._verify_user_metadata(c.resource_metadata)

    def test_instance_scheduled(self):
        ic = instance.InstanceScheduled(None)

        self.assertIn(INSTANCE_SCHEDULED['event_type'],
                      ic.event_types)

        counters = list(ic.process_notification(INSTANCE_SCHEDULED))
        self.assertEqual(1, len(counters))
        names = [c.name for c in counters]
        self.assertEqual(['instance.scheduled'], names)
        rid = [c.resource_id for c in counters]
        self.assertEqual(['fake-uuid1-1'], rid)
