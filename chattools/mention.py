"""Tools for extracting @mention data."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import re


MENTION_REGEX = re.compile(
    r'(\s|\W|^)+@(\w+)',
    re.UNICODE | re.IGNORECASE | re.MULTILINE,
)


def mentions(text):
    """Generate an iterable of @mentions from a given text body.

    Args:
        text (str): The body text of a chat message.

    Returns:
        iter of str: An iterable of strings that represent the @mentions used
            within the body text.
    """
    for _, match in MENTION_REGEX.findall(text):

        yield match
