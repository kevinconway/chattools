"""Test suites for href tools."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import responses

from chattools import href


def test_hrefs_are_empty_if_not_present():
    """Ensure there are no hrefs generated if none exist in the text.

    Example: is anybody there?
    Result: ()
    """
    results = tuple(href.hrefs('is anybody there?'))
    assert not results


def test_href_detects_at_text_start():
    """Ensure hrefs at the beginning of a line of text are found.

    Example: http://example.com/some_page is not a great site.
    Result: ('http://example.com/some_page',)
    """
    results = tuple(
        href.hrefs('http://example.com/some_page is not a great site.')
    )
    assert 'http://example.com/some_page' in results
    assert len(results) == 1


def test_href_detects_mid_stream():
    """Ensure hrefs within the body of the text are found.

    Example: I just discovered https://zombo.com today.
    Result: ('https://zombo.com',)
    """
    results = tuple(
        href.hrefs('I just discovered https://zombo.com today.')
    )
    assert 'https://zombo.com' in results
    assert len(results) == 1


def test_href_detects_end_of_text():
    """Ensure hrefs at the end of a line are also detected.

    Example: Check if you're connected by hitting http://www.purple.com/.
    Results: ('http://www.purple.com/',)
    """
    results = tuple(
        href.hrefs(
            "Check if you're connected by hitting http://www.purple.com/.",
        )
    )
    assert 'http://www.purple.com/' in results
    assert len(results) == 1


def test_href_detects_multiple_hrefs():
    """Ensure multiple hrefs are detected if given.

    Example: Check out https://one.com, http://two.com, and https://three.com!
    Results: (https://one.com, http://two.com, https://three.com)
    """
    results = tuple(
        href.hrefs(
            'Check out https://one.com, http://two.com, and https://three.com!'
        )
    )
    assert 'https://one.com' in results
    assert 'http://two.com' in results
    assert 'https://three.com' in results
    assert len(results) == 3


def test_href_detects_multiline():
    """Ensure the hrefs are detected even if the text more than one line.

    Example: Cool sites for today:
            https://www.reddit.com/
            http://digg.com/ (yes! it's still alive!)
            https://news.ycombinator.com/

    Results: (
        'https://www.reddit.com/',
        'http://digg.com/',
        'https://news.ycombinator.com/',
    )
    """
    results = tuple(
        href.hrefs(
            """Cool sites for today:
            https://www.reddit.com/
            http://digg.com/ (yes! it's still alive!)
            https://news.ycombinator.com/""",
        )
    )
    assert 'https://www.reddit.com/' in results
    assert 'http://digg.com/' in results
    assert 'https://news.ycombinator.com/' in results
    assert len(results) == 3


@responses.activate
def test_requests_body_provider_success():
    """Ensure the provider returns a content body on success."""
    url = 'https://coolsite.com/pages/3'
    body = '<html></html>'
    responses.add(
        responses.GET,
        url,
        body=body,
        status=200,
        content_type='text/html'
    )
    content_body = href.requests_body_provider(url)
    assert content_body == body


@responses.activate
@pytest.mark.parametrize(
    'status',
    tuple(range(300, 600, 1)),
)
def test_requests_body_provider_fail_high(status):
    """Ensure high end non-2xx responses evaluate to None."""
    url = 'https://coolsite.com/pages/3'
    body = '<html></html>'
    responses.add(
        responses.GET,
        url,
        body=body,
        status=status,
        content_type='text/html'
    )
    assert href.requests_body_provider(url) is None


@responses.activate
@pytest.mark.parametrize(
    'status',
    tuple(range(0, 200, 1)),
)
def test_requests_body_provider_fail_low(status):
    """Ensure low end non-2xx responses evaluate to None."""
    url = 'https://coolsite.com/pages/3'
    body = '<html></html>'
    responses.add(
        responses.GET,
        url,
        body=body,
        status=status,
        content_type='text/html'
    )
    assert href.requests_body_provider(url) is None


def test_etree_title_provider_invalid_xhtml():
    """Ensure the provider returns None when the content body is invalid."""
    body = '<html><head><title>TEST</title></head>'
    assert href.etree_title_provider(body) is None


def test_scanning_title_provider_invalid_xhtml():
    """Ensure the provider returns a title even if the content is invalid."""
    body = '<html><head><title>TEST</title></head>'
    assert href.scanning_title_provider(body) == 'TEST'


def test_scanning_title_provider_unbounded_title():
    """Ensure the provider returns None when the title is unbounded."""
    body = '<html><head><title>TEST</head></html>'
    assert href.scanning_title_provider(body) is None


@pytest.mark.parametrize(
    'title_provider',
    (href.etree_title_provider, href.scanning_title_provider),
)
def test_title_provider_missing_title(title_provider):
    """Ensure the provider returns None when the title is missing."""
    body = '<html><head></head><body></body></html>'
    assert title_provider(body) is None


@pytest.mark.parametrize(
    'title_provider',
    (href.etree_title_provider, href.scanning_title_provider),
)
def test_title_provider_fetches_title(title_provider):
    """Ensure the title is returned if present."""
    title = 'TEST PAGE'
    body = '<html><head><title>{0}</title></head><body></body></html>'.format(
        title,
    )
    assert title_provider(body) == title


@pytest.mark.parametrize(
    'title_provider',
    (href.etree_title_provider, href.scanning_title_provider),
)
def test_title_provider_fetches_first_title(title_provider):
    """Ensure the first title is returned if multiple are present."""
    title = 'TEST PAGE'
    title2 = 'TEST PAGE 2'
    body = (
        '<html><head><title>{0}</title>'
        '<title>{1}</title></head><body></body></html>'.format(
            title,
            title2,
        )
    )
    assert title_provider(body) == title


def test_titles_uses_given_providers():
    """Ensure the titles generator uses configurable data providers."""
    def body_provider(url):

        return '<html></html>'

    def title_provider(body):

        return 'TEST'

    hrefs = (
        'https://www.reddit.com/'
        'http://digg.com/',
        'https://news.ycombinator.com/',
    )
    titles = tuple(
        href.titles(
            hrefs,
            body_provider=body_provider,
            title_provider=title_provider,
        )
    )
    for title in titles:

        assert title == 'TEST'


def test_titles_generates_none_if_no_body():
    """Ensure the titles produces None if not body is fetched.."""
    def body_provider(url):

        return None

    def title_provider(body):

        return None

    hrefs = (
        'https://www.reddit.com/'
        'http://digg.com/',
        'https://news.ycombinator.com/',
    )
    titles = tuple(
        href.titles(
            hrefs,
            body_provider=body_provider,
            title_provider=title_provider,
        )
    )
    for title in titles:

        assert title is None


def test_titles_generates_none_if_no_title():
    """Ensure the titles produces None if no title is fetched.."""
    def body_provider(url):

        return '<html></html>'

    def title_provider(body):

        return None

    hrefs = (
        'https://www.reddit.com/'
        'http://digg.com/',
        'https://news.ycombinator.com/',
    )
    titles = tuple(
        href.titles(
            hrefs,
            body_provider=body_provider,
            title_provider=title_provider,
        )
    )
    for title in titles:

        assert title is None
