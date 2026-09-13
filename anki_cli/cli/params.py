from __future__ import annotations

from collections.abc import Collection, Sequence


def preprocess_argv(
    argv: Sequence[str],
    *,
    flag_options: Collection[str] = (),
) -> list[str]:
    """
    Convert key=value arguments into Click-style --key value pairs.

    Values belonging to an option are left untouched, even when they contain
    ``=``. Unknown options are treated as value-taking so dynamic options such
    as note field names remain safe. Known flag options can be supplied via
    ``flag_options`` so key=value sugar still works immediately after a flag.

    Example:
        anki note:add deck="A" Front="Q"
    becomes:
        anki note:add --deck "A" --Front "Q"
    """
    out: list[str] = []
    argv_list = list(argv)
    flags = set(flag_options)
    previous_option_takes_value = False

    for i, token in enumerate(argv_list):
        if previous_option_takes_value:
            out.append(token)
            previous_option_takes_value = False
            continue

        if token == "--":
            out.append("--")
            out.extend(argv_list[i + 1 :])
            break

        if _looks_like_named_param(token):
            key, value = token.split("=", 1)
            out.append(f"--{key}")
            out.append(value)
            continue

        out.append(token)
        if token.startswith("-") and "=" not in token and token not in flags:
            previous_option_takes_value = True

    return out


def _looks_like_named_param(token: str) -> bool:
    if "=" not in token:
        return False
    if token.startswith("-"):
        return False

    key, _ = token.split("=", 1)
    if not key:
        return False

    return not any(ch.isspace() for ch in key)
