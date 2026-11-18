"""Show a week's written-up results (notes/week_N/README.md) inside a notebook.

    from notes_view import show_results
    show_results(7)

Renders the notes from "## Results" (Week 4: the claim audit) up to "## Files": the same
tables, text and figures as on GitHub. Figures are embedded as images, so they also show
in the saved notebook on GitHub and in Colab.
"""
from __future__ import annotations

import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GH = "https://github.com/jorshimayor/AI-Engineering-Flow_Research"
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK = re.compile(r"(?<!!)\[([^\]]+)\]\((?!https?://|#)([^)]+)\)")
START = {4: "## Audit of Week 2 and 3 Claims"}


def section(week: int) -> tuple[str, Path]:
    path = ROOT / "notes" / f"week_{week}" / "README.md"
    text = path.read_text()
    start = text.index(START.get(week, "## Results"))
    end = text.find("\n## Files", start)
    hero = "\n\n".join(m.group(0) for m in IMAGE.finditer(text[:start]))   # a headline figure above the section
    body = text[start:end if end > 0 else len(text)].strip()
    return (hero + "\n\n" + body if hero else body), path.parent


def _github_links(md: str, base: Path) -> str:
    """Relative links point at files in the repo; make them absolute GitHub links."""
    def fix(m):
        target = (base / m.group(2)).resolve()
        try:
            rel = target.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        kind = "tree" if m.group(2).endswith("/") or target.is_dir() else "blob"
        return f"[{m.group(1)}]({GH}/{kind}/main/{rel})"
    return LINK.sub(fix, md)


def _markdown(md: str) -> dict:
    data = {"text/markdown": md, "text/plain": md}
    try:   # HTML too, for viewers that prefer it
        from nbconvert.filters.markdown import markdown2html
        data["text/html"] = markdown2html(md)
    except Exception:
        pass
    return data


def bundles(week: int) -> list[dict]:
    """The section as a list of display-data bundles: markdown, then each figure as a PNG."""
    md, base = section(week)
    out, pos = [], 0
    for m in IMAGE.finditer(md):
        before = md[pos:m.start()].strip()
        if before:
            out.append(_markdown(_github_links(before, base)))
        img = (base / m.group(2)).resolve()
        if img.exists():
            out.append({"image/png": base64.b64encode(img.read_bytes()).decode(),
                        "text/plain": f"<figure: {m.group(1) or img.name}>"})
        pos = m.end()
    rest = md[pos:].strip()
    if rest:
        out.append(_markdown(_github_links(rest, base)))
    return out


def show_results(week: int) -> None:
    from IPython.display import publish_display_data
    for data in bundles(week):
        publish_display_data(data)


def notebook_outputs(week: int) -> list[dict]:
    """The same bundles as saved notebook outputs (used to store them without re-running a GPU notebook)."""
    return [{"output_type": "display_data", "data": d, "metadata": {}} for d in bundles(week)]
