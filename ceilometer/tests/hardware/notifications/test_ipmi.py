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
    'instance_uuid': 'f11251ax-c568-25ca-4582-0x27add644c6',
    'timestamp': '20140223134852',
    'node_uuid': 'f4982fd2-2f2b-4bb5-9aff-48aac801d1ad',
    'message_id': 'f22188ca-c068-47ce-a3e5-0e27ffe234c6',
    'publisher_id': 'f23188ca-c068-47ce-a3e5-0e27ffe234c6',
    'payload': {
        'Temperature': {
            'DIMM GH VR Temp (0x3b)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '26 (+/- 0.500) degrees C',
                'Entity ID': '20.6 (Power Module)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '95.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '105.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '100.000',
                'Sensor ID': 'DIMM GH VR Temp (0x3b)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
            'CPU1 VR Temp (0x36)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '32 (+/- 0.500) degrees C',
                'Entity ID': '20.1 (Power Module)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '95.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '105.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '100.000',
                'Sensor ID': 'CPU1 VR Temp (0x36)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
            'DIMM EF VR Temp (0x3a)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '26 (+/- 0.500) degrees C',
                'Entity ID': '20.5 (Power Module)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '95.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '105.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '100.000',
                'Sensor ID': 'DIMM EF VR Temp (0x3a)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
            'CPU2 VR Temp (0x37)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '31 (+/- 0.500) degrees C',
                'Entity ID': '20.2 (Power Module)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '95.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '105.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '100.000',
                'Sensor ID': 'CPU2 VR Temp (0x37)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
            'Ambient Temp (0x32)': {
                'Status': 'ok',
                'Sensor Reading': '25 (+/- 0) degrees C',
                'Entity ID': '12.1 (Front Panel Board)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Event Message Control': 'Per-threshold',
                'Assertion Events': '',
                'Upper non-critical': '43.000',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Upper non-recoverable': '50.000',
                'Positive Hysteresis': '4.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '46.000',
                'Sensor ID': 'Ambient Temp (0x32)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '25.000'
            },
            'Mezz Card Temp (0x35)': {
                'Status': 'Disabled',
                'Sensor Reading': 'Disabled',
                'Entity ID': '44.1 (I/O Module)',
                'Event Message Control': 'Per-threshold',
                'Upper non-critical': '70.000',
                'Upper non-recoverable': '85.000',
                'Positive Hysteresis': '4.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '80.000',
                'Sensor ID': 'Mezz Card Temp (0x35)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '25.000'
            },
            'PCH Temp (0x3c)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '46 (+/- 0.500) degrees C',
                'Entity ID': '45.1 (Processor/IO Module)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '93.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '103.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '98.000',
                'Sensor ID': 'PCH Temp (0x3c)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
            'DIMM CD VR Temp (0x39)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '27 (+/- 0.500) degrees C',
                'Entity ID': '20.4 (Power Module)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '95.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '105.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '100.000',
                'Sensor ID': 'DIMM CD VR Temp (0x39)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
            'PCI Riser 2 Temp (0x34)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '30 (+/- 0) degrees C',
                'Entity ID': '16.2 (System Internal Expansion Board)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '70.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '85.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '80.000',
                'Sensor ID': 'PCI Riser 2 Temp (0x34)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
            'DIMM AB VR Temp (0x38)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '28 (+/- 0.500) degrees C',
                'Entity ID': '20.3 (Power Module)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '95.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '105.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '100.000',
                'Sensor ID': 'DIMM AB VR Temp (0x38)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
            'PCI Riser 1 Temp (0x33)': {
                'Status': 'ok',
                'Deassertions Enabled': 'unc+ ucr+ unr+',
                'Sensor Reading': '38 (+/- 0) degrees C',
                'Entity ID': '16.1 (System Internal Expansion Board)',
                'Assertions Enabled': 'unc+ ucr+ unr+',
                'Positive Hysteresis': '4.000',
                'Assertion Events': '',
                'Upper non-critical': '70.000',
                'Event Message Control': 'Per-threshold',
                'Upper non-recoverable': '85.000',
                'Normal Maximum': '112.000',
                'Maximum sensor range': 'Unspecified',
                'Sensor Type (Analog)': 'Temperature',
                'Readable Thresholds': 'unc ucr unr',
                'Negative Hysteresis': 'Unspecified',
                'Threshold Read Mask': 'unc ucr unr',
                'Upper critical': '80.000',
                'Sensor ID': 'PCI Riser 1 Temp (0x33)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '16.000'
            },
        },
        'Current': {
            'Avg Power (0x2e)': {
                'Status': 'ok',
                'Sensor Reading': '130 (+/- 0) Watts',
                'Entity ID': '21.0 (Power Management)',
                'Assertions Enabled': '',
                'Event Message Control': 'Per-threshold',
                'Readable Thresholds': 'No Thresholds',
                'Positive Hysteresis': 'Unspecified',
                'Sensor Type (Analog)': 'Current',
                'Negative Hysteresis': 'Unspecified',
                'Maximum sensor range': 'Unspecified',
                'Sensor ID': 'Avg Power (0x2e)',
                'Assertion Events': '',
                'Minimum sensor range': '2550.000',
                'Settable Thresholds': 'No Thresholds'
            }
        },
        'Fan': {
            'Fan 4A Tach (0x46)': {
                'Status': 'ok',
                'Sensor Reading': '6900 (+/- 0) RPM',
                'Entity ID': '29.4 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2580.000',
                'Positive Hysteresis': '120.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '15300.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '120.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 4A Tach (0x46)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '4020.000'
            },
            'Fan 5A Tach (0x48)': {
                'Status': 'ok',
                'Sensor Reading': '7140 (+/- 0) RPM',
                'Entity ID': '29.5 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2580.000',
                'Positive Hysteresis': '120.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '15300.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '120.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 5A Tach (0x48)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '4020.000'
            },
            'Fan 3A Tach (0x44)': {
                'Status': 'ok',
                'Sensor Reading': '6900 (+/- 0) RPM',
                'Entity ID': '29.3 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2580.000',
                'Positive Hysteresis': '120.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '15300.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '120.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 3A Tach (0x44)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '4020.000'
            },
            'Fan 1A Tach (0x40)': {
                'Status': 'ok',
                'Sensor Reading': '6960 (+/- 0) RPM',
                'Entity ID': '29.1 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2580.000',
                'Positive Hysteresis': '120.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '15300.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '120.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 1A Tach (0x40)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '4020.000'
            },
            'Fan 3B Tach (0x45)': {
                'Status': 'ok',
                'Sensor Reading': '7104 (+/- 0) RPM',
                'Entity ID': '29.3 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2752.000',
                'Positive Hysteresis': '128.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '16320.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '128.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 3B Tach (0x45)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '3968.000'
            },
            'Fan 2A Tach (0x42)': {
                'Status': 'ok',
                'Sensor Reading': '7080 (+/- 0) RPM',
                'Entity ID': '29.2 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2580.000',
                'Positive Hysteresis': '120.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '15300.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '120.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 2A Tach (0x42)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '4020.000'
            },
            'Fan 4B Tach (0x47)': {
                'Status': 'ok',
                'Sensor Reading': '7488 (+/- 0) RPM',
                'Entity ID': '29.4 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2752.000',
                'Positive Hysteresis': '128.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '16320.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '128.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 4B Tach (0x47)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '3968.000'
            },
            'Fan 2B Tach (0x43)': {
                'Status': 'ok',
                'Sensor Reading': '7168 (+/- 0) RPM',
                'Entity ID': '29.2 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2752.000',
                'Positive Hysteresis': '128.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '16320.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '128.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 2B Tach (0x43)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '3968.000'
            },
            'Fan 5B Tach (0x49)': {
                'Status': 'ok',
                'Sensor Reading': '7296 (+/- 0) RPM',
                'Entity ID': '29.5 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2752.000',
                'Positive Hysteresis': '128.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '16320.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '128.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 5B Tach (0x49)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '3968.000'
            },
            'Fan 1B Tach (0x41)': {
                'Status': 'ok',
                'Sensor Reading': '7296 (+/- 0) RPM',
                'Entity ID': '29.1 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2752.000',
                'Positive Hysteresis': '128.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '16320.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '128.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 1B Tach (0x41)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '3968.000'
            },
            'Fan 6B Tach (0x4b)': {
                'Status': 'ok',
                'Sensor Reading': '7616 (+/- 0) RPM',
                'Entity ID': '29.6 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2752.000',
                'Positive Hysteresis': '128.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '16320.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '128.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 6B Tach (0x4b)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '3968.000'
            },
            'Fan 6A Tach (0x4a)': {
                'Status': 'ok',
                'Sensor Reading': '7080 (+/- 0) RPM',
                'Entity ID': '29.6 (Fan Device)',
                'Assertions Enabled': 'lcr-',
                'Normal Minimum': '2580.000',
                'Positive Hysteresis': '120.000',
                'Assertion Events': '',
                'Event Message Control': 'Per-threshold',
                'Normal Maximum': '15300.000',
                'Deassertions Enabled': 'lcr-',
                'Sensor Type (Analog)': 'Fan',
                'Lower critical': '1920.000',
                'Negative Hysteresis': '120.000',
                'Threshold Read Mask': 'lcr',
                'Maximum sensor range': 'Unspecified',
                'Readable Thresholds': 'lcr',
                'Sensor ID': 'Fan 6A Tach (0x4a)',
                'Settable Thresholds': '',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '4020.000'
            }
        },
        'Voltage': {
            'Planar 12V (0x18)': {
                'Status': 'ok',
                'Sensor Reading': '12.312 (+/- 0) Volts',
                'Entity ID': '7.1 (System Board)',
                'Assertions Enabled': 'lcr- ucr+',
                'Event Message Control': 'Per-threshold',
                'Assertion Events': '',
                'Maximum sensor range': 'Unspecified',
                'Positive Hysteresis': '0.108',
                'Deassertions Enabled': 'lcr- ucr+',
                'Sensor Type (Analog)': 'Voltage',
                'Lower critical': '10.692',
                'Negative Hysteresis': '0.108',
                'Threshold Read Mask': 'lcr ucr',
                'Upper critical': '13.446',
                'Readable Thresholds': 'lcr ucr',
                'Sensor ID': 'Planar 12V (0x18)',
                'Settable Thresholds': 'lcr ucr',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '12.042'
            },
            'Planar 3.3V (0x16)': {
                'Status': 'ok',
                'Sensor Reading': '3.309 (+/- 0) Volts',
                'Entity ID': '7.1 (System Board)',
                'Assertions Enabled': 'lcr- ucr+',
                'Event Message Control': 'Per-threshold',
                'Assertion Events': '',
                'Maximum sensor range': 'Unspecified',
                'Positive Hysteresis': '0.028',
                'Deassertions Enabled': 'lcr- ucr+',
                'Sensor Type (Analog)': 'Voltage',
                'Lower critical': '3.039',
                'Negative Hysteresis': '0.028',
                'Threshold Read Mask': 'lcr ucr',
                'Upper critical': '3.564',
                'Readable Thresholds': 'lcr ucr',
                'Sensor ID': 'Planar 3.3V (0x16)',
                'Settable Thresholds': 'lcr ucr',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '3.309'
            },
            'Planar VBAT (0x1c)': {
                'Status': 'ok',
                'Sensor Reading': '3.137 (+/- 0) Volts',
                'Entity ID': '7.1 (System Board)',
                'Assertions Enabled': 'lnc- lcr-',
                'Event Message Control': 'Per-threshold',
                'Assertion Events': '',
                'Readable Thresholds': 'lcr lnc',
                'Positive Hysteresis': '0.025',
                'Deassertions Enabled': 'lnc- lcr-',
                'Sensor Type (Analog)': 'Voltage',
                'Lower critical': '2.095',
                'Negative Hysteresis': '0.025',
                'Lower non-critical': '2.248',
                'Maximum sensor range': 'Unspecified',
                'Sensor ID': 'Planar VBAT (0x1c)',
                'Settable Thresholds': 'lcr lnc',
                'Threshold Read Mask': 'lcr lnc',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '3.010'
            },
            'Planar 5V (0x17)': {
                'Status': 'ok',
                'Sensor Reading': '5.062 (+/- 0) Volts',
                'Entity ID': '7.1 (System Board)',
                'Assertions Enabled': 'lcr- ucr+',
                'Event Message Control': 'Per-threshold',
                'Assertion Events': '',
                'Maximum sensor range': 'Unspecified',
                'Positive Hysteresis': '0.045',
                'Deassertions Enabled': 'lcr- ucr+',
                'Sensor Type (Analog)': 'Voltage',
                'Lower critical': '4.475',
                'Negative Hysteresis': '0.045',
                'Threshold Read Mask': 'lcr ucr',
                'Upper critical': '5.582',
                'Readable Thresholds': 'lcr ucr',
                'Sensor ID': 'Planar 5V (0x17)',
                'Settable Thresholds': 'lcr ucr',
                'Minimum sensor range': 'Unspecified',
                'Nominal Reading': '4.995'
            }
        }
    }
}


class TestNotifications(test.BaseTestCase):

    def test_ipmi_temperature_notification(self):
        """Based on the above test data the expected sample for a single
        temperature reading has::

        * a resource_id composed from the node_uuid Sensor ID
        * a name composed from 'hardware.ipmi.' and 'temperature'
        * a volume from the first chunk of the Sensor Reading
        * a unit from the last chunk of the Sensor Reading
        * some readings are skipped if the value is 'Disabled'
        """
        processor = ipmi.TemperatureSensorNotification(None)
        counters = dict([(counter.resource_id, counter) for counter in
                         processor.process_notification(SENSOR_DATA)])

        self.assertEqual(len(counters), 10,
                         'expected 10 temperature readings')
        resource_id = (
            'f4982fd2-2f2b-4bb5-9aff-48aac801d1ad-dimm_gh_vr_temp_(0x3b)'
        )
        test_counter = counters[resource_id]
        self.assertEqual(test_counter.volume, 26.0)
        self.assertEqual(test_counter.unit, 'C')
        self.assertEqual(test_counter.type, sample.TYPE_GAUGE)
        self.assertEqual(test_counter.name, 'hardware.ipmi.temperature')

    def test_ipmi_current_notification(self):
        """A single current reading is effectively the same as temperature,
        modulo "current".
        """
        processor = ipmi.CurrentSensorNotification(None)
        counters = dict([(counter.resource_id, counter) for counter in
                         processor.process_notification(SENSOR_DATA)])

        self.assertEqual(len(counters), 1,
                         'expected 1 current reading')
        resource_id = (
            'f4982fd2-2f2b-4bb5-9aff-48aac801d1ad-avg_power_(0x2e)'
        )
        test_counter = counters[resource_id]
        self.assertEqual(test_counter.volume, 130.0)
        self.assertEqual(test_counter.unit, 'Watts')
        self.assertEqual(test_counter.type, sample.TYPE_GAUGE)
        self.assertEqual(test_counter.name, 'hardware.ipmi.current')

    def test_ipmi_fan_notification(self):
        """A single fan reading is effectively the same as temperature,
        modulo "fan".
        """
        processor = ipmi.FanSensorNotification(None)
        counters = dict([(counter.resource_id, counter) for counter in
                         processor.process_notification(SENSOR_DATA)])

        self.assertEqual(len(counters), 12,
                         'expected 12 fan readings')
        resource_id = (
            'f4982fd2-2f2b-4bb5-9aff-48aac801d1ad-fan_4a_tach_(0x46)'
        )
        test_counter = counters[resource_id]
        self.assertEqual(test_counter.volume, 6900.0)
        self.assertEqual(test_counter.unit, 'RPM')
        self.assertEqual(test_counter.type, sample.TYPE_GAUGE)
        self.assertEqual(test_counter.name, 'hardware.ipmi.fan')

    def test_ipmi_voltage_notification(self):
        """A single voltage reading is effectively the same as temperature,
        modulo "voltage".
        """
        processor = ipmi.VoltageSensorNotification(None)
        counters = dict([(counter.resource_id, counter) for counter in
                         processor.process_notification(SENSOR_DATA)])

        self.assertEqual(len(counters), 4,
                         'expected 4 volate readings')
        resource_id = (
            'f4982fd2-2f2b-4bb5-9aff-48aac801d1ad-planar_vbat_(0x1c)'
        )
        test_counter = counters[resource_id]
        self.assertEqual(test_counter.volume, 3.137)
        self.assertEqual(test_counter.unit, 'Volts')
        self.assertEqual(test_counter.type, sample.TYPE_GAUGE)
        self.assertEqual(test_counter.name, 'hardware.ipmi.voltage')
