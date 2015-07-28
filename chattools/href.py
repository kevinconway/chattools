# -*- coding: utf-8 -*-
"""Tools for extracting HREF data."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import re

from defusedxml import ElementTree
import requests


# HREF regex implementation by JOHN GRUBER, available via his blog at
# http://daringfireball.net/2010/07/improved_regex_for_matching_urls. The
# author has released the content as public domain.
REGEX = r"""
(?xi)
\b
(                           # Capture 1: entire matched URL
  (?:
    https?:             # URL protocol and colon
    (?:
      /{1,3}                        # 1-3 slashes
      |                             #   or
      [a-z0-9%]                     # Single letter or digit or '%'
                                    # (Trying not to match e.g. "URI::Escape")
    )
    |                           #   or
                                # looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|
        museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq
        |ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv
        |bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd
        |de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd
        |ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id
        |ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky
        |kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn
        |mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu
        |nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa
        |sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc
        |td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va
        |vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
    /
  )
  (?:                           # One or more:
    [^\s()<>{}\[\]]+                        # Run of non-space, non-()<>{}[]
    |                               #   or
    # balanced parens, one level deep: (...(...)...)
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)
    |
    \([^\s]+?\)                         # balanced parens, non-recursive: (...)
  )+
  (?:                           # End with:
     # balanced parens, one level deep: (...(...)...)
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)
    |
    \([^\s]+?\)                       # balanced parens, non-recursive: (...)
    |                                 #   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]    # not a space or one of these punct chars
  )
  |                 # OR, the following to match naked domains:
  (?:
    (?<!@)          # not preceded by a @, avoid matching foo@_gmail.com_
    [a-z0-9]+
    (?:[.\-][a-z0-9]+)*
    [.]
    (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum
        |name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at
        |au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz
        |ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk
        |dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg
        |gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im
        |in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb
        |lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr
        |ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe
        |pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se
        |sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th
        |tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi
        |vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
    \b
    /?
    # not succeeded by a @, avoid matching "foo.na" in "foo.na@example.com"
    (?!@)
  )
)"""

HREF_REGEX = re.compile(
    REGEX,
    re.UNICODE | re.IGNORECASE | re.MULTILINE | re.VERBOSE,
)


def hrefs(text):
    """Generate an iterable of http://hrefs.com from a given text body.

    Args:
        text (str): The body text of a chat message.

    Returns:
        iter of str: An iterable of strings that represent the hrefs contained
            within the body text.
    """
    for match in HREF_REGEX.findall(text):

        yield match


def requests_body_provider(href):
    """Get the content body of a page identified by an href.

    This implementation uses the requests library to fetch content. If the
    response is not a 2XX then None will be returned instead.

    Args:
        href (str): The location of a web page for which to fetch the content
            body.

    Returns:
        str: The content body as text or None if the body could not be fetched.
    """
    response = requests.get(href)
    if response.status_code < 200 or response.status_code >= 300:

        return None

    return response.text


def etree_title_provider(body):
    """Get the title of a page from its content body.

    This implementation uses the defusedxml wrapper for etree. If no title
    is found on the page then None is returned.

    Args:
        body (str): The content body of an xhtml page.

    Returns:
        str: The text of the first <title></title> tag or None if the title
            is not found or the body is invalid xhtml.
    """
    try:

        root = ElementTree.fromstring(body)

    except ElementTree.ParseError:

        return None

    for title in root.getiterator('title'):

        return title.text

    return None


def titles(
        urls,
        body_provider=requests_body_provider,
        title_provider=etree_title_provider,
):
    """Generate an iterable of page titles from an iterable of hrefs.

    Args:
        urls (iter of str): An iterable of strings that represent the location
            of sites that should have title extracted.
        body_provider: A callable that accepts an href and produces the content
            body of the page. The callable must return None if the content
            body cannot be fetched.
        title_provider: A callable that accepts an xhtml content body and
            produces the title of the page if found. The callable must return
            None if the content body is not valid or if a title cannot be
            found.

    Returns:
        iter of str: An iterable of strings that represent the titles of the
            pages identified within the hrefs iterable. Values may be None
            if the title could not be determined for any reason.
    """
    for url in urls:

        body = body_provider(url)
        if not body:

            yield None

        title = title_provider(body)
        if not title:

            yield None

        yield title
