# Policy: redaction in screenshots and captured output

Screenshots are the leakiest artifact in a documentation pipeline. Text gets
reviewed; images get pasted.

**Redact before capture, not after.** Apply the overlay or replacement in the
page itself (a DOM overlay, a seeded test dataset) and then take the picture. A
crop or a blur applied afterward leaves the original in the file's history, in
the editor's undo buffer, or in the uncropped copy someone kept.

**Scope.** Treat as redactable any direct identifier attached to a person or an
account: names, member and subscriber identifiers, dates more specific than a
year where they attach to a person, addresses below state level, phone numbers,
email addresses, record and account numbers, and any free-text note field, which
is where identifiers hide in practice. Where a formal standard governs your
domain, use its identifier list as the floor rather than your own judgment.

**Verify the redaction against the real UI.** An overlay positioned by
coordinates drifts when the layout changes, and a menu rendered in a portal or
shadow root may not be covered at all. After capturing, look at the image and
confirm every intended target is actually obscured. Also confirm you did not
obscure the thing the screenshot exists to show.

**Never capture an authentication surface.** Login pages, token dialogs, and
credential managers get autofilled by the browser, and an accessibility snapshot
of an autofilled form serializes the password as text even when the pixels show
dots.
