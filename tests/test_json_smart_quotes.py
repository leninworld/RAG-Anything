import pytest

from raganything.modalprocessors import BaseModalProcessor


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        (
            "{\u201cdetailed_description\u201d: \u201cok\u201d, "
            "\u201centity_info\u201d: {\u201centity_name\u201d: \u201cfigure\u201d, "
            "\u201centity_type\u201d: \u201cimage\u201d, \u201csummary\u201d: \u201cexample\u201d}}",
            {
                "detailed_description": "ok",
                "entity_info": {
                    "entity_name": "figure",
                    "entity_type": "image",
                    "summary": "example",
                },
            },
        ),
        (
            "Here is the response: {\u201cdetailed_description\u201d: \u201cok\u201d, "
            "\u201centity_info\u201d: {\u201centity_name\u201d: \u201cfigure\u201d}} End.",
            {
                "detailed_description": "ok",
                "entity_info": {"entity_name": "figure"},
            },
        ),
        (
            "{\u201cdetailed_description\u201d: \u201cok\u201d, "
            "\u201centity_info\u201d: {\u201centity_name\u201d: \u201cfigure\u201d},}",
            {
                "detailed_description": "ok",
                "entity_info": {"entity_name": "figure"},
            },
        ),
        ('{"a": "say \u201chi\u201d",}', {"a": "say \u201chi\u201d"}),
        # This passes without the fix and guards preservation of literal content.
        (
            '{"a": "say \u201chi\u201d, don\u2019t"}',
            {"a": "say \u201chi\u201d, don\u2019t"},
        ),
        (
            "{\u201cdetailed_description\u201d: \u201ccode } snippet\u201d, "
            "\u201centity_info\u201d: {\u201centity_name\u201d: \u201cfigure\u201d}}",
            {
                "detailed_description": "code } snippet",
                "entity_info": {"entity_name": "figure"},
            },
        ),
        (
            "Here is the response: {\u201cdetailed_description\u201d: \u201ccode { snippet\u201d, "
            "\u201centity_info\u201d: {\u201centity_name\u201d: \u201cfigure\u201d}} End }",
            {
                "detailed_description": "code { snippet",
                "entity_info": {"entity_name": "figure"},
            },
        ),
        (
            "```json\n{\u201citems\u201d: [\u201cone\u201d, \u201ctwo\u201d,], "
            "\u201cmeta\u201d: {\u201cok\u201d: true,},}\n```",
            {"items": ["one", "two"], "meta": {"ok": True}},
        ),
    ],
)
def test_json_smart_quotes(response, expected):
    processor = BaseModalProcessor.__new__(BaseModalProcessor)

    assert processor._robust_json_parse(response) == expected
