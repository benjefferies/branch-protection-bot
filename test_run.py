import unittest
from unittest.mock import patch

from run import toggle_enforce_admin


class TestRun(unittest.TestCase):

    @patch('run.enable')
    @patch('run.login')
    def test_should_always_enable_force_admins(self, enable, login):
        # Given
        options = DotDict({
            'access_token': '',
            'repo': '',
            'owner': '',
            'branch': '',
            'retries': 1,
            'enforce_admins': 'true',
        })

        # When
        toggle_enforce_admin(options)

        # Then
        enable.assert_called_once()

    @patch('run.enable')
    def test_should_always_enable_force_admins_when_enabled(self, enable):
        # Given
        options = DotDict({
            'access_token': '',
            'repo': '',
            'owner': '',
            'branch': '',
            'retries': 1,
            'enforce_admins': 'true',
        })

        # When
        with patch('run.login') as mock:
            mock.return_value\
                .repository.return_value\
                .branch.return_value\
                .protection.return_value\
                .enforce_admins.enabled = True
            toggle_enforce_admin(options)

        # Then
        enable.assert_called_once()

    @patch('run.disable')
    @patch('run.login')
    def test_should_always_disable_force_admins(self, disable, login):
        # Given
        options = DotDict({
            'access_token': '',
            'repo': '',
            'owner': '',
            'branch': '',
            'retries': 1,
            'enforce_admins': 'false',
        })

        # When
        toggle_enforce_admin(options)

        # Then
        disable.assert_called_once()

    @patch('run.disable')
    def test_should_always_disable_force_admins_when_disabled(self, disable):
        # Given
        options = DotDict({
            'access_token': '',
            'repo': '',
            'owner': '',
            'branch': '',
            'retries': 1,
            'enforce_admins': 'false',
        })

        # When
        with patch('run.login') as mock:
            mock.return_value\
                .repository.return_value\
                .branch.return_value\
                .protection.return_value\
                .enforce_admins.enabled = False
            toggle_enforce_admin(options)

        # Then
        disable.assert_called_once()

    @patch('run.disable')
    def test_should_disable_force_admins(self, disable):
        # Given
        options = DotDict({
            'access_token': '',
            'repo': '',
            'owner': '',
            'branch': '',
            'retries': 1,
            'enforce_admins': '',
        })

        # When
        with patch('run.login') as mock:
            mock.return_value\
                .repository.return_value\
                .branch.return_value\
                .protection.return_value\
                .enforce_admins.enabled = True
            toggle_enforce_admin(options)

        # Then
        disable.assert_called_once()

    @patch('run.enable')
    def test_should_enable_force_admins(self, enable):
        # Given
        options = DotDict({
            'access_token': '',
            'repo': '',
            'owner': '',
            'branch': '',
            'retries': 1,
            'enforce_admins': '',
        })

        # When
        with patch('run.login') as mock:
            mock.return_value\
                .repository.return_value\
                .branch.return_value\
                .protection.return_value\
                .enforce_admins.enabled = False
            toggle_enforce_admin(options)

        # Then
        enable.assert_called_once()


class DotDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, val):
        if key in self.__dict__:
            self.__dict__[key] = val
        else:
            self[key] = val