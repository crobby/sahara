# Copyright (c) 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from keystoneclient import session as keystone
import mock

from sahara import exceptions as ex
from sahara.service import sessions
from sahara.tests.unit import base


class TestSessionCache(base.SaharaTestCase):

    def test_get_session(self):
        sc = sessions.SessionCache()
        session = sc.get_session()
        self.assertTrue(isinstance(session, keystone.Session))

        self.assertRaises(ex.SaharaException,
                          sc.get_session,
                          session_type='bad service')

    @mock.patch('keystoneclient.session.Session')
    def test_get_keystone_session(self, keystone_session):
        sc = sessions.SessionCache()
        self.override_config('ca_file', '/some/cacert', group='keystone')
        self.override_config('api_insecure', True, group='keystone')
        sc.get_session(sessions.SESSION_TYPE_KEYSTONE)
        keystone_session.assert_called_once_with(cert='/some/cacert',
                                                 verify=True)

        sc = sessions.SessionCache()
        keystone_session.reset_mock()
        self.override_config('ca_file', None, group='keystone')
        self.override_config('api_insecure', None, group='keystone')
        sc.get_session(sessions.SESSION_TYPE_KEYSTONE)
        keystone_session.assert_called_once_with()

        keystone_session.reset_mock()
        sc.get_session(sessions.SESSION_TYPE_KEYSTONE)
        self.assertFalse(keystone_session.called)

    @mock.patch('keystoneclient.session.Session')
    def test_get_nova_session(self, keystone_session):
        sc = sessions.SessionCache()
        self.override_config('ca_file', '/some/cacert', group='nova')
        self.override_config('api_insecure', True, group='nova')
        sc.get_session(sessions.SESSION_TYPE_NOVA)
        keystone_session.assert_called_once_with(cert='/some/cacert',
                                                 verify=True)

        sc = sessions.SessionCache()
        keystone_session.reset_mock()
        self.override_config('ca_file', None, group='nova')
        self.override_config('api_insecure', None, group='nova')
        sc.get_session(sessions.SESSION_TYPE_NOVA)
        keystone_session.assert_called_once_with()

        keystone_session.reset_mock()
        sc.get_session(sessions.SESSION_TYPE_NOVA)
        self.assertFalse(keystone_session.called)

    @mock.patch('keystoneclient.session.Session')
    def test_get_cinder_session(self, keystone_session):
        sc = sessions.SessionCache()
        self.override_config('ca_file', '/some/cacert', group='cinder')
        self.override_config('api_insecure', True, group='cinder')
        sc.get_session(sessions.SESSION_TYPE_CINDER)
        keystone_session.assert_called_once_with(cert='/some/cacert',
                                                 verify=True)

        sc = sessions.SessionCache()
        keystone_session.reset_mock()
        self.override_config('ca_file', None, group='cinder')
        self.override_config('api_insecure', None, group='cinder')
        sc.get_session(sessions.SESSION_TYPE_CINDER)
        keystone_session.assert_called_once_with()

        keystone_session.reset_mock()
        sc.get_session(sessions.SESSION_TYPE_CINDER)
        self.assertFalse(keystone_session.called)

    @mock.patch('keystoneclient.session.Session')
    def test_get_neutron_session(self, keystone_session):
        sc = sessions.SessionCache()
        self.override_config('ca_file', '/some/cacert', group='neutron')
        self.override_config('api_insecure', True, group='neutron')
        sc.get_session(sessions.SESSION_TYPE_NEUTRON)
        keystone_session.assert_called_once_with(cert='/some/cacert',
                                                 verify=True)

        sc = sessions.SessionCache()
        keystone_session.reset_mock()
        self.override_config('ca_file', None, group='neutron')
        self.override_config('api_insecure', None, group='neutron')
        sc.get_session(sessions.SESSION_TYPE_NEUTRON)
        keystone_session.assert_called_once_with()

        keystone_session.reset_mock()
        sc.get_session(sessions.SESSION_TYPE_NEUTRON)
        self.assertFalse(keystone_session.called)
