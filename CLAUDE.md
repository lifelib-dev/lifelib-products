# Notes for Claude Code sessions

## Input files name no company or product

No input file may name an individual company or product. Input files are every CSV beside a
model under `lifelib/libraries/<lib>/products/<product>/`, model point tables included, and
the rule covers every column: `provenance` text, lookup keys and ids, and labels.

- **Companies**: insurers, reinsurers, banks, brokers and any other firm, by legal name,
  brand or abbreviation (`Allianz`, `AXA`, `흥국생명`, `MEDICPROOF`).
- **Products**: product and product-line names, riders, share classes and option names
  (`Shield 10`, `Series ADV`, `Flex GMWB Single Core`, `온라인정기보험`).

Cite and describe instead:

- A `provenance` cell cites its source by key (`[S5]`, `[S4 Annexe I]`, `[R29]`,
  `[REG-R18]`). Where it needs to say more, it describes the source generically: "one
  carrier", "the anchor carrier", "a second carrier", "a group contract", or the document
  type ("published tariff", "rate sheet", "상품요약서").
- A lookup key describes its row by source key or by design, never by company:
  `s14_50_viager`, `s3_2019`, `simple`.

The names belong in `sources.md`, which is the citation record. The `_research/` notes are the
raw provenance record and are not edited to remove them. Public bodies are not companies for
this rule: regulators, statistics offices and actuarial or industry associations (NAIC, SOA,
DAV, GDV, IAJ, LIAJ, KIDI/보험개발원, FCA, ACPR, FSA, FSS) may be named, as may the tables they
publish, market indices and rates (VIX, CMT), laws, and any attribution a data licence
requires.

Before committing a change to an input file, search it for every publisher and product its
product's `sources.md` cites. Search case-insensitively: lowercase keys such as
`axa_50_viager` slip past a case-sensitive search.
