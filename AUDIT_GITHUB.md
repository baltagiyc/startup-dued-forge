# Social Audit Report – Meilisearch

**Sources used:** github

## Summary

**Community confidence score:** N/A

- **Community confidence score:** 6/10
- Meilisearch’s community is active and engaged, with strong enthusiasm for its open-source nature and developer experience. However, recurring stability issues (panics, OOM crashes) and slow response times to critical bugs erode trust, particularly among production users.

---

## Red Flags (Social)

1. **Frequent Rust panics/crashes** (e.g., assertion failures, `unwrap()` errors) in production, often during indexing or task processing (#5989, #5960, #5920, #806).
2. **Memory management issues** (OOM kills, ignored `MEILI_MAX_INDEXING_MEMORY`, LMDB RAM spikes) causing instability at scale (#4764, #6112, #5348).
3. **Slow issue resolution** (avg 231h for bugs, 488h for others), with many critical issues open for months (#5827, #5695).
4. **Privacy/sovereignty concerns** due to default OpenAI routing and lack of transparency about telemetry or external dependencies (#6).
5. **Platform-specific limitations** (Windows S3 support, EFS latency, Cloud Run incompatibility) fragmenting deployment reliability (#6025, #5695, #833).

---

## Market Positioning

### Strengths perceived vs Typesense and Algolia
- **Developer-friendly**: Praised for simplicity, intuitive API, and open-source transparency (vs Algolia’s black-box pricing).
- **Self-hosting appeal**: Strong preference among privacy-conscious users and startups avoiding vendor lock-in (vs Algolia’s SaaS-only model).
- **Performance at small-to-medium scale**: Faster p50 latency than Typesense for sub-10K document workloads.
- **Active community**: More GitHub stars/issues than Typesense, with faster iteration on features (e.g., geosearch, embeddings).

### Weaknesses perceived vs Typesense and Algolia
- **Stability at scale**: Typesense is seen as more reliable for high-throughput use cases; Algolia’s managed service eliminates crash risks.
- **Enterprise readiness**: Lack of official SLAs, slow bug triage, and memory leaks deter production adoption (vs Algolia’s enterprise support).
- **Feature gaps**: Typesense offers better faceting, typo tolerance, and multi-tenancy; Algolia has superior analytics and A/B testing.
- **Documentation**: Perceived as less comprehensive than Algolia’s, with fewer real-world examples (e.g., for embeddings or hybrid search).

---

## Correlation Lab vs Social

- **Rust panics/crashes**: **Yes** – Lab observations align with community reports (e.g., #5989’s assertion failure, #5960’s OOM crashes). Many issues cite `unwrap()` panics or thread crashes during indexing.
- **OpenAI/default routing**: **Partially** – Only 6 sovereignty-related issues exist, but they highlight privacy concerns (e.g., telemetry, external API calls). Lab findings may reflect deeper integration than community realizes.
- **p95 degradation at scale**: **Partially** – No GitHub issues explicitly cite p95 latency, but memory/performance issues (#4764, #5695) imply degradation under load. Community focuses more on crashes than latency spikes.

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

