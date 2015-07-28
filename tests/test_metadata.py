"""Test suites for the metadata aggregation tools."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json

from chattools import metadata


def test_metadata_aggregates_all_values():
    """Ensure the json text shows all found values."""
    message = """@clair check out the list of (emoticons) at
                https://www.hipchat.com/emoticons"""
    meta = metadata.Metadata(
        message,
        title_provider=lambda urls: ('Emoticons are neat.' for url in urls),
    )
    payload = json.loads(meta.json)
    assert 'mentions' in payload
    assert 'clair' in payload['mentions']
    assert 'emoticons' in payload
    assert 'emoticons' in payload['emoticons']
    assert 'links' in payload
    assert payload['links'][0]['url'] == 'https://www.hipchat.com/emoticons'
    assert payload['links'][0]['title'] == 'Emoticons are neat.'


def test_metadata_optionally_includes_values():
    """Ensure the json text only contains found values."""
    message = 'just some text'
    meta = metadata.Metadata(
        message,
        title_provider=lambda urls: ('Emoticons are neat.' for url in urls),
    )
    payload = json.loads(meta.json)
    assert 'mentions' not in payload
    assert 'emoticons' not in payload
    assert 'links' not in payload
