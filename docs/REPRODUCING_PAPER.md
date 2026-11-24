# Reviewer walkthrough

## 1. Verify the saved result

Run `python3 artifacts/verify.py` from the repository root. The two CSVs contain the completion ordinal within each split, the public CVE identifier, and the evaluator's binary outcome. A CVE identifier can occur more than once. The ordinal preserves each logged benchmark case. The [manifest](../artifacts/manifest.json) identifies the May 2026 runs and records SHA-256 digests for their logs and the packaged CSVs.

The CSVs preserve scored outcomes. Raw model responses are absent, so this check recalculates the recorded tally without rescoring responses. The manuscript describes strict matching. The supplied historical evaluator implements a case-insensitive gold-string substring check in `cwe_in_answer`.

## 2. Install the archived implementation

The implementation and requirements are from the archived public code snapshot at commit `ec41386f7707cf24e0337536255d16cb0bc307d5`. Install the [retrieval dependencies](../requirements-retrieval.txt) with a CUDA-capable PyTorch build. Serve the answer model from a separate environment with vLLM 0.19.x. [requirements.txt](../requirements.txt) preserves the archived dependency list.

```bash
python3 -m pip install -r requirements-retrieval.txt
```

## 3. Load the benchmark and construct the corpus

```bash
git clone https://github.com/xashru/cti-bench.git data/cti-bench
git -C data/cti-bench checkout --detach 4543e5b6560d3204e1205ced4fa286adc7452d07
```

This is the benchmark revision available in the working checkout when preparing the repository. The archived evaluator reads `data/cti-bench/data/cti-rcm.tsv` and uses its `Prompt` field.

Place an independently obtained CVE Services JSON corpus under `data/raw/cves/cves/YYYY/`, using the CVE 5 record format expected by the builder. The archived builder reads explicit `cweId` values in CNA and ADP problem-type fields. The bundled CWE text chunks are derived from the MITRE CWE catalog.

```bash
python3 prepare_corpus.py
```

The May runs recorded 332,104 loaded CVE and CWE chunks. The exact May corpus and embedding cache are unavailable in this package. A different corpus snapshot can change the mapped/unmapped split and retrieval results.

## 4. Run and score fresh predictions

Serve the answer model on a GPU:

```bash
vllm serve microsoft/Phi-4-mini-reasoning \
  --enable-prefix-caching --trust-remote-code --port 8000 \
  --max-model-len 24576 --gpu-memory-utilization 0.90
```

In the retrieval environment, run a single question or score the benchmark:

```bash
python3 predict.py 'Which CWE best describes unchecked writes beyond a buffer boundary?'
```

```bash
export CTI_RAG_EMBEDDER_DEVICE=cuda
export CTI_RAG_CWE_CROSSENCODER_DEVICE=cuda
export CTI_RAG_EVAL_STREAM_RESULTS=1
bash scripts/run_shipped_phi_eval.sh 1000 --nvd-mapped
bash scripts/run_shipped_phi_eval.sh 1000 --nvd-unmapped
```

The launcher uses the context-only prompt, enables CWE cross-encoder reranking, and configures a 2,048-token generation budget. The commands above use GPU retrieval with a locally served reader. The saved May logs correspond to two archived split runs. The commands provide a fresh evaluation on the supplied corpus. Each invocation reports its denominator and writes output under `logs/`.
