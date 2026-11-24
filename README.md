# Graph-Augmented Hybrid RAG for CVE-to-CWE Mapping

Reviewer artifacts for *Graph-Augmented Hybrid RAG for CVE-to-CWE Mapping with Compact Open Large Language Models*. The system combines BM25 and dense retrieval, structured CVE-to-CWE graph edges, similarity-weighted neighbor voting, cross-encoder reranking, and a Phi-4-mini-reasoning answer step.

## Saved CTI-Bench RCM result

| Historical subset | Correct / total | Accuracy |
| --- | ---: | ---: |
| Mapped | 837 / 903 | 92.7% |
| Unmapped | 72 / 97 | 74.2% |
| Combined | 909 / 1,000 | 90.9% |

The mapped condition can use the structured CWE assignment for the target CVE when available. The historical evaluator marks a case correct when the gold CWE string occurs anywhere in the generated answer, ignoring case.

## Run the working code

Clone the repository:

```bash
git clone https://github.com/Sundarith/graph-augmented-hybrid-rag-reviewer.git
cd graph-augmented-hybrid-rag-reviewer
```

Follow the [setup instructions](docs/REPRODUCING_PAPER.md#2-install-the-archived-implementation) to install retrieval dependencies, build the corpus, and serve Phi-4-mini-reasoning. Then run a single CWE classification question:

```bash
python3 predict.py 'Which CWE best describes unchecked writes beyond a buffer boundary?'
```

For batch scoring, use the [CTI-Bench evaluation commands](docs/REPRODUCING_PAPER.md#4-run-and-score-fresh-predictions).

## Verify the saved result

Run the offline check from the repository root with Python 3.10 or newer:

```bash
python3 artifacts/verify.py
```

The verifier checks the integrity and completeness of the two saved outcome files and recalculates the reported tally. See the [reviewer walkthrough](docs/REPRODUCING_PAPER.md) for evidence provenance, benchmark setup, and fresh-inference commands.

| Path | Contents |
| --- | --- |
| [artifacts/](artifacts/) | Per-case historical outcomes, source manifest, and offline verifier |
| [docs/REPRODUCING_PAPER.md](docs/REPRODUCING_PAPER.md) | Procedure and historical configuration |
| [predict.py](predict.py) | Single-question inference |
| [prepare_corpus.py](prepare_corpus.py) | Build CVE chunks and the evaluation split index |
| [better_rag.py](better_rag.py) | Archived retrieval and answer pipeline |
| [eval_rcm.py](eval_rcm.py) | Archived benchmark harness |
| [scripts/run_shipped_phi_eval.sh](scripts/run_shipped_phi_eval.sh) | Historical inference defaults |
