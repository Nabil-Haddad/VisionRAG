# Project plan: product Q&A from a photo and a question

A multimodal retrieval-augmented generation (RAG) system built from scratch in Python.
A user sends a **photo of a product** and a **text question**; the system identifies the
product from the image, retrieves the relevant passages from a product knowledge base, and
answers with Claude, citing its sources or saying it doesn't know.

> Status: work in progress. See the [roadmap](#roadmap).

## The problem

Someone holds a product (an appliance, a food package, a bottle, a gadget) and wants an
answer that is buried in a manual, a spec sheet or a FAQ:

- *"Can I put this in the dishwasher?"* (photo of a mug)
- *"What is the warranty on this?"* (photo of a box)
- *"Is this safe for children under 3?"* (photo of a toy label)

Text-only search fails because the user doesn't know the model name. Image-only models
fail because the answer isn't in the picture. Combining both fixes this: **the photo
identifies the product, the question says what to look up, retrieval supplies the facts.**

## How it works

```
 photo + question
        |
        v
 1. VISION       Claude reads the image -> structured product info
        |        (brand, name, model, visible text, confidence)
        v
 2. QUERY        question + product info -> retrieval query (+ product filter)
        |
        v
 3. RETRIEVAL    embed query -> top-k chunks from the vector store
        |        (knowledge base: manuals, spec sheets, FAQs)
        v
 4. GENERATION   Claude answers from the chunks + the image,
                 cites sources, abstains if the sources don't support an answer
```

| Stage | Module | Responsibility |
|---|---|---|
| Vision | `src/vision.py` | Image -> structured product description (JSON) |
| Processing | `src/process.py` | Clean and chunk the raw documents |
| Ingestion | `src/ingestion.py` | Embed chunks and write them to the vector store |
| Retrieval | `src/retrieval.py` | Query -> ranked, filtered chunks |
| Generation | `src/generation.py` | Grounded answer with citations or an abstention |
| Config | `src/config.py` | Keys, model names, paths, constants |
| Entry point | `main.py` | CLI: `python main.py --image PHOTO --question "..."` |

## Design decisions

| Decision | Choice | Why |
|---|---|---|
| LLM and vision | Claude (Anthropic API) | One model for both reading the image and writing the answer |
| Embeddings | Local `sentence-transformers` | Anthropic has no embeddings API; local is free and reproducible |
| Vector store | Chroma (persistent, local) | No server, supports metadata filters |
| Knowledge base | 10 to 15 products with manuals/spec pages | Small enough to inspect by hand, big enough to be non-trivial |
| Product matching | Vision output used as a metadata filter and as query text | Stops answers from a similar but wrong product |

## Quality criteria

This project is judged against these, and each one has a deliverable.

1. **Vision and RAG are integrated.** The image changes what is retrieved, not just
   what is displayed. Deliverable: the vision output feeds the retrieval query and filter.
2. **A concrete use case.** Product Q&A over a fixed knowledge base. Deliverable: the
   dataset in `data/` and the example questions above.
3. **Evaluation.** Deliverable: `eval/questions.jsonl` (30 cases: image, question, expected
   answer, gold source) and `eval/run_eval.py` printing the metrics below.
4. **Clean structure.** Deliverable: one responsibility per module, typed signatures,
   no `exit()` in library code, config in one place, unit tests for the non-API parts.
5. **Reproducible.** Deliverable: `requirements.txt`, `.env.example`, setup steps below,
   and a short demo (screenshots or a GIF) in the README.
6. **Honest limits.** Deliverable: a "Known limitations" section filled in from real
   failures found during evaluation.

### Evaluation metrics

| Metric | What it measures |
|---|---|
| Product identification accuracy | Does the vision step name the right product? |
| Retrieval hit@k | Is the gold source chunk in the top k results? |
| Answer correctness | Does the answer match the expected one? (LLM judge plus manual spot checks) |
| Abstention rate | On questions the knowledge base can't answer, does it say so instead of guessing? |
| Citation validity | Does every cited source actually support the claim? |

Also report a **baseline** (question only, no image; image only, no retrieval) so the
benefit of combining both is visible in numbers.

## Roadmap

- [x] Project skeleton and config
- [x] Call Claude with text and with an image
- [ ] **M1 Vision:** return structured JSON (brand, product, model, visible text, confidence); test on the three sample images
- [ ] **M2 Knowledge base:** collect 10 to 15 product documents into `data/text/raw/`
- [ ] **M3 Processing and ingestion:** chunking, embeddings, Chroma store with product metadata
- [ ] **M4 Retrieval:** top-k search with product filter
- [ ] **M5 Generation:** grounded answer with citations and abstention
- [ ] **M6 CLI:** wire everything into `main.py`
- [ ] **M7 Evaluation:** question set, metrics, baselines, results table below
- [ ] **M8 Polish:** tests, limitations section, demo

## Results

_To be filled in after M7._

| Setup | Product ID | Hit@3 | Correctness | Abstains correctly |
|---|---|---|---|---|
| Question only | n/a | | | |
| Image only | | n/a | | |
| **Image + question + retrieval** | | | | |

## Setup

```bash
conda create -n mini-rag python=3.11
conda activate mini-rag
pip install -r requirements.txt
cp .env.example .env        # then set ANTHROPIC_API_KEY
python -m src.generation    # smoke test
```

## Known limitations

_To be filled in from evaluation failures (blurry photos, look-alike products,
questions the knowledge base cannot answer, and so on)._
