# Source Repositories (Audit Trail)

This folder preserves the **29 open-source repositories** that were cloned,
audited, and merged to build the `deep-research/` and `deep-analysis/` skills
in this same repo. Each folder is named `author__repo` and is a snapshot
clone (`--depth 1`, taken 2025-10-19) with the upstream `.git` directory
removed. They are kept here for reference, provenance, and re-verification.

> **Repo layout (single `main` branch):** the final skills live in
> `deep-research/` and `deep-analysis/`; this `sources/` folder is the
> raw audit trail of everything that was studied and merged.

## Provenance & Licensing

Full details: see `docs/capability-matrix.md` and `ATTRIBUTION.md` at the repo root.

| Folder | Upstream | License note |
|---|---|---|
| Weizhena__deep-research-skills | github.com/Weizhena/deep-research-skills | MIT-declared, no file |
| jojocorse2b__deep-research-skill | github.com/jojocorse2b/deep-research-skill | verify upstream |
| B143KC47__deep-research-skill | github.com/B143KC47/deep-research-skill | verify upstream |
| hec-ovi__research-skill | github.com/hec-ovi/research-skill | MIT |
| TheAdamLabs__deep-research-skill | github.com/TheAdamLabs/deep-research-skill | MIT-declared, no file |
| doryashar__deep-research-skill | github.com/doryashar/deep-research-skill | MIT |
| alirezakarimi82__Deep-Research | github.com/alirezakarimi82/Deep-Research | NO LICENSE |
| zy839971925-zyy__Agent--deep-research-Workflow-Skills | github.com/zy839971925-zyy/Agent--deep-research-Workflow-Skills | verify upstream |
| 199-biotechnologies__claude-deep-research-skill | github.com/199-biotechnologies/claude-deep-research-skill | MIT-declared, no file |
| nraford7__deep-research | github.com/nraford7/deep-research | verify upstream |
| comeonvictor__claude-code-deep-research | github.com/comeonvictor/claude-code-deep-research | verify upstream |
| robertnowell__deep-research | github.com/robertnowell/deep-research | verify upstream |
| hashbulla__deep-research | github.com/hashbulla/deep-research | verify upstream |
| ramit-mitra__deep-research-skill | github.com/ramit-mitra/deep-research-skill | verify upstream |
| cyberelf__agent_skills | github.com/cyberelf/agent_skills | verify upstream |
| Silence-view__deep-research | github.com/Silence-view/deep-research | verify upstream |
| bntvllnt__agent-skills | github.com/bntvllnt/agent-skills | verify upstream |
| dzhng__deep-research | github.com/dzhng/deep-research | MIT |
| assafelovic__gpt-researcher | github.com/assafelovic/gpt-researcher | Apache-2.0 |
| bytedance__deer-flow | github.com/bytedance/deer-flow | MIT (check upstream for updates) |
| SkyworkAI__DeepResearchAgent | github.com/SkyworkAI/DeepResearchAgent | verify upstream |
| MiroMindAI__MiroThinker | github.com/MiroMindAI/MiroThinker | Apache-2.0 |
| mvanhorn__last30days-skill | github.com/mvanhorn/last30days-skill | MIT |
| HughYau__AcademicForge | github.com/HughYau/AcademicForge | NOASSERTION |
| Imbad0202__academic-research-skills | github.com/Imbad0202/academic-research-skills | CC BY-NC 4.0 |
| Leonxlnx__unlazy | github.com/Leonxlnx/unlazy | verify upstream |
| chaseai-yt__claudex-loop | github.com/chaseai-yt/claudex-loop | NOASSERTION |
| wanshuiyin__Auto-claude-code-research-in-sleep | github.com/wanshuiyin/Auto-claude-code-research-in-sleep | verify upstream |
| zLanqing__codex-claude-academic-skills | github.com/zLanqing/codex-claude-academic-skills | verify upstream |

Plus `discovery_candidates.json` — the inventory of 141 additional candidates
found via GitHub-wide discovery search (audit trail only; not cloned).

## License Caveat

These are third-party snapshots, redistributed here for private study and
provenance. The repositories marked *NO LICENSE*, *NOASSERTION*, or
*verify upstream* do not carry an explicit redistribution license — the
final skills on `main` reuse ideas from those only, not code (see
`docs/capability-matrix.md`). For any public redistribution of this branch,
respect each upstream's license and remove unlicensed snapshots first.
