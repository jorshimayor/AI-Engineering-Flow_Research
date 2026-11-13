# Article 2: Where RAG fails (outline)

## Title options
- **My Retriever Found the Right Page and the Wrong Paragraph**
- Chunk Boundaries, Question Wording and k: A RAG Error Audit
- Why "What Colour Is It Sold In?" Broke My Retriever

**Target reader:** has a RAG system that is "mostly right" and no breakdown of why the rest is wrong.
**Promise:** split every wrong answer into retrieval misses and reading misses, find the pattern in each, and test the cheap fixes.
**Length:** ~1,400 words · **Hero:** `week7_topk.png`

---

## Outline

### 1. Hook (~120 words)
At k = 1, 47 of 200 answers were wrong. Every one was a colour or power-rating question, and every time the retriever had picked the right page.

### 2. Split errors in two (~200 words)
- Retrieval miss: the chunk holding the answer was not in the prompt.
- Reading miss: it was there, and the model still got it wrong (a sibling's value, "unknown", or a misread).
- How to mark the answer-bearing chunk when you know the gold answer.

### 3. The wrong paragraph (~300 words)
- Colour, power and weight sit in the same middle chunk. Weight questions found it 30 of 30 times; colour 1 of 28; power 10 of 30.
- Likely cause: question words pull towards other chunks ("sold in" ≈ "sells the C-200 at…").
- At k = 1 accuracy equals retrieval accuracy, because the models abstained on all 47 misses.

### 4. More chunks, more distractors (~250 words)
- k = 1 → 3: +21 to 23 points. k = 3 → 10: within 1.5 points, at 2.8× the tokens and time.
- At 1.5B, k = 5 gave a sibling's value 6 times with the right chunk ranked first. The 3B model never did.

### 5. Chunk size and the title fix (~300 words)
- Sweep: 32, 64, 128 words and whole pages; BM25, dense, hybrid; with and without the page title in every chunk.
- At 32 words the title lifts hit@3 from 50% to 97% (BM25) and 68% to 92% (dense).
- Dense found the right chunk first more often than BM25 (76% vs 55% at 64 words), the opposite of my prediction that product codes would favour BM25.
- The one result I can't explain: at 128 words the title lowered dense hit@3 from 98% to 92%.

### 6. What I'd change (~150 words)
Title (or a one-line summary) in every chunk; k = 3; check which chunk a question type retrieves; harder eval questions for Week 8: misspelt names, two-fact questions, conflicting pages.

### 7. Reproduce this
Colab link; the notebook's failure section prints each wrong answer with its retrieved chunks.

---

## Stretch experiment
**Contextual chunks.** Prepend a one-sentence, model-written summary of the page to each chunk (Anthropic's contextual retrieval) and re-run the k = 1 condition. Does it fix the colour questions that the title alone does not?

## Self-check (closed-book)
1. What makes a chunk "answer-bearing", and why does that need the gold answer?
2. Why did accuracy equal retrieval accuracy at k = 1?
3. Why could adding chunks lower accuracy for the 1.5B model?
4. Why does BM25 struggle to pick between chunks of the same page?
5. Name two cheap changes that would raise hit@1 here, and the cost of each.
