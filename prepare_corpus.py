"""Build the CVE retrieval corpus and evaluation split index."""

import json
from pathlib import Path

import build_cve_chunks


def main():
    if not build_cve_chunks.RAW_DIR.is_dir():
        raise SystemExit(f"Place CVE 5 JSON records under {build_cve_chunks.RAW_DIR}/")

    build_cve_chunks.main()
    with build_cve_chunks.OUT.open(encoding="utf-8") as source:
        records = (json.loads(line) for line in source)
        index = {record["identifier"]: record.get("cwe_ids", []) for record in records}
    if not index:
        raise SystemExit("No published CVE records were found")

    directory = build_cve_chunks.OUT.parent
    target = directory / "cve_cwe_index.json"
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(index), encoding="utf-8")
    temporary.replace(target)

    # The archived retriever checks cache size, so an equally sized rebuild also
    # needs invalidation to keep embedding rows aligned with the new corpus.
    for cache in directory.glob("chunk_embs*.npy"):
        cache.unlink()
    print(f"Indexed {len(index):,} CVEs in {target}")


if __name__ == "__main__":
    main()
