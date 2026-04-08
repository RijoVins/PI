# Vector Database Reference Guide & Cheat Sheet

## Quick Reference Commands

### Installation & Setup
```bash
# Navigate to project directory
cd d:\projects\Vector db

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install libraries
pip install chromadb pandas sentence-transformers

# Run setup
python setup_vector_db.py
```

### Running Searches
```bash
# Interactive search (recommended for beginners)
python search_verses.py

# Single query search
python search_verses.py --query "your search term"

# Get 10 results
python search_verses.py --query "search term" --results 10

# Run example searches
python search_verses.py --examples

# See all options
python search_verses.py --help
```

### Running Integration Examples
```bash
python integration_examples.py
```

---

## Where to Find What

| What | Location | When to Use |
|------|----------|------------|
| **Concepts & Theory** | VECTOR_DB_GUIDE.md | Understand vector databases |
| **Quick Start** | QUICK_START.md | First time setup |
| **Search** | search_verses.py | Perform queries |
| **Setup** | setup_vector_db.py | Create/update database |
| **Code Integration** | integration_examples.py | Use in your code |
| **Database** | chroma_db/ | Stores embeddings (don't edit) |

---

## Key Concepts Cheat Sheet

### Vector (Embedding)
```
Text: "அறம் செய விரும்பு"
        ↓
    [0.234, -0.156, 0.892, -0.445, 0.123, ..., 0.567]
    
Number of dimensions: 384
Represents: Meaning, context, semantic content
```

### Similarity Score
```
Match%  Interpretation          When to trust
100%    Perfect match           Very specific query
90%     Highly relevant         Most situations
80%     Very relevant           General matches
70%     Relevant               Broader searches
<70%    Less relevant          Consider other results
```

### Distance Metric
```
ChromaDB uses: Cosine Distance
0   = Identical vectors
1   = Perpendicular
2   = Opposite

Conversion to similarity: 1 - (distance / 2)
```

---

## Essential Files Explained

### setup_vector_db.py
**What it does:**
- Reads CSV files
- Generates embeddings
- Stores in ChromaDB
- Creates database

**When to run:**
- First time only
- When CSV data changes
- When you want to rebuild database

**Time: 2-5 minutes** (first run)

### search_verses.py
**What it does:**
- Loads database
- Searches embeddings
- Displays results
- Multiple search modes

**When to use:**
- Testing queries
- Interactive searches
- Command-line usage

**Time: <100ms** per query (after first run)

### integration_examples.py
**What it does:**
- Shows 6 practical examples
- Demonstrates API usage
- Flask integration template
- QA system example

**When to look at:**
- Building applications
- Understanding API
- Learning patterns

---

## Common Search Queries - Thirukural

### By Theme

**Morality & Ethics**
```
"righteousness and virtue"
"ethical conduct and duty"
"moral principles and dharma"
```

**Self-Control**
```
"controlling anger and emotions"
"self-discipline and restraint"
"mastering desires and passions"
```

**Knowledge & Learning**
```
"importance of learning and education"
"acquiring knowledge and wisdom"
"power of education and study"
```

**Generosity & Compassion**
```
"giving and charity"
"compassion and kindness"
"helping the needy and poor"
```

**Family & Relationships**
```
"family duties and responsibilities"
"friendship and companionship"
"husband and wife relations"
```

**Governance & Justice**
```
"ruling and governance"
"justice and fairness"
"king and subjects relations"
```

**Wealth & Prosperity**
```
"earning livelihood and wealth"
"prosperity and abundance"
"poverty and hardship"
```

**Love & Devotion**
```
"love and affection"
"devotion and loyalty"
"passion and desire"
```

---

## API Reference (for integration_examples.py)

### Class: TamilVersesSearcher

```python
from integration_examples import TamilVersesSearcher

# Initialize
searcher = TamilVersesSearcher()

# Search method
results = searcher.search(
    query: str,              # Search query
    num_results: int = 5     # Number of results
) -> List[Dict]

# Result structure
{
    'id': 'thirukural_1',
    'verse': 'verse text...',
    'source': 'Thirukural',
    'verse_number': '1',
    'chapter': 'கடவுள் வாழ்த்து',
    'similarity': 89.5  # Percentage
}
```

### Class: SimpleTamilQA

```python
from integration_examples import SimpleTamilQA

# Initialize
qa = SimpleTamilQA()

# Ask question
answer = qa.answer_question(
    question: str
) -> str

# Returns formatted answer with relevant verses
```

---

## Directory Structure Reference

```
Vector db/
│
├── 📄 VECTOR_DB_GUIDE.md              ← Detailed concepts & theory
├── 📄 QUICK_START.md                   ← 5-step quick start
├── 📄 CHEAT_SHEET.md                   ← This file
│
├── 🐍 setup_vector_db.py               ← Create database (run once)
├── 🐍 search_verses.py                 ← Search interface (run often)
├── 🐍 integration_examples.py           ← Code examples (reference)
│
├── Thirukural DB/
│   └── thirukkural_final.csv           ← Input data (1330 verses)
│
├── Aathichoodi/
│   └── aathichoodi.csv                 ← Input data (10 verses)
│
└── chroma_db/                          ← Vector database (auto-created)
    ├── chroma.sqlite3                  ← Main database file
    ├── chroma.sqlite3-shm
    └── chroma.sqlite3-wal
```

---

## Troubleshooting Quick Guide

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: chromadb` | Library not installed | `pip install chromadb` |
| `FileNotFoundError: CSV file` | Wrong file path | Check file path in script |
| `database locked` | Multiple instances running | Close other instances |
| `Model download stuck` | Network issues | Check connection, retry |
| `Memory error` | Insufficient RAM | Close other apps, try lighter model |
| `slow search` | First database load | This is normal; subsequent searches are fast |
| `No results found` | Query too specific | Try broader search terms |

---

## Performance Tuning

### Speed Up Searches
```python
# Use lightweight model (current default)
"all-MiniLM-L6-v2"  # 384 dimensions, fastest

# vs. More accurate but slower
"all-mpnet-base-v2"  # 768 dimensions, slower
```

### Reduce Memory Usage
```python
# Batch size in setup_vector_db.py
batch_size = 32  # Increasing this uses more RAM
batch_size = 8   # Decreasing this uses less RAM
```

### Optimize for Production
```python
# In search_verses.py, adjust:
include=['metadatas', 'documents', 'distances']  # Current
include=['metadatas', 'documents']               # Faster (no distances)
```

---

## Frequently Asked Questions (FAQ)

**Q: Can I search in English?**
A: Yes! The model understands English. Mix Tamil and English freely.

**Q: Can I update the database with new verses?**
A: Yes. Add to CSV and run `setup_vector_db.py` again.

**Q: Is the database persistent?**
A: Yes. The chroma_db/ folder contains everything. Delete it to reset.

**Q: Can multiple users search together?**
A: Read-only queries are safe. Avoid running setup while searching.

**Q: How do I back up the database?**
A: Copy the entire `chroma_db/` folder to backup location.

**Q: Can I use different embedding models?**
A: Yes. Change `EMBEDDING_MODEL` constant in scripts. Requires rerun of setup.

**Q: Does this work offline?**
A: Yes, after initial setup. No internet needed for searches.

**Q: Can I export search results?**
A: Yes. See integration_examples.py for programmatic access.

---

## Embedding Models Comparison

| Model | Dimensions | Speed | Accuracy | Size | Use Case |
|-------|-----------|-------|----------|------|----------|
| all-MiniLM-L6-v2 | 384 | 🟢 Fast | 🟡 Good | 80MB | Default, good balance |
| all-mpnet-base-v2 | 768 | 🟡 Slow | 🟢 Excellent | 330MB | High accuracy needed |
| all-distilroberta-v1 | 768 | 🟡 Medium | 🟡 Good | 270MB | Balanced |

To switch models:
1. Open `setup_vector_db.py`
2. Change `EMBEDDING_MODEL = "model-name"`
3. Delete `chroma_db/` folder
4. Run setup again

---

## Data Flow Diagram

```
CSV Files (1340 verses)
        ↓
[setup_vector_db.py]
        ↓
Pandas DataFrame parsing
        ↓
Text extraction (verse + meaning)
        ↓
[Sentence Transformer Model]
        ↓
Embeddings (384-dim vectors)
        ↓
[ChromaDB Storage]
        ↓
PERSISTENT DATABASE (chroma_db/)
        ↓
[search_verses.py]
        ↓
Query → Embedding → Similarity Match → Results
        ↓
User sees search results
```

---

## Best Practices

### Searching
✅ Use 3-5 word phrases
✅ Include concepts, not just keywords
✅ Start broad, then refine
✅ Try multiple queries for comprehensive results

❌ Don't use single words (too broad)
❌ Don't use exact phrase matching
❌ Don't expect keyword Boolean search

### Integration
✅ Cache results when possible
✅ Use batch queries for efficiency
✅ Handle empty results gracefully
✅ Show similarity scores to users

❌ Don't query 1000s of times per second
❌ Don't modify database manually
❌ Don't delete chroma_db while searching

### Maintenance
✅ Back up chroma_db/ regularly
✅ Keep CSV files updated
✅ Re-run setup after major CSV changes
✅ Monitor disk space

❌ Don't edit CSV files with special tools that may change encoding
❌ Don't move chroma_db/ without updating path
❌ Don't run multiple setup processes simultaneously

---

## Advanced: Custom Filtering

After getting search results, you can filter programmatically:

```python
searcher = TamilVersesSearcher()
results = searcher.search("righteousness", num_results=10)

# Filter by source
thirukural_only = [r for r in results if r['source'] == 'Thirukural']

# Filter by similarity
high_confidence = [r for r in results if r['similarity'] > 80]

# Get top result
best_match = results[0] if results else None
```

---

## Integration with Web Frameworks

### Flask
See `integration_examples.py` for template

### Django
```python
from django.http import JsonResponse
from integration_examples import TamilVersesSearcher

searcher = TamilVersesSearcher()

def search_view(request):
    query = request.GET.get('q')
    results = searcher.search(query)
    return JsonResponse({'results': results})
```

### FastAPI
```python
from fastapi import FastAPI
from integration_examples import TamilVersesSearcher

app = FastAPI()
searcher = TamilVersesSearcher()

@app.get("/search")
def search(query: str, n: int = 5):
    return searcher.search(query, num_results=n)
```

---

## Monitoring & Logging

To add logging to scripts:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting search for: " + query)
logger.debug("Found " + str(len(results)) + " results")
```

---

## Further Learning

### Official Documentation
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Vector Search Guide](https://en.wikipedia.org/wiki/Vector_search)

### Related Technologies
- Embeddings
- Vector Databases
- Semantic Search
- Similarity Metrics
- NLP (Natural Language Processing)

---

## Version Information

| Component | Version | Recommended |
|-----------|---------|------------|
| Python | 3.8+ | 3.10+ |
| ChromaDB | Latest | 0.4.0+ |
| Sentence-Transformers | Latest | 2.2.0+ |
| Pandas | Latest | 2.0+ |

Check versions:
```bash
python -c "import chromadb; print(chromadb.__version__)"
pip show sentence-transformers | grep Version
```

---

## Support & Resources

- **Errors?** Check Troubleshooting section above
- **How-to?** See QUICK_START.md
- **Concepts?** Read VECTOR_DB_GUIDE.md
- **Code?** Look at integration_examples.py
- **More help?** Check official documentation links above

---

**Last Updated:** April 6, 2026
**Status:** Production Ready
