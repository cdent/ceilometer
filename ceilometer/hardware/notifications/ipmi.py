#
# Copyright 2014 Red Hat
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
"""Converters for producing hardware sensor data sample messages from
notification events.
"""

from ceilometer.openstack.common import log
from ceilometer.openstack.common import timeutils
from ceilometer import plugin
from ceilometer import sample

LOG = log.getLogger(__name__)


class SensorNotification(plugin.NotificationBase):

    event_types = ['hardware.*']
    metric = None

    @staticmethod
    def get_targets(conf):
        return []  # Nothing for now

    def _get_sample(self, message):
        try:
            return (payload for _, payload
                    in message['payload'][self.metric].items())
        except KeyError:
            return []

    def _transform_id(self, data):
        return data

    def _transform_reading(self, data):
        return data

    def _package_payload(self, message, payload):
        info = {}
        info['publisher_id'] = message['publisher_id']
        info['resource_id'] = '%s-%s' % (message['node_uuid'],
                                         self._transform_id(
                                             payload['Sensor ID']))
        info['timestamp'] = str(timeutils.parse_strtime(
            message['timestamp'], '%Y%m%d%H%M%S'))
        info['event_type'] = 'I DO NOT KNOW'
        info['payload'] = payload
        return info

    def process_notification(self, message):
        payloads = self._get_sample(message)
        for payload in payloads:
            info = self._package_payload(message, payload)
            yield sample.Sample.from_notification(
                name='hardware.ipmi.%s' % self.metric.lower(),
                type=self.sample_type,
                unit=self._extract_unit(info['payload']['Sensor Reading']),
                volume=self._transform_reading(
                    info['payload']['Sensor Reading']),
                user_id=None,
                project_id=None,
                resource_id=info['resource_id'],
                message=info)


class TemperatureSensorNotification(SensorNotification):
    metric = 'Temperature'
    sample_type = sample.TYPE_GAUGE

    def _transform_id(self, data):
        return data.lower().replace(' ', '_')

    def _transform_reading(self, data):
        return data.split(' ', 1)[0]

    def _extract_unit(self, data):
        return data.rsplit(' ', 1)[0]
