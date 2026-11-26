"""Best Advice I Ever Got — make.fun entry.

Writes one original sentence about the best advice the writer ever
received to the output path (default /output/entry.txt).

Deterministic, no network, no randomness, no dependencies.
"""

import os

ENTRY = (
    "My first boss, on the day I wanted to quit over one angry "
    "customer, told me, 'One bad table doesn't close the restaurant "
    "\u2014 wipe it down and seat the next one.'"
)

MAX_CHARS = 200
MIN_CHARS = 1


# --- Character checks -------------------------------------------------

def check_not_empty(text):
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")


def check_max_length(text):
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )


def check_min_length(text):
    if len(text) < MIN_CHARS:
        raise ValueError("entry must be at least %d character" % MIN_CHARS)


def check_is_text(text):
    if not isinstance(text, str):
        raise ValueError("entry must be a string")


# --- Sentence checks ---------------------------------------------------

def check_single_sentence(text):
    stripped = text.strip()
    if stripped.count(".") != 1:
        raise ValueError("entry must contain exactly one period")


def check_terminal_period(text):
    stripped = text.strip()
    # A quoted sentence ends with its period just before the closing quote.
    core = stripped[:-1] if stripped.endswith(("'", '"')) else stripped
    if not core.endswith("."):
        raise ValueError("entry must end with a single terminal period")


def check_no_extra_sentence_enders(text):
    body = text.strip()[:-1]
    for mark in ("?", "!"):
        if mark in body:
            raise ValueError("entry must be a single sentence, found %r" % mark)


def check_no_newlines(text):
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def check_no_double_spaces(text):
    if "  " in text:
        raise ValueError("entry must not contain double spaces")


# --- Content checks ----------------------------------------------------

def check_names_a_person(text):
    people = ("boss", "grandfather", "grandmother", "father", "mother",
              "teacher", "coach", "uncle", "aunt", "mentor")
    lowered = text.lower()
    if not any(word in lowered for word in people):
        raise ValueError("entry must name the person who gave the advice")


def check_mentions_advice_given(text):
    if "told me" not in text.lower() and "said" not in text.lower():
        raise ValueError("entry must show the advice being given")


def check_has_quoted_advice(text):
    if "'" not in text:
        raise ValueError("entry must quote the advice itself")


def check_no_generic_slogan(text):
    slogans = ("never give up", "be yourself", "follow your dreams",
               "believe in yourself", "anything is possible")
    lowered = text.lower()
    for slogan in slogans:
        if slogan in lowered:
            raise ValueError("entry must not be a generic slogan: %r" % slogan)


def check_no_addressing_judge(text):
    lowered = text.lower()
    for word in ("dear judge", "judge,"):
        if word in lowered:
            raise ValueError("entry must not address the judge")


# --- Grouped validators ------------------------------------------------

def validate_length(text):
    check_is_text(text)
    check_not_empty(text)
    check_min_length(text)
    check_max_length(text)


def validate_sentence_shape(text):
    check_single_sentence(text)
    check_terminal_period(text)
    check_no_extra_sentence_enders(text)
    check_no_newlines(text)
    check_no_double_spaces(text)


def validate_content(text):
    check_names_a_person(text)
    check_mentions_advice_given(text)
    check_has_quoted_advice(text)
    check_no_generic_slogan(text)
    check_no_addressing_judge(text)


def validate(text=ENTRY):
    validate_length(text)
    validate_sentence_shape(text)
    validate_content(text)
    return text


def output_path():
    return os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main():
    text = validate()
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    print("Wrote %d characters to %s" % (len(text), path))


if __name__ == "__main__":
    main()
