"""Tools for extracting all content metadata."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json

from . import emoticon
from . import href
from . import mention


JSON_PROVIDER = json.dumps


class Metadata(object):

    """Metadata container for a chat message."""

    def __init__(
            self,
            message,
            emoticon_provider=emoticon.emoticons,
            href_provider=href.hrefs,
            title_provider=href.titles,
            mention_provider=mention.mentions,
            json_provider=JSON_PROVIDER,
    ):
        """Initialize the container with a message and content providers.

        Args:
            message (str): The message text for which to generate metadata.
            emoticon_provider: A callable that generates an iterable of
                emoticons from a message text.
            href_provider: A callable that generates an iterable of hrefs
                from a message text.
            title_provider: A callable that generates an iterable of titles
                from an iterable of hrefs.
            mention_provider: A callable that generates an iterable of mentions
                from a message text.
            json_provider: A callable that converts a Python dictionary into
                JSON text.
        """
        self._message = message
        self._emoticon_provider = emoticon_provider
        self._href_provider = href_provider
        self._title_provider = title_provider
        self._mention_provider = mention_provider
        self._json_provider = json_provider

    @property
    def emoticons(self):
        """Get an iterable of emoticons used in the message."""
        return self._emoticon_provider(self._message)

    @property
    def links(self):
        """Get an iterable of links used in the message.

        Each element is a two-tuple in the form of (url, title).
        """
        hrefs = tuple(self._href_provider(self._message))
        return zip(hrefs, self._title_provider(hrefs))

    @property
    def mentions(self):
        """Get an iterable of mentions used in the message."""
        return self._mention_provider(self._message)

    @property
    def json(self):
        """Get a JSON text payload that represents the message metadata.

        The format of the JSON object is:

            {
                "mentions": ["mary", "geetha"],
                "emoticons": ["mindblown"],
                "links": [
                    {"url": "https://something.com", "title": "Page title!"}
                ]
            }
        """
        payload = {}
        emoticons = tuple(self.emoticons)
        links = tuple(self.links)
        mentions = tuple(self.mentions)
        if emoticons:

            payload['emoticons'] = emoticons

        if links:

            payload['links'] = []
            for url, title in links:

                payload['links'].append({"url": url, "title": title})

        if mentions:

            payload['mentions'] = mentions

        return self._json_provider(payload)
