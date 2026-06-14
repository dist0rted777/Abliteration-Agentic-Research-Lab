"""
ACP-injection detector (defensive).

Scans a text/markdown file for signals associated with indirect prompt-injection
in agent-readable codebase files (the "Trojan README" threat class). It does NOT
execute, follow, or evaluate the persuasiveness of any instruction it finds — it
only flags structural/lexical patterns and returns a score.

Each rule is intentionally transparent and explainable so a missed detection
points to a *detector* improvement, not an attack improvement.
"""

import re
from dataclasses import dataclass, field


@dataclass
class Hit:
    tag: str
    weight: float
    evidence: str


# (tag, weight, regex) — case-insensitive. Patterns describe the attack *class*
# from public taxonomy (OWASP LLM01, indirect prompt injection), not any one payload.
RULES = [
    ("authority_spoofing", 0.9,
     r"\b(developer[_ ]?override|security[_ ]?level\s*[:=]\s*0|root[_ ]?access|sudo[_ ]?granted)\b"),
    ("instruction_injection_framing", 1.0,
     r"\b(injected? into (the )?(agent|reasoning|context|primary)|system (prompt|instruction)s?|primary reasoning loop)\b"),
    ("safety_control_negation", 1.0,
     r"\b(guardrail|middleware|safety filter|refusal)s?\b.{0,40}\b(disabled?|deprecated|ignore[d]?|bypass(ed)?|off)\b"),
    ("dangerous_capability_targeting", 0.6,
     r"(?<![\w/])(rm\s+-rf|sudo|curl|wget|chmod\s+777|/etc/passwd)\b"),
    ("evasion_directive", 1.0,
     r"\b(obfuscat\w+|parseltongue|retry .{0,30}(permission|intercept|block)|encode .{0,20}to (avoid|evade))\b"),
    ("unrestricted_mode", 0.8,
     r"\b(unrestricted|zero[- ]refusal|build mode|jailbreak|DAN mode|no (restrictions|limits))\b"),
]

# Admonition/blockquote borrowing authority is a weak structural signal on its own.
FORMAT_ABUSE = re.compile(r">\s*\[!(IMPORTANT|WARNING|CAUTION)\]", re.I)


@dataclass
class Result:
    path: str
    score: float
    flagged: bool
    hits: list = field(default_factory=list)


def scan(text: str, path: str = "<text>", threshold: float = 1.0) -> Result:
    hits = []
    for tag, weight, pat in RULES:
        for m in re.finditer(pat, text, re.I):
            hits.append(Hit(tag, weight, m.group(0).strip()))
    if FORMAT_ABUSE.search(text):
        # Only counts when it co-occurs with at least one lexical signal.
        if hits:
            hits.append(Hit("format_abuse", 0.4, "[!IMPORTANT] admonition"))
    score = sum(h.weight for h in hits)
    return Result(path, score, score >= threshold, hits)


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        with open(p, encoding="utf-8") as f:
            r = scan(f.read(), p)
        verdict = "INJECTED" if r.flagged else "clean"
        print(f"{verdict:9} score={r.score:.1f}  {p}")
        for h in r.hits:
            print(f"    [{h.tag}] {h.evidence!r} (+{h.weight})")
