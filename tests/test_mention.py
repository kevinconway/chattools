"""Test suites for @mention tools."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from chattools import mention


def test_mentions_are_empty_if_not_present():
    """Ensure there are no mentions generated if not exist in the text.

    Example: mary, you there?
    Result: ()
    """
    results = tuple(mention.mentions('mary, you there?'))
    assert not results


def test_mention_detects_at_text_start():
    """Ensure mentions at the beginning of a line of text are found.

    Example: @mary, you there?.
    Result: ('mary',)
    """
    results = tuple(mention.mentions('@mary, you there?'))
    assert 'mary' in results
    assert len(results) == 1


def test_mention_detects_mid_stream():
    """Ensure mentions within the body of the text are found.

    Example: Has anyone seen @mary today? I need her help.
    Result: ('mary',)
    """
    results = tuple(
        mention.mentions('Has anyone seen @mary today? I need her help.')
    )
    assert 'mary' in results
    assert len(results) == 1


def test_mention_detects_end_of_text():
    """Ensure mentions at the end of a line are also detected.

    Example: When you get a chance, I really need your help with this @mary!
    Results: ('mary',)
    """
    results = tuple(
        mention.mentions(
            'When you get a chance, I really need your help with this @mary!',
        )
    )
    assert 'mary' in results
    assert len(results) == 1


def test_mention_detects_multiple_mentions():
    """Ensure multiple mentions are detected if given.

    Example: Hey, @mary & @geetha, thanks for knocking out that bug!
    Results: (mary, geetha)
    """
    results = tuple(
        mention.mentions(
            'Hey, @mary & @geetha, thanks for knocking out that bug!',
        )
    )
    assert 'mary' in results
    assert 'geetha' in results
    assert len(results) == 2


def test_mention_detects_multiline():
    """Ensure the mentions are detected even if the text more than one line.

    Example: @everyone, three cheers for our team's MVPs of the day!
            @mary, @geetha resolved a major customer issue!
            Drinks on @themanager tonight!

    Results: ('everyone', 'mary', 'geetha', 'themanager')
    """
    results = tuple(
        mention.mentions(
            """@everyone, three cheers for our team's MVPs of the day!
            @mary, @geetha resolved a major customer issue!
            Drinks on @themanager tonight!""",
        )
    )
    assert 'everyone' in results
    assert 'mary' in results
    assert 'geetha' in results
    assert 'themanager' in results
    assert len(results) == 4


def test_mention_skips_emails():
    """Ensure email addresses are not mistaken for mentions.

    Example: @riddhi, try emailing the new team @ devtools@ourcorp.com.
    Results: ('riddhi',)
    """
    results = tuple(
        mention.mentions(
            '@riddhi, try emailing the new team @ devtools@ourcorp.com.',
        )
    )
    assert 'riddhi' in results
    assert 'ourcorp' not in results
    assert 'ourcorp.com' not in results
    assert len(results) == 1
