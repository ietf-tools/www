import pytest

from ietf.snippets.factories import CharterFactory, WorkingGroupFactory

pytestmark = pytest.mark.django_db


def test_link_working_group():
    working_group = WorkingGroupFactory()
    snippet = CharterFactory(working_group=working_group)
    assert snippet.url == working_group.charter_url
