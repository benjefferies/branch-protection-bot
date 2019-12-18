import unittest
from unittest.mock import patch

from run import toggle_enforce_admin


class TestRun(unittest.TestCase):

    @patch('run.login')
    @patch('run.enable')
    def test_should_always_enable_force_admins(self, enable, login):
        # Given
        options = DotDict({
            'retries': 1,
            'enforce_admins': 'true',
            'owner': 'benjefferies',
            'repo': 'branch-bot-protection',
        })

        # When
        toggle_enforce_admin(options)

        # Then
        enable.assert_called_once()
        login.return_value.repository.assert_called_once_with('benjefferies', 'branch-bot-protection')

    @patch('run.enable')
    def test_should_always_enable_force_admins_when_enabled(self, enable):
        # Given
        options = DotDict({
            'retries': 1,
            'enforce_admins': 'true',
            'github_repository': 'benjefferies/branch-bot-protection'
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

    @patch('run.login')
    @patch('run.disable')
    def test_should_always_disable_force_admins(self, disable, login):
        # Given
        options = DotDict({
            'retries': 1,
            'enforce_admins': 'false',
            'github_repository': 'benjefferies/branch-bot-protection'
        })

        # When
        toggle_enforce_admin(options)

        # Then
        disable.assert_called_once()

    @patch('run.disable')
    def test_should_always_disable_force_admins_when_disabled(self, disable):
        # Given
        options = DotDict({
            'retries': 1,
            'enforce_admins': 'false',
            'github_repository': 'benjefferies/branch-bot-protection'
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
            'retries': 1,
            'github_repository': 'benjefferies/branch-bot-protection'
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
            'retries': 1,
            'github_repository': 'benjefferies/branch-bot-protection'
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

    @patch('run.login')
    @patch('run.enable')
    def test_should_enable_force_admins_using_github_repository_environment_variables(self, enable, login):
        # Given
        options = DotDict({
            'retries': 1,
            'enforce_admins': 'true',
            'github_repository': 'benjefferies/branch-bot-protection'
        })

        # When
        toggle_enforce_admin(options)

        # Then
        enable.assert_called_once()
        login.return_value.repository.assert_called_once_with('benjefferies', 'branch-bot-protection')

    def test_should_error_when_no_github_repository_or_owner_and_repo(self):
        # Given
        options = DotDict({
            'retries': 1,
            'enforce_admins': 'true',
        })

        # When
        to_error = lambda: toggle_enforce_admin(options)

        # Then
        self.assertRaises(RuntimeError, to_error)

    @patch('run.login')
    @patch('run.enable')
    def test_should_use_owner_repo_over_github_repository(self, enable, login):
        # Given
        options = DotDict({
            'retries': 1,
            'enforce_admins': 'true',
            'owner': 'benjefferies',
            'repo': 'branch-protection-bot',
            'github_repository': 'other/repo'
        })

        # When
        toggle_enforce_admin(options)

        # Then
        enable.assert_called_once()
        login.return_value.repository.assert_called_once_with('benjefferies', 'branch-protection-bot')


class DotDict(dict):
    def __getattr__(self, key):
        return self[key] if key in self else ''

    def __setattr__(self, key, val):
        if key in self.__dict__:
            self.__dict__[key] = val
        else:
            self[key] = val