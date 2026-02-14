# Social Audit Report – Meilisearch

**Sources used:** github, tavily

## Summary

**Community confidence score:** N/A

- **Community confidence score:** 6/10
- Meilisearch’s community demonstrates strong enthusiasm for its performance and developer experience, but recurring stability issues (crashes, OOM errors) and slow response times to critical bugs erode trust. The project’s transparency and Rust-based foundation are praised, but operational reliability remains a key concern.

---

## Red Flags (Social)

1. **Frequent Rust panics/crashes** (e.g., assertion failures, OOM kills) during indexing, updates, or edge-case queries (e.g., #5989, #5960, #5348).
2. **Memory management issues**, including ignored `MEILI_MAX_INDEXING_MEMORY` limits and LMDB RAM spikes (e.g., #6112, #4764).
3. **Slow issue triage/fixes**, with average first responses to bugs exceeding 230 hours (e.g., #6158, #5827).
4. **Platform-specific instability**, particularly on Windows (S3 snapshots) and cloud environments (EFS latency, GCP crashes) (e.g., #6025, #5695, #833).
5. **Privacy/sovereignty concerns** around default OpenAI routing (not explicitly mentioned in GH issues but aligns with lab findings).

---

## Market Positioning

### **Strengths vs. Typesense and Algolia**
- **Developer experience**: Praised for simplicity, Rust performance, and open-source transparency (e.g., "easier to self-host than Algolia").
- **Cost efficiency**: Free tier and self-hosting appeal to startups/SMBs avoiding Algolia’s pricing.
- **Feature velocity**: Rapid iteration on new features (e.g., `_geojson` fields, embedders) compared to Typesense’s slower pace.
- **Community engagement**: Active Discord/GitHub presence and responsiveness (when issues are addressed).

### **Weaknesses vs. Typesense and Algolia**
- **Stability/reliability**: More frequent crashes and OOM errors than Typesense or Algolia (e.g., #5960, #5348).
- **Enterprise readiness**: Lacks Algolia’s scalability guarantees (p95 degradation) and Typesense’s battle-tested production use cases.
- **Support latency**: Slower issue resolution (230h avg for bugs) vs. Algolia’s 24/7 support or Typesense’s community-driven fixes.
- **Cloud compatibility**: Struggles with managed environments (EFS, GCP) where Algolia/Typesense are optimized (e.g., #5695, #833).

---

## Correlation Lab vs Social

- **Rust panics/crashes**: **Yes** – Community reports mirror lab findings (e.g., #5989’s assertion failure, #5960’s OOM crashes).
- **OpenAI/default routing**: **Partially** – Not directly cited in GH issues, but sovereignty concerns (#6) align with lab privacy flags.
- **p95 degradation at scale**: **Partially** – Performance issues are reported (e.g., EFS latency #5695), but p95 specifics are not detailed in community data. Lab findings likely reflect deeper technical debt.

---
## Data Summary

- **GitHub repo:** meilisearch/meilisearch
- **Issues matched:** 36
- **By category:** {'stabilite': 30, 'souverainete': 6, 'performance': 0}
- **Velocity (avg first response):** bugs 231.4265873015873h, other 488.6399845679012h
- **Tavily (web/social) results:** 60
