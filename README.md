# Graph-Augmented Hybrid RAG for CVE-to-CWE Mapping

Reviewer artifacts for *Graph-Augmented Hybrid RAG for CVE-to-CWE Mapping with Compact Open Large Language Models*. The system combines BM25 and dense retrieval, structured CVE-to-CWE graph edges, similarity-weighted neighbor voting, cross-encoder reranking, and a Phi-4-mini-reasoning answer step.

## Saved CTI-Bench RCM result

| Historical subset | Correct / total | Accuracy |
| --- | ---: | ---: |
| Mapped | 837 / 903 | 92.7% |
| Unmapped | 72 / 97 | 74.2% |
| Combined | 909 / 1,000 | 90.9% |

The mapped condition can use the structured CWE assignment for the target CVE when available. The historical evaluator marks a case correct when the gold CWE string occurs anywhere in the generated answer, ignoring case.

## Quickstart

Run the offline check from the repository root with Python 3.10 or newer:

```bash
python3 artifacts/verify.py
```

The verifier checks the integrity and completeness of the two saved outcome files and recalculates the reported tally. See the [reviewer walkthrough](docs/REPRODUCING_PAPER.md) for evidence provenance, benchmark setup, and fresh-inference commands.

| Path | Contents |
| --- | --- |
| [artifacts/](artifacts/) | Per-case historical outcomes, source manifest, and offline verifier |
| [docs/REPRODUCING_PAPER.md](docs/REPRODUCING_PAPER.md) | Procedure and historical configuration |
| [better_rag.py](better_rag.py) | Archived retrieval and answer pipeline |
| [eval_rcm.py](eval_rcm.py) | Archived benchmark harness |
| [scripts/run_shipped_phi_eval.sh](scripts/run_shipped_phi_eval.sh) | Historical inference defaults |
