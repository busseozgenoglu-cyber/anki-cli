import pytest

from anki_cli.cli.params import preprocess_argv


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (
            ["note:add", "deck=Default", "Front=Q", "Back=A"],
            ["note:add", "--deck", "Default", "--Front", "Q", "--Back", "A"],
        ),
        (
            ["note:add", "--deck", "Default", "Front=Q"],
            ["note:add", "--deck", "Default", "--Front", "Q"],
        ),
        (
            ["note:add", "--", "Front=Q", "Back=A"],
            ["note:add", "--", "Front=Q", "Back=A"],
        ),
        (
            ["note:add", "--foo=bar", "Front=Q"],
            ["note:add", "--foo=bar", "--Front", "Q"],
        ),
        (
            ["note:add", "=value", "Front=Q"],
            ["note:add", "=value", "--Front", "Q"],
        ),
        (
            ["note:add", "bad key=value", "Front=Q"],
            ["note:add", "bad key=value", "--Front", "Q"],
        ),
        (
            ["note:add", "Front=a=b"],
            ["note:add", "--Front", "a=b"],
        ),
        (
            ["note:add", "Front="],
            ["note:add", "--Front", ""],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_preprocess_argv(argv: list[str], expected: list[str]) -> None:
    assert preprocess_argv(argv) == expected


@pytest.mark.parametrize(
    ("argv", "value_options"),
    [
        (["cards:ids", "--query", "prop:lapses=0"], {"--query"}),
        (["review", "--deck", "Lang=Spanish"], {"--deck"}),
        (["config:set", "--value", "a==b"], {"--value"}),
    ],
)
def test_preprocess_argv_preserves_values_with_equals(
    argv: list[str],
    value_options: set[str],
) -> None:
    assert preprocess_argv(argv, value_options=value_options) == argv


def test_preprocess_argv_still_rewrites_named_value_ending_with_dashes() -> None:
    assert preprocess_argv(["note:add", "Front=--"]) == ["note:add", "--Front", "--"]


def test_preprocess_argv_preserves_bare_dash() -> None:
    assert preprocess_argv(["-"]) == ["-"]