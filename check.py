#!/usr/bin/env python3
"""Structural checks for doc-skills-library.

Run: python check.py
Exit 0 if every check passes, 1 if any fails. No third-party imports, no network.

What this does NOT do: it cannot tell you whether a skill produces good output.
These skills are prompts; their behaviour is a model's behaviour and is not
testable from here. Everything below is a property of the files on disk, which is
the part that can rot silently while still looking fine in a diff.

Each check corresponds to a claim the README makes. If a check and the README
disagree, the README is wrong.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# --- baselines -------------------------------------------------------------
# Counted by this script on a clean tree. A change here is not automatically a
# bug, but it should be a deliberate edit to both the constant and the README,
# not a surprise.
EXPECTED_SKILL_COUNT = 21
EXPECTED_LOCAL_LINKS = 34

# Mirrors the README "Limitations" section. check_contract() also verifies the
# README still names these same skills, so the two cannot drift apart.
EXPECTED_CONTRACT_EXCEPTIONS = {"house-style", "verify-loop", "source-backed-rfp"}
EXPECTED_NO_OUTPUT_BLOCK = {"rubber-duck", "house-style", "source-backed-rfp"}

# The one em dash in the repo is the counter-example inside the house-style rule
# that forbids em dashes. Anywhere else is a violation of the rule itself.
EM_DASH = "\u2014"
EM_DASH_ALLOWED_IN = "skills/house-style/SKILL.md"
SMART_QUOTES = {
    "\u2018": "left single quote",
    "\u2019": "right single quote",
    "\u201c": "left double quote",
    "\u201d": "right double quote",
}

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", ".idea", ".vscode", "docs", "reports"}
# config.yml is the gitignored local file holding real hostnames and project
# keys. It is not part of the published repo, so it is not this script's
# business and scanning it would report the user's own values back at them.
SKIP_FILES = {"config.yml", "config.yaml"}


def out(line=""):
    """Print without dying on a cp1252 console."""
    sys.stdout.write(line.encode("ascii", "backslashreplace").decode("ascii") + "\n")


failures = []


def fail(check, message):
    failures.append((check, message))


# --- file discovery --------------------------------------------------------

def walk_files():
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if fn in SKIP_FILES or fn.endswith((".pyc", ".pyo")):
                continue
            found.append(os.path.join(dirpath, fn))
    return found


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


ALL_FILES = walk_files()
MD_FILES = [p for p in ALL_FILES if p.lower().endswith(".md")]
SKILLS_DIR = os.path.join(ROOT, "skills")
SKILL_NAMES = sorted(
    d for d in os.listdir(SKILLS_DIR)
    if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
)


# --- shared markdown helpers ----------------------------------------------

FENCE_RE = re.compile(r"^\s*(```|~~~)")


def strip_fences(text):
    """Blank out fenced code blocks, keeping line numbers stable.

    Needed because most skills put a literal '## Report Title' inside their
    Output Format template. That is sample output, not a heading, and counting
    it as one makes every skill look like a contract violation.
    """
    kept = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            kept.append("")
            continue
        kept.append("" if in_fence else line)
    return "\n".join(kept)


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)


def headings(text, level=None):
    result = []
    for m in HEADING_RE.finditer(strip_fences(text)):
        if level is None or len(m.group(1)) == level:
            result.append((len(m.group(1)), m.group(2)))
    return result


def slugify(heading):
    """GitHub's heading-anchor rules, as far as they matter here.

    Strip inline markdown emphasis and code ticks, lowercase, drop everything
    that is not a word character, space or hyphen, then spaces to hyphens.
    """
    s = heading
    s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)      # images -> alt text
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)        # links -> link text
    s = s.replace("`", "")
    s = re.sub(r"[*_~]", "", s)
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return re.sub(r"\s+", "-", s)


def anchors_for(path):
    """Every anchor GitHub would generate for a file, including -1/-2 dupes."""
    slugs = set()
    counts = {}
    for _level, text in headings(read(path)):
        base = slugify(text)
        n = counts.get(base, 0)
        slugs.add(base if n == 0 else "%s-%d" % (base, n))
        counts[base] = n + 1
    return slugs


# --- check 1: every markdown link resolves --------------------------------

# Inline links only: [text](target). Negative lookbehind skips images. The
# target must be parenthesis- and space-free, which every link in this repo is.
LINK_RE = re.compile(r"(?<!!)\[([^\]\[]*)\]\(([^()\s]+)\)")


def check_links():
    total = 0
    dangling = 0
    for path in MD_FILES:
        body = read(path)
        for _label, target in LINK_RE.findall(body):
            if re.match(r"^(https?:|mailto:|#?[a-z+.-]+://)", target, re.I):
                continue  # external, not ours to verify offline
            total += 1
            filepart, _, anchor = target.partition("#")
            if filepart:
                dest = os.path.normpath(os.path.join(os.path.dirname(path), filepart))
            else:
                dest = path  # same-file anchor
            if not os.path.isfile(dest):
                dangling += 1
                fail("links", "%s -> %s : file does not exist" % (rel(path), target))
                continue
            if anchor:
                if not dest.lower().endswith(".md"):
                    continue  # cannot resolve an anchor in a non-markdown target
                if anchor.lower() not in anchors_for(dest):
                    dangling += 1
                    fail("links", "%s -> %s : no heading in %s slugifies to '%s'"
                         % (rel(path), target, rel(dest), anchor.lower()))
    out("  %d markdown files, %d local links, %d dangling" % (len(MD_FILES), total, dangling))
    if total != EXPECTED_LOCAL_LINKS:
        fail("links", "local link count is %d, expected %d. If the change was "
                      "intentional, update EXPECTED_LOCAL_LINKS and the README."
             % (total, EXPECTED_LOCAL_LINKS))


# --- check 2: frontmatter --------------------------------------------------

CONTRACT_KEYS = ["name", "description", "user_invocable"]


def parse_frontmatter(text):
    """Hand-rolled, because PyYAML is not in the standard library.

    Handles only what this contract allows: a leading '---' block of top-level
    'key: value' lines, values optionally double- or single-quoted on one line.
    Anything else (nesting, block scalars, lists, a multi-line value) is
    reported as a parse failure rather than guessed at, which is the point: the
    contract says three scalar keys, so a file needing real YAML has already
    broken it.
    """
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None, "no opening '---' on line 1"
    body = text.split("\n", 1)[1]
    end = re.search(r"^---\s*$", body, re.M)
    if not end:
        return None, "frontmatter block is never closed with '---'"
    pairs = []
    for i, line in enumerate(body[:end.start()].splitlines(), start=2):
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not m:
            return None, "line %d is not a top-level 'key: value' pair: %r" % (i, line[:60])
        key, value = m.group(1), m.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        pairs.append((key, value))
    return pairs, None


def check_frontmatter():
    for name in SKILL_NAMES:
        path = os.path.join(SKILLS_DIR, name, "SKILL.md")
        pairs, err = parse_frontmatter(read(path))
        if err:
            fail("frontmatter", "%s: %s" % (rel(path), err))
            continue
        keys = [k for k, _ in pairs]
        if keys != CONTRACT_KEYS:
            fail("frontmatter", "%s: keys are %s, contract is exactly %s (in order)"
                 % (rel(path), keys, CONTRACT_KEYS))
            continue
        values = dict(pairs)
        if values["name"] != name:
            fail("frontmatter", "%s: name is '%s' but the directory is '%s'"
                 % (rel(path), values["name"], name))
        if values["user_invocable"] != "true":
            fail("frontmatter", "%s: user_invocable is '%s', must be 'true'"
                 % (rel(path), values["user_invocable"]))
        if not values["description"].strip():
            fail("frontmatter", "%s: description is empty" % rel(path))
    out("  %d SKILL.md frontmatter blocks parsed, keys %s"
        % (len(SKILL_NAMES), "/".join(CONTRACT_KEYS)))


# --- check 3: skill count matches the README table ------------------------

README = os.path.join(ROOT, "README.md")
TABLE_ROW_RE = re.compile(r"^\|\s*`/([a-z0-9][a-z0-9-]*)`\s*\|", re.M)


def check_readme_table():
    rows = TABLE_ROW_RE.findall(read(README))
    dupes = sorted({r for r in rows if rows.count(r) > 1})
    if dupes:
        fail("readme-table", "README lists these skills more than once: %s" % dupes)
    row_set, dir_set = set(rows), set(SKILL_NAMES)
    for missing in sorted(dir_set - row_set):
        fail("readme-table", "skills/%s/ exists but has no row in the README table" % missing)
    for extra in sorted(row_set - dir_set):
        fail("readme-table", "README table has a row for '/%s' but skills/%s/ does not exist"
             % (extra, extra))
    if len(SKILL_NAMES) != EXPECTED_SKILL_COUNT:
        fail("readme-table", "found %d skill directories, expected %d. If the change was "
                             "intentional, update EXPECTED_SKILL_COUNT and the README prose."
             % (len(SKILL_NAMES), EXPECTED_SKILL_COUNT))
    out("  %d skill directories, %d README table rows, names match"
        % (len(SKILL_NAMES), len(rows)))


# --- check 4: every skill links the shared guardrails ---------------------

GUARDRAILS_REL = "../../GUARDRAILS.md"


def check_guardrails():
    # Count what actually passed. This line used to read len/len, which made it
    # print "21/21 skills link ... and it resolves" immediately before FAIL,
    # because the numerator was the loop's input rather than its result. A
    # detail line that cannot disagree with the verdict is worse than no detail
    # line: it is the failure mode this library's own guardrails call
    # "absence of evidence is not evidence of absence", printed by the checker
    # that exists to catch it.
    ok = 0
    for name in SKILL_NAMES:
        path = os.path.join(SKILLS_DIR, name, "SKILL.md")
        targets = [t for _l, t in LINK_RE.findall(read(path))]
        if GUARDRAILS_REL not in targets:
            fail("guardrails", "%s does not link %s (links: %s)"
                 % (rel(path), GUARDRAILS_REL, targets or "none"))
            continue
        dest = os.path.normpath(os.path.join(os.path.dirname(path), GUARDRAILS_REL))
        if not os.path.isfile(dest):
            fail("guardrails", "%s links %s but that path does not resolve from its location"
                 % (rel(path), GUARDRAILS_REL))
            continue
        ok += 1
    out("  %d/%d skills link %s and it resolves"
        % (ok, len(SKILL_NAMES), GUARDRAILS_REL))


# --- check 5: the section contract and its named exceptions --------------

FORGE = os.path.join(SKILLS_DIR, "skill-forge", "SKILL.md")
DECLARING_SKILL = os.path.basename(os.path.dirname(FORGE))
BACKTICKED_H2_RE = re.compile(r"`(##\s+[^`]+)`")


def contract_sections():
    """Read the contract out of /skill-forge rather than restating it here.

    skill-forge's 'Draft the skill file in the house contract' step names the
    required H2 headings, in order, in backticks. Those backticked mentions are
    the contract. If skill-forge is reworded, this check follows it.
    """
    found = [re.sub(r"\s+", " ", h).strip()
             for h in BACKTICKED_H2_RE.findall(strip_fences(read(FORGE)))]
    seen = []
    for h in found:
        if h not in seen:
            seen.append(h)
    return seen


def check_contract():
    contract = contract_sections()
    if len(contract) < 3:
        fail("contract", "could not read the section contract out of %s: found %s"
             % (rel(FORGE), contract))
        return
    out("  contract read from %s: %s" % (rel(FORGE), " -> ".join(contract)))

    contract_bad, no_block = set(), set()
    for name in SKILL_NAMES:
        text = read(os.path.join(SKILLS_DIR, name, "SKILL.md"))
        h2 = ["## " + t for _l, t in headings(text, level=2)]
        # Conforming means the H2 sequence is exactly the contract: same
        # headings, same order, nothing extra. Extra top-level sections are a
        # deviation too, since an aggregator walks these by name.
        if h2 != contract:
            contract_bad.add(name)
        if not output_block(text):
            no_block.add(name)

    for label, got, want, readme_key in (
        ("section contract", contract_bad, EXPECTED_CONTRACT_EXCEPTIONS,
         "do not follow the section contract"),
        ("machine-readable output block", no_block, EXPECTED_NO_OUTPUT_BLOCK,
         "machine-readable output block"),
    ):
        out("  %s exceptions: %s" % (label, ", ".join(sorted(got)) or "none"))
        if got != want:
            for name in sorted(got - want):
                fail("contract", "%s: '%s' deviates from the %s but the README does not "
                                 "list it as an exception" % (label, name, label))
            for name in sorted(want - got):
                fail("contract", "%s: README lists '%s' as an exception but it now conforms"
                     % (label, name))
        # Cross-check the README still names the same set, so the constants
        # above and the prose cannot drift apart independently.
        bullet = readme_bullet(readme_key)
        if bullet is None:
            fail("contract", "no README bullet mentions '%s'" % readme_key)
        else:
            named = {n for n in re.findall(r"`/?([a-z0-9][a-z0-9-]*)`", bullet)
                     if n in SKILL_NAMES}
            # The bullet cites the skill that declares the contract. That is a
            # reference, not an exception. Dropping it is safe: if the declaring
            # skill ever stopped conforming it would land in `got`, and the set
            # comparison above would fail on it.
            named -= {DECLARING_SKILL}
            if named != want:
                fail("contract", "README's '%s' bullet names %s, but this script expects %s"
                     % (readme_key, sorted(named), sorted(want)))


def output_block(text):
    """True if '## Output Format' holds a closed fenced template with [slots].

    skill-forge calls this the highest-leverage convention in the library: a
    fenced literal template with bracketed slots, so an umbrella skill can diff
    a child's output run over run. Both halves are required. An unclosed fence
    is not a template, and a fence with no slots is not fillable, so neither
    counts. Prose describing the output shape does not count either.
    """
    section = output_format_section(text)
    if section is None:
        return False
    fence_open = None
    for line in section.splitlines():
        if FENCE_RE.match(line):
            if fence_open is None:
                fence_open = []
            else:
                if re.search(r"\[[^\]\n]+\]", "\n".join(fence_open)):
                    return True
                fence_open = None
        elif fence_open is not None:
            fence_open.append(line)
    return False


def output_format_section(text):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Output Format":
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    in_fence = False
    for k in range(start + 1, len(lines)):
        if FENCE_RE.match(lines[k]):
            in_fence = not in_fence
        elif lines[k].startswith("## ") and not in_fence:
            end = k
            break
    return "\n".join(lines[start + 1:end])


def readme_bullet(needle):
    """The README list item containing needle, joined across its wrapped lines."""
    items = []
    current = None
    for line in read(README).splitlines():
        if re.match(r"^\s*[-*]\s", line):
            if current is not None:
                items.append(" ".join(current))
            current = [line.strip()]
        elif current is not None and line.strip():
            current.append(line.strip())
        elif current is not None:
            items.append(" ".join(current))
            current = None
    if current is not None:
        items.append(" ".join(current))
    for item in items:
        if needle in item:
            return item
    return None


# --- check 6: the no-em-dash house rule ----------------------------------

def check_typography():
    em = []
    smart = []
    for path in ALL_FILES:
        try:
            text = read(path)
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable: no prose to police
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            if EM_DASH in line:
                em.append((path, i, line.strip()))
            for ch, label in SMART_QUOTES.items():
                if ch in line:
                    smart.append((path, i, label, line.strip()))
    for path, line_no, _text in em:
        if rel(path) != EM_DASH_ALLOWED_IN:
            fail("typography", "em dash at %s:%d. The only allowed one is the "
                               "counter-example in %s." % (rel(path), line_no, EM_DASH_ALLOWED_IN))
    if len(em) == 1:
        out("  1 em dash, at %s:%d (the house-style counter-example)" % (rel(em[0][0]), em[0][1]))
    else:
        out("  %d em dashes found" % len(em))
        if len(em) > 1 and all(rel(p) == EM_DASH_ALLOWED_IN for p, _i, _t in em):
            fail("typography", "%d em dashes in %s; the rule's example needs exactly one"
                 % (len(em), EM_DASH_ALLOWED_IN))
        elif not em:
            fail("typography", "no em dash anywhere. %s should still contain the one "
                               "counter-example that demonstrates the rule." % EM_DASH_ALLOWED_IN)
    for path, line_no, label, _text in smart:
        fail("typography", "smart quote (%s) at %s:%d, use a straight quote"
             % (label, rel(path), line_no))
    out("  %d smart quotes" % len(smart))


# --- check 7: secrets and tenant identifiers -----------------------------

# Deliberately narrow. Several skills in this library are ABOUT leak scanning,
# so the repo is full of the words "secret", "token", "credential" and
# "password" in prose. A pattern that matched those would fire on every run and
# get switched off, which is worse than not having it. So every pattern below
# needs structure a sentence does not have: an assignment operator followed by a
# long opaque value, a ticket key with digits, a real host, or an absolute path.
#
# WHAT THIS CATCHES: key=value / key: value credential assignments with a
# >=16-char opaque value; JWTs; AWS access key ids; PEM private key headers;
# ticket keys for the configured project prefixes; *.atlassian.net hosts other than the
# example.* placeholder; C:\Users\, /home/, /Users/ absolute paths.
#
# WHAT IT DOES NOT CATCH, and cannot without crying wolf: a secret pasted as a
# bare value with no key next to it (a lone hex or base64 blob is
# indistinguishable from a hash or an example); an internal hostname that is not
# under atlassian.net; employee or customer names; a real customfield id quoted
# in prose (the README quotes one on purpose, as an anti-example); a credential
# inside an image.
#
# AND THIS FILE. check_secrets skips check.py, because the patterns above would
# each report themselves. That exclusion is necessary and it is also the one
# blind spot in the repo, so it is worth saying out loud: this file is the only
# place a tenant identifier can sit and still let the check print PASS. It has
# happened. Three real ticket keys were hardcoded here, in the check that hunts
# for ticket keys, and check 7 passed the whole time. They are configuration now.
# Read this file by eye; the scan will not do it for you.
#
# Passing check 7 means no obvious assigned value or tenant id
# is present. It does not mean the repo has been cleared for publication by a
# human, and /leak-scan exists because that read is still required.

CRED_KEY = (r"(?:api[_-]?key|apikey|secret|client[_-]?secret|password|passwd|pwd|"
            r"auth[_-]?token|access[_-]?token|bearer|private[_-]?key|access[_-]?key)")
CRED_ASSIGN_RE = re.compile(
    CRED_KEY + r"\s*[:=]\s*[\"']?([A-Za-z0-9+/=_.\-]{16,})[\"']?", re.I)
PLACEHOLDER_RE = re.compile(
    r"^(?:your|my|the|<|\$|\{|example|changeme|placeholder|redacted|xxx+|\.\.\.|todo|fill)",
    re.I)
# Project keys are tenant identifiers, so they are configured rather than baked
# in. This line used to hardcode three real ones, which put the exact class of
# string the check looks for into the checker that looks for it. Same reasoning
# as the custom field ids in the README: yours will differ.
TICKET_PREFIXES = [p.strip() for p in
                   os.environ.get("DOC_SKILLS_TICKET_PREFIXES", "PROJ,OPS,TMPL").split(",")
                   if p.strip()]
# An empty list would compile to `\b(?:)-\d+\b`, which matches nothing while
# looking like it works. Degrade and say so instead, per GUARDRAILS.md.
TICKET_RE = re.compile(
    r"\b(?:%s)-\d+\b" % "|".join(re.escape(p) for p in TICKET_PREFIXES),
    re.I) if TICKET_PREFIXES else None
ATLASSIAN_RE = re.compile(r"\b([A-Za-z0-9][A-Za-z0-9-]*)\.atlassian\.net\b", re.I)
ABS_PATH_RE = re.compile(r"(?:[A-Za-z]:\\Users\\|/home/[A-Za-z0-9._-]+|/Users/[A-Za-z0-9._-]+)")
HIGH_CONFIDENCE_RE = re.compile(
    r"(?:eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"          # JWT
    r"|AKIA[0-9A-Z]{16}"                                      # AWS access key id
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----)")                  # PEM private key


def check_secrets():
    hits = 0
    scanned = 0
    for path in ALL_FILES:
        if rel(path) == "check.py":
            continue  # the patterns themselves are not findings
        try:
            text = read(path)
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        for i, line in enumerate(text.splitlines(), start=1):
            where = "%s:%d" % (rel(path), i)
            for m in CRED_ASSIGN_RE.finditer(line):
                value = m.group(1)
                if PLACEHOLDER_RE.match(value) or "example" in value.lower():
                    continue
                hits += 1
                fail("secrets", "%s: looks like an assigned credential value: %s"
                     % (where, m.group(0)[:70]))
            for m in HIGH_CONFIDENCE_RE.finditer(line):
                hits += 1
                fail("secrets", "%s: %s" % (where, m.group(0)[:40]))
            if TICKET_RE is not None:
                for m in TICKET_RE.finditer(line):
                    hits += 1
                    fail("secrets", "%s: internal ticket key %s" % (where, m.group(0)))
            for m in ATLASSIAN_RE.finditer(line):
                if m.group(1).lower() == "example":
                    continue
                hits += 1
                fail("secrets", "%s: tenant host %s" % (where, m.group(0)))
            for m in ABS_PATH_RE.finditer(line):
                hits += 1
                fail("secrets", "%s: absolute local path %s" % (where, m.group(0)))
    # Name the ticket-key configuration in the output. A check that silently did
    # not run reads exactly like a check that passed, which is the failure mode
    # GUARDRAILS.md calls "absence of evidence is not evidence of absence".
    if TICKET_PREFIXES:
        out("  ticket-key prefixes scanned: %s (set DOC_SKILLS_TICKET_PREFIXES "
            "to yours)" % ",".join(TICKET_PREFIXES))
    else:
        out("  ticket-key scan SKIPPED: DOC_SKILLS_TICKET_PREFIXES is empty")
    out("  %d files scanned, %d findings (narrow patterns; see the comment in check.py "
        "for what this does not catch)" % (scanned, hits))


# --- runner ---------------------------------------------------------------

CHECKS = [
    ("links", "every markdown link resolves", check_links),
    ("frontmatter", "every SKILL.md has valid contract frontmatter", check_frontmatter),
    ("readme-table", "skill directories match the README table", check_readme_table),
    ("guardrails", "every skill links the shared GUARDRAILS.md", check_guardrails),
    ("contract", "section contract and its named exceptions", check_contract),
    ("typography", "the no-em-dash house rule", check_typography),
    ("secrets", "no secrets or tenant identifiers", check_secrets),
]


def main():
    out("doc-skills-library structural check")
    out("repo: %s" % ROOT)
    out()
    for n, (key, title, fn) in enumerate(CHECKS, start=1):
        before = len(failures)
        out("[%d/%d] %s" % (n, len(CHECKS), title))
        fn()
        out("  %s" % ("PASS" if len(failures) == before else "FAIL"))
        out()
    if not failures:
        out("All %d checks passed." % len(CHECKS))
        out("Structural only. This says nothing about whether a skill produces good output.")
        return 0
    out("%d failure(s):" % len(failures))
    for key, message in failures:
        out("  [%s] %s" % (key, message))
    out()
    out("FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
