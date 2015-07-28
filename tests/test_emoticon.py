"""Test suites for emoticon tools."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from chattools import emoticon


@pytest.mark.parametrize(
    'emoticons',
    (emoticon.emoticons, emoticon.emoticons_regex),
)
def test_emoticons_are_empty_if_not_present(emoticons):
    """Ensure there are no emoticons generated none present in the text.

    Example: clara, you there?
    Result: ()
    """
    results = tuple(emoticons('clara, you there?'))
    assert not results


@pytest.mark.parametrize(
    'emoticons',
    (emoticon.emoticons, emoticon.emoticons_regex),
)
def test_emoticon_detects_at_text_start(emoticons):
    """Ensure emoticons at the beginning of a line of text are found.

    Example: (alert)@clara, you there?.
    Result: ('alert',)
    """
    results = tuple(emoticons('(alert)@clara, you there?'))
    assert 'alert' in results
    assert len(results) == 1


@pytest.mark.parametrize(
    'emoticons',
    (emoticon.emoticons, emoticon.emoticons_regex),
)
def test_emoticon_detects_mid_stream(emoticons):
    """Ensure emoticons within the body of the text are found.

    Example: Has anyone (seen) clara today? I need her help.
    Result: ('seen',)
    """
    results = tuple(
        emoticons('Has anyone (seen) clara today? I need her help.')
    )
    assert 'seen' in results
    assert len(results) == 1


@pytest.mark.parametrize(
    'emoticons',
    (emoticon.emoticons, emoticon.emoticons_regex),
)
def test_emoticon_detects_end_of_text(emoticons):
    """Ensure emoticons at the end of a line are also detected.

    Example: I really need your help with this clara! (panic)!
    Results: ('panic',)
    """
    results = tuple(
        emoticons(
            'I really need your help with this clara! (panic)!',
        )
    )
    assert 'panic' in results
    assert len(results) == 1


@pytest.mark.parametrize(
    'emoticons',
    (emoticon.emoticons, emoticon.emoticons_regex),
)
def test_emoticon_detects_multiple_emoticons(emoticons):
    """Ensure multiple emoticons are detected if given.

    Example: (mindblown) (motherofgod)... thanks for stomping that bug, clara!
    Results: (mindblown, motherofgod)
    """
    results = tuple(
        emoticons(
            '(mindblown) (motherofgod)... thanks for stomping that bug, clara!'
        )
    )
    assert 'mindblown' in results
    assert 'motherofgod' in results
    assert len(results) == 2


@pytest.mark.parametrize(
    'emoticons',
    (emoticon.emoticons, emoticon.emoticons_regex),
)
def test_emoticon_detects_multiline(emoticons):
    """Ensure the emoticons are detected even if the text more than one line.

    Example: everyone, (standup) & (salute) our team's MVP of the day!
            we all said (huh) but clara said (goodnews)!
            (beer) on the manager tonight!

    Results: ('standup', 'salute', 'huh', 'goodnews', 'beer')
    """
    results = tuple(
        emoticons(
            """everyone, (standup) & (salute) our team's MVP of the day!
            we all said (huh) but clara said (goodnews)!
            (beer) on the manager tonight!""",
        )
    )
    assert 'standup' in results
    assert 'salute' in results
    assert 'huh' in results
    assert 'goodnews' in results
    assert 'beer' in results
    assert len(results) == 5


def test_emoticon_skips_invalid_parens():
    """Ensure emoticons are not detected if they use too many parens.

    Example: (emoti(con)).
    Results: ()
    """
    results = tuple(
        emoticon.emoticons('(emoti(con)).')
    )
    assert not results


def test_emoticon_skips_unbounded_parens():
    """Ensure emoticons are not detected if they use too little parens.

    Example: (emoti (con).
    Results: ()
    """
    results = tuple(
        emoticon.emoticons('(emoti (con).')
    )
    assert not results


@pytest.mark.parametrize(
    'emoticons',
    (emoticon.emoticons, emoticon.emoticons_regex),
)
def test_emoticon_skips_too_short(emoticons):
    """Ensure emoticons are not detected if they contain no content.

    Example: ().
    Results: ()
    """
    results = tuple(
        emoticons('().')
    )
    assert not results


@pytest.mark.parametrize(
    'emoticons',
    (emoticon.emoticons, emoticon.emoticons_regex),
)
def test_emoticon_skips_too_long(emoticons):
    """Ensure emoticons are not detected if they contain too much content.

    Example: (1234567890123456).
    Results: ()
    """
    results = tuple(
        emoticons('(1234567890123456).')
    )
    assert not results
