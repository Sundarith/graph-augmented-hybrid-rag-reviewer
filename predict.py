"""Run Graph-Augmented Hybrid RAG on a single CWE classification question."""

import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", help="CVE-to-CWE classification question")
    args = parser.parse_args()

    os.chdir(Path(__file__).resolve().parent)
    corpus = Path("data/processed/cve_chunks.jsonl")
    if not corpus.is_file() or corpus.stat().st_size == 0:
        parser.error("run python3 prepare_corpus.py to build the CVE corpus")

    defaults = {
        "CTI_RAG_RCM_ONLY": "1",
        "CTI_RAG_PROMPT_CONTEXT_ONLY": "1",
        "CTI_RAG_CWE_CROSSENCODER": "1",
        "CTI_RAG_LLM_MAX_MODEL_LEN": "24576",
        "CTI_RAG_LLM_RESPONSE_BUDGET": "2048",
    }
    for name, value in defaults.items():
        os.environ.setdefault(name, value)

    import better_rag

    answer, _, _ = better_rag.ask(args.question, [], eval_mode=True)
    if not answer or answer.startswith("Error:"):
        raise SystemExit(answer or "The answer model returned an empty response")
    print(answer)


if __name__ == "__main__":
    main()
