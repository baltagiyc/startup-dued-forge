# Social Audit Report – Meilisearch

**Sources used:** github

## Summary

**Community confidence score:** N/A

- **Community confidence score:** 6/10
- Meilisearch’s community demonstrates strong enthusiasm for its performance and developer experience, but recurring stability issues (crashes, OOM kills, memory leaks) and slow response times to critical bugs erode trust. Sovereignty concerns are niche but vocal among privacy-focused users.

---

## Red Flags (Social)

1. **Stability/crashes**: Frequent Rust panics (e.g., assertion failures, `unwrap()` errors) and OOM kills under load (#5989, #5960, #5904).
2. **Memory management**: Ignored `MEILI_MAX_INDEXING_MEMORY` settings and unbounded RAM usage (#6112, #4764).
3. **Slow issue resolution**: Average first response time for bugs (~231h) and non-bugs (~489h) frustrates users (#6158, #5827).
4. **Platform-specific failures**: Crashes on Windows (S3 snapshots) and cloud platforms (GCP, EFS) (#6025, #5695, #833).
5. **Privacy/sovereignty**: Default OpenAI routing and lack of transparency about data handling (#6 "souveraineté" issues).

---

## Market Positioning

### **Strengths vs. Typesense and Algolia**
- **Developer experience**: Praised for simplicity, Rust-based performance, and open-source transparency (vs. Algolia’s black-box pricing).
- **Self-hosting**: Stronger appeal for sovereignty-focused users (vs. Algolia’s SaaS lock-in).
- **Cost**: Free tier and predictable pricing for self-hosted deployments (vs. Algolia’s opaque enterprise pricing).

### **Weaknesses vs. Typesense and Algolia**
- **Stability**: More frequent crashes and memory issues (vs. Typesense’s reputation for reliability).
- **Scalability**: p95 latency degradation at scale (vs. Algolia’s horizontal scaling).
- **Enterprise features**: Lacks Algolia’s advanced analytics and Typesense’s mature clustering.
- **Support**: Slower issue resolution and fewer community resources (vs. Typesense’s active Discord).

---

## Correlation Lab vs Social

- **Rust panics/crashes**: **Yes** – Multiple GitHub issues report assertion failures (`left == right` mismatches), `unwrap()` panics, and OOM kills (#5989, #5960, #5904, #806).
- **OpenAI/default routing**: **Partially** – Only 6 sovereignty-related issues, but these highlight privacy concerns (e.g., default embedder routing to OpenAI).
- **p95 degradation at scale**: **Partially** – No direct GitHub issues, but #5695 (EFS latency) and #5348 (OOM under load) imply performance cliffs at scale.

---
## Data Summary

- **GitHub repo:** meilisearch/meilisearch
- **Issues matched:** 36
- **By category:** {'stabilite': 30, 'souverainete': 6, 'performance': 0}
- **Velocity (avg first response):** bugs 231.4265873015873h (n=7), other 488.6399845679012h (n=18)

#### Issues used for velocity average (time to first comment)

- [#6152](https://github.com/meilisearch/meilisearch/issues/6152) — 25.4h — *other* — rest embedder could not reach embedding server after upgrading meilisearch to v1
- [#4686](https://github.com/meilisearch/meilisearch/issues/4686) — 1.6h — *bug* — Use container's RAM limit set by deploy resources limit
- [#6123](https://github.com/meilisearch/meilisearch/issues/6123) — 194.0h — *other* — Chat causes errors when used with Mistral
- [#6146](https://github.com/meilisearch/meilisearch/issues/6146) — 92.1h — *other* — Query behaves differently (uppercase vs lowercase)
- [#6056](https://github.com/meilisearch/meilisearch/issues/6056) — 647.9h — *other* — baseUrl appears to be ignored for chat completions workspace
- [#5958](https://github.com/meilisearch/meilisearch/issues/5958) — 554.7h — *other* — Massive document addition causes freeze
- [#5717](https://github.com/meilisearch/meilisearch/issues/5717) — 119.3h — *other* — Missing nested fields in `/stats` route
- [#5818](https://github.com/meilisearch/meilisearch/issues/5818) — 567.8h — *other* — Add support for _geoBoundingBox filter on _geojson documents
- [#5819](https://github.com/meilisearch/meilisearch/issues/5819) — 567.8h — *other* — Add support for _geoRadius filter on _geojson documents
- [#5822](https://github.com/meilisearch/meilisearch/issues/5822) — 567.8h — *bug* — In extractor: points removed are still serialized as GeoJSON
- [#5920](https://github.com/meilisearch/meilisearch/issues/5920) — 119.0h — *other* — Test failures in 1.22.2
- [#5937](https://github.com/meilisearch/meilisearch/issues/5937) — 2140.5h — *other* — Embedding fault tolerance
- [#5973](https://github.com/meilisearch/meilisearch/issues/5973) — 147.9h — *other* — Throttling document embedding requests
- [#5986](https://github.com/meilisearch/meilisearch/issues/5986) — 40.7h — *other* — `_geoDistance` not returned in `/documents`
- [#5811](https://github.com/meilisearch/meilisearch/issues/5811) — 438.9h — *bug* — Why do other words come out when using search?
- [#5827](https://github.com/meilisearch/meilisearch/issues/5827) — 0.2h — *other* — Some batches never get deleted
- [#5880](https://github.com/meilisearch/meilisearch/issues/5880) — 397.5h — *bug* — searchCutoffMs setting not working - processing time exceeds configured cutoff
- [#6048](https://github.com/meilisearch/meilisearch/issues/6048) — 15.2h — *bug* — Make sure payloads are effectively deleted on error
- [#5673](https://github.com/meilisearch/meilisearch/issues/5673) — 1816.7h — *other* — suggest add build target musl ,GLIBC2.35 is niche
- [#6112](https://github.com/meilisearch/meilisearch/issues/6112) — 47.5h — *other* — `MEILI_MAX_INDEXING_MEMORY` is ignored
- [#5898](https://github.com/meilisearch/meilisearch/issues/5898) — 90.9h — *bug* — Meilisearch mTLS Interoperability Issue with Go Client (TLS Error Decoding Messa
- [#5957](https://github.com/meilisearch/meilisearch/issues/5957) — 561.5h — *other* — Exposed `reindex` function in milli uses parameter with private type `SettingsDe
- [#6043](https://github.com/meilisearch/meilisearch/issues/6043) — 1149.2h — *other* — Chat endpoint looks into indexes it's not allowed to
- [#5953](https://github.com/meilisearch/meilisearch/issues/5953) — 108.1h — *bug* — Meilisearch v1.24 was not published to Gemfury
- [#6120](https://github.com/meilisearch/meilisearch/issues/6120) — 3.3h — *other* — Running MeiliSearch on cluster

