# Install and configure

Back to the [skill list](../README.md).

Claude Code is the terminal agent that loads a skill when you type `/name`. You also need a checkout of this repo. You do not need to edit the skills to run them. You do need to point them at your corpus before the audit skills have anything to read.

The files stand alone as procedures. Open `skills/<name>/SKILL.md` and follow the steps in the file. The severity labels and the report template are part of the skill. The slash command is one way to run them.

The pass order, and how to read a verdict, are in [Using the skills](using.md).

## Install

Skills live in a `skills/` directory Claude Code reads. Copy the ones you want, and copy the shared guardrails file and the `references/` directory with them:

```bash
git clone https://github.com/pinklightultra/doc-skills-library
cd doc-skills-library
mkdir -p ~/.claude/skills             # cp fails, or silently mis-copies, without this
cp -r skills/leak-scan ~/.claude/skills/
cp GUARDRAILS.md ~/.claude/           # every skill links ../../GUARDRAILS.md
cp -r references ~/.claude/           # cited by 9 of the 21
```

To install the set, replace the single-skill copy with `cp -r skills/* ~/.claude/skills/`. Pulling this repo later does not update `~/.claude`. Copy again after an update.

The `mkdir` is required. If `~/.claude/skills/` does not exist, `cp -r` either fails outright or, when `~/.claude/` exists and `skills/` does not, exits 0 and copies the *contents* of the skill directory to `~/.claude/skills/SKILL.md`. The skill is then uninstalled, with no error and no directory named after it.

Do not skip the last two copies. All 21 skills inherit their safety rules by linking `../../GUARDRAILS.md` rather than restating them. From `~/.claude/skills/leak-scan/` that path resolves to `~/.claude/GUARDRAILS.md`. A missing file leaves a dangling link: nothing errors, and the skill runs without the five rules, including the two that keep it read-only. `GUARDRAILS.md` and `references/` sit one level above `skills/`, beside it. `~/.claude/skills/GUARDRAILS.md` is the wrong place, and it is wrong silently.

The same shape applies wherever you install. The skill file has to land at `<root>/skills/<name>/SKILL.md`, with `GUARDRAILS.md` and `references/` at `<root>/`. For the commands above, `<root>` is `~/.claude`.

## Configure

```bash
cp config.example.yml config.yml   # config.yml is gitignored
```

Fill in `config.yml` before running a corpus skill. Skills reference config keys by name. An unconfigured library stops and tells you, or it produces a report full of gaps. It will not invent the values.

The keys a documentation set actually needs on day one:

- `docs.corpus_root`: a local checkout or an export of the knowledge base. The example value is `./corpus`.
- `docs.search_command`: literal search. The default is `grep`, because it is present everywhere.
- `docs.reader_url_template`: the URL a reader would open, so citations are not authoring links.
- `docs.audience_model` and `docs.audience_field`: how this stack decides who can read an article. Set this wrong and `/audience-lens` will recommend a control you do not have. See [The audience-gating problem](limits.md#the-audience-gating-problem).
- `issue_tracker`: base URL, project keys, and the support-volume query, if you want gap lists ordered by what readers already asked.

`config.example.yml` comments every key. Two of those comments point at [What is missing](limits.md#what-is-missing) and [The audience-gating problem](limits.md#the-audience-gating-problem).

Do not point `docs.corpus_root` at this repo's `docs/` directory. Those files are these pages. `check.py` scans flat markdown there and skips subdirectories, `corpus/`, and `reports/`. `corpus/` is gitignored. If a previous config used `./docs`, move the export. A flat markdown file dropped beside these pages is scanned with the rest of the library.
