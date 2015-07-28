"""Tools for extracting emoticon data."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import re


EMOTICON_REGEX = re.compile(
    r'\((\w{1,15})\)',
    re.UNICODE | re.IGNORECASE | re.MULTILINE,
)


def emoticons_regex(text):
    """Generate an iterable of (emoticons) from a given text body.

    This implementation uses regular expressions to select emoticon text from
    the source. If valid emoticons cannot contain parenthesis characters then
    this implementation cannot be used as the recursive (emoti(con)) would have
    the (con) portion returned as an emoticon.

    Args:
        text (str): The body text of a chat message.

    Returns:
        iter of str: An iterable of strings that represent the emoticons used
            within the body text.
    """
    for match in EMOTICON_REGEX.findall(text):

        yield match


def emoticons(text):
    """Generate an iterable of emoticons from a given text body.

    This implementation bypasses the use of regex in order to filter out
    invalid emoticons containing nested parenthesis characters. This method
    will read a top level emoticon (emoti(con)) until the final enclosing
    parenthesis is read. If the resulting capture contains any nested
    parenthesis characters the result is discarded.

    Args:
        text (str): The body text of a chat message.

    Returns:
        iter of str: An iterable of strings that represent the emoticons used
            within the body text.
    """
    emoticon = []
    level = 0
    for letter in text:

        if letter == '(':

            level += 1

        if letter == ')':

            level -= 1

        if level > 0:

            emoticon.append(letter)

        if level < 1 and emoticon:

            result = ''.join(emoticon)[1:]
            emoticon = []
            if '(' in result or ')' in result:

                continue

            yield result
