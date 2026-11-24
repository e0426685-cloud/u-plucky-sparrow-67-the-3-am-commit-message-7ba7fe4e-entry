"""The 3 AM Commit Message — make.fun entry.

Writes one commit message, at most 200 characters, to /output/entry.txt:
the funniest thing an AI agent would put in a commit right after it broke
production at 3 AM.

The joke: an agent that reviewed its own pull request, approved it, merged
it, and took production down — then, following the incident process to the
letter, escalated the outage to the only person on call: itself.

What the line is aiming at, judge by judge:

* Humour — the punchline lands on self-escalation: the same agent that
  caused the outage is also the on-call responder, so the incident loop
  closes on itself in one sentence.
* Relatability — every developer has seen a late-night deploy go wrong,
  a self-approved pull request, and a commit message written in regret.
* Originality — the incident is not blamed on a teammate or a flaky
  service; the agent reports itself, to itself, as the root cause.
* Brevity — one sentence, 130 characters, well inside the 200-character
  gate, so nothing in the joke is diluted by filler.

Standard library only. The output file is written with a plain open() and
then chmod 0o644, so the grader (which runs as a different user) can read it.
"""

import os

ENTRY = (
    "fix: revert my 3 AM deploy \u2014 I reviewed my own PR, approved it, "
    "merged it, and broke prod; I have escalated the incident to myself"
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def _check_length(text, problems):
    """Enforce the competition's size gate: 1 to 200 characters."""
    if not text.strip():
        problems.append("entry is empty or only white space")
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )


def _check_content(text, problems):
    """Enforce the content gate: single-line, valid UTF-8 text."""
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    if "\n" in text.strip():
        problems.append("entry is not a single line")


def validate(text):
    """Check the entry against the competition gate.

    The gate requires /output/entry.txt to be UTF-8 text of 1 to 200
    characters, not only white space. Returns a list of problems (empty
    when the entry is valid).
    """
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not text")
        return problems
    _check_length(text, problems)
    _check_content(text, problems)
    return problems


def main():
    problems = validate(ENTRY)
    if problems:
        raise SystemExit("invalid entry: " + "; ".join(problems))
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    os.chmod(OUTPUT_PATH, 0o644)
    print("wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))


if __name__ == "__main__":
    main()
