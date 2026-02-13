# Understanding LLM Hallucinations in Health Insurance Recommendations

## 📖 Table of Contents

1. [What Are Hallucinations?](#what-are-hallucinations)
2. [Why Do Hallucinations Happen?](#why-do-hallucinations-happen)
3. [Our Specific Hallucination Problems](#our-specific-problems)
4. [Why RAG Alone Doesn't Solve It](#why-rag-alone-doesnt-solve-it)
5. [How to Reduce Hallucinations](#how-to-reduce-hallucinations)
6. [Production Solutions](#production-solutions)
7. [Tradeoffs & Recommendations](#tradeoffs--recommendations)

---

## What Are Hallucinations?

**Hallucination** = When an AI model generates information that is **factually incorrect** or **not based on the provided data**.

### Examples from Our System

❌ **Company Hallucinations:**
- "Future Generali India Insurance Company Limited" (not in our database)
- "Bajaj Allianz General Insurance Company Limited" (not in our database)
- "Acko General Insurance" (not in our database)

❌ **Data Hallucinations:**
- Showing "Unlimited" sum insured for wrong plans
- Making up CSR percentages
- Creating fake plan names like "ICICIdirect SuperSaver Plus"
- Empty table columns or nonsense text like "₹1 – 3 L Acres Per Child"

✅ **What We Actually Have:**
Only 6 insurers in our database:
- Star Health and Allied Insurance Co. Ltd.
- HDFC ERGO General Insurance Company Ltd.
- ICICI Lombard General Insurance Co. Ltd.
- Niva Bupa Health Insurance Co. Ltd.
- Care Health Insurance Ltd.
- Aditya Birla Health Insurance Co. Ltd.

---

## Why Do Hallucinations Happen?

### 1. **Training Data Conflict**

LLMs like llama3.2 were trained on massive internet data including **real information about Indian insurance companies**.

```
LLM Training Data Contains:
- Future Generali (REAL company that exists)
- Bajaj Allianz (REAL company that exists)
- Acko (REAL company that exists)
- Max Bupa, Reliance, Tata AIG, etc.
```

**The Problem:**
When asked about Indian health insurance, the model **already "knows" these companies from training** and defaults to using that knowledge instead of our RAG data.

**Analogy:**
- You give someone a textbook to read (RAG context)
- But they already memorized a different textbook (training data)
- They answer from memory, not from the book you gave them

### 2. **Prompt Following Limitations**

Even with strict instructions like:
```
⚠️ DO NOT mention Future Generali
⚠️ USE ONLY the 3 plans provided above
⚠️ COPY EXACTLY from the data
```

**Small models like llama3.2 struggle to**:
- Ignore their pre-trained knowledge
- Follow complex negative instructions ("don't use X")
- Prioritize context over training

### 3. **Pattern Completion**

LLMs work by predicting the next token. When they see:
```
| Insurer | HDFC ERGO | ??? | ??? |
```

Their training tells them: "Indian insurance comparison tables usually have 3-4 companies, and common ones are Future Generali, Bajaj..."

**They complete the pattern from training data, not from context.**

### 4. **Context Window Limitations**

Even though we use RAG to provide relevant data:
- LLM processes ~200K tokens of context
- Our RAG context is only ~2000 tokens
- Training data is in the model's weights (always "louder" than context)

### 5. **Instruction Hierarchy**

The model sees conflicting instructions:
- **System training:** "Know about all Indian insurance companies"
- **Our prompt:** "Only use these 3 companies"

Small models can't reliably prioritize our instructions over training.

---

## Our Specific Problems

### Problem 1: Company Name Hallucinations

**What Happens:**
```
User: "I need maternity coverage"
RAG: Returns Star Health, HDFC ERGO, Care Health
LLM: Outputs Future Generali, Bajaj Allianz, Acko
```

**Why:**
- LLM knows Future Generali has good maternity coverage (from training)
- Ignores our RAG data
- Uses general knowledge instead

### Problem 2: Empty Table Rows/Columns

**What Happens:**
First row of comparison table is empty

**Why:**
- Model struggles with markdown table formatting
- Loses track of which cell it's filling
- Instruction following breaks down mid-generation

### Problem 3: Made-up Plan Names

**What Happens:**
"ICICIdirect SuperSaver Plus" instead of real plan names

**Why:**
- Model combines pattern fragments
- ICICI Lombard (real) + Direct (common word) + SuperSaver (from another plan)
- Creates plausible-sounding but fake names

### Problem 4: Wrong Values for Right Plans

**What Happens:**
Shows "Unlimited" sum insured for Star Comprehensive (max is ₹1Cr)

**Why:**
- Model knows some plans have "Unlimited" (Super Star does)
- Mixes up which plan has which feature
- Cross-contaminates plan details

---

## Why RAG Alone Doesn't Solve It

### What RAG Does ✅

1. **Semantic Search** - Finds most relevant 3 plans
2. **Provides Context** - Sends exact plan data to LLM
3. **Reduces Scope** - Only 3 plans instead of all 9

### What RAG Cannot Do ❌

1. **Override Training** - Can't erase model's pre-trained knowledge
2. **Guarantee Compliance** - Can't force model to use only provided data
3. **Prevent Pattern Matching** - Can't stop model from completing patterns with training data
4. **Fix Small Model Limits** - Can't make llama3.2 as reliable as GPT-4

### The Fundamental Issue

```
RAG = Better INPUT to the model
Hallucination = OUTPUT problem

No matter how good the input, small models can still produce bad output.
```

---

## How to Reduce Hallucinations

### ✅ Solutions That Work

#### 1. **Use Larger/Better Models**

**Switch from llama3.2 to:**
- **GPT-4** (OpenAI API)
  - 95%+ reliability
  - Cost: ~$0.01-0.02 per recommendation
  - Best instruction following

- **Claude 3.5 Sonnet** (Anthropic API)
  - Excellent at following constraints
  - Cost: ~$0.01 per recommendation
  - Great for structured output

- **llama3.1-70B** (Ollama, local)
  - Better than llama3.2
  - Requires powerful GPU
  - Free but slower

**Why It Works:**
Larger models have better instruction following and can override training with context more reliably.

#### 2. **Validation + Retry Loop**

```python
for attempt in range(3):
    response = get_llm_response()
    if no_hallucinations_detected(response):
        return response
    else:
        print(f"Retry {attempt + 1}/3")

return "Error: Could not generate accurate recommendation"
```

**Pros:**
- Catches hallucinations
- Auto-retries
- Works with any model

**Cons:**
- Slower (3x time worst case)
- Still might fail after 3 tries
- Bad user experience if frequent failures

#### 3. **Constrained Generation**

Force model to only output from allowed list:

```python
ALLOWED_INSURERS = [
    "Star Health",
    "HDFC ERGO",
    "ICICI Lombard",
    ...
]

# During generation, reject tokens not in allowed list
```

**Pros:**
- 100% prevents company hallucinations
- Guaranteed accuracy

**Cons:**
- Technically complex
- Not well-supported in CrewAI
- Reduces natural language quality

#### 4. **Template-Based Output**

Don't use LLM for comparison table:

```python
# LLM only selects 3 plans
selected_plans = llm.select_plans(user_needs)

# Python code creates table
table = create_comparison_table(selected_plans)
```

**Pros:**
- 100% accurate tables
- No formatting issues
- Fast and reliable

**Cons:**
- Less flexible
- Loses natural language recommendations
- More code to maintain

#### 5. **Fine-Tuning**

Train llama3.2 specifically on OUR 6 insurers:

```
Training data:
User: "I need maternity coverage"
AI: "I recommend Star Health Comprehensive Policy..."

DO NOT include Future Generali, Bajaj, etc. in training
```

**Pros:**
- Model "forgets" other insurers
- Optimized for our exact use case
- Free after training

**Cons:**
- Requires ML expertise
- ~100-500 training examples needed
- Needs re-training when data changes

#### 6. **Hybrid Approach**

Combine multiple techniques:

1. RAG for retrieval
2. Strict prompts
3. Validation layer
4. Template for comparison table
5. LLM only for reasoning/recommendations

**Pros:**
- Best of all approaches
- Reliable and flexible

**Cons:**
- More complex architecture

---

## Production Solutions

### Option A: Switch to GPT-4 (Recommended)

**What to Change:**
```python
os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4"
os.environ["OPENAI_API_KEY"] = "your-api-key"
```

**Costs:**
- Input: $0.01 per 1K tokens
- Output: $0.03 per 1K tokens
- ~2K tokens per recommendation = $0.05 per recommendation
- 1000 users = $50

**Pros:**
- Works immediately
- 95%+ accuracy
- No hallucinations

**Cons:**
- Costs money
- Requires API key
- Internet dependency

### Option B: Validation + Retry

**Add to backend:**
1. Detect hallucinations (already added)
2. If detected, retry up to 3 times
3. If still failing, show error to user

**Pros:**
- Free
- Works with llama3.2
- Reduces hallucinations by 60-70%

**Cons:**
- Not 100% reliable
- Slower
- Some requests fail

### Option C: Template Tables

**Use LLM for:**
- Understanding user needs
- Selecting 3 best plans
- Writing "Why This Plan" reasoning

**Use Python for:**
- Comparison table (100% accurate)
- All numerical data

**Pros:**
- Free
- 100% accurate tables
- Fast

**Cons:**
- Less natural language
- More code

---

## Tradeoffs & Recommendations

### For Production (Public Users)

**Use GPT-4**
- Cost: ~$50-100/month for moderate traffic
- Reliability: 95%+
- User Experience: Excellent

### For Development/Demo

**Use llama3.2 + Templates**
- Cost: Free
- Reliability: 85-90%
- User Experience: Good

### For Internal Tool

**Use llama3.2 + Validation**
- Cost: Free
- Reliability: 70-80%
- User Experience: Acceptable (users understand it's experimental)

---

## Summary

### Why Hallucinations Happen

1. **Training data conflict** - Model knows other insurers
2. **Small model limitations** - Can't reliably follow complex instructions
3. **Pattern completion** - Fills gaps with training knowledge
4. **Context vs. weights** - Training always "louder" than RAG context

### Best Solutions

| Solution | Cost | Reliability | Complexity |
|----------|------|-------------|------------|
| GPT-4 API | $$$ | 95% | Low |
| llama3.1-70B | Free* | 85% | Medium |
| Validation + Retry | Free | 70% | Medium |
| Templates | Free | 90%** | High |
| Fine-tuning | Free* | 80% | Very High |

*Requires powerful hardware  
**For tables only

### Our Recommendation

**Phase 1 (Now):** Add validation + retry to reduce hallucinations

**Phase 2 (Production):** Switch to GPT-4 API OR use template-based tables

**Long-term:** Fine-tune a local model on our data for cost-free accuracy

---

**Remember:** Hallucinations are a fundamental limitation of small LLMs. There's no perfect free solution. Production systems need either better models or hybrid approaches.
