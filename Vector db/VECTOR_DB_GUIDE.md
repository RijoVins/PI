# Vector Database Setup Guide for Tamil Literature

## Table of Contents
1. [Understanding Vector Databases](#understanding-vector-databases)
2. [Choosing the Right Database](#choosing-the-right-database)
3. [Architecture Overview](#architecture-overview)
4. [Installation & Setup](#installation--setup)
5. [Complete Implementation](#complete-implementation)
6. [Testing & Querying](#testing--querying)

---

## Understanding Vector Databases

### What is a Vector?
A **vector** is a mathematical representation of text as numbers. For example:
```
Text: "பொறிவாயில் ஐந்தவித்தான் பொய்தீர் ஒழுக்க"
Vector: [0.234, -0.156, 0.892, -0.445, 0.123, ..., 0.567]  (384+ dimensions)
```

### Why Vector Databases?
- **Semantic Search**: Find similar verses even if they use different words
- **Meaning-Based Retrieval**: Search by meaning, not just keywords
- **AI Integration**: Enable intelligent question-answering systems
- **Fast Similarity Matching**: Quickly find related content

### How It Works: 3-Step Process

**Step 1: Embedding Generation**
```
Input Text → Embedding Model → Vector
"அறம் செய விரும்பு" → [0.12, -0.45, 0.78, ...] (384 numbers)
```

**Step 2: Storage in Vector DB**
```
Vector DB stores: {
  id: 1,
  meaning: "Quality of being righteous",
  text: "அறம் செய விரும்பு",
  vector: [0.12, -0.45, 0.78, ...]
}
```

**Step 3: Semantic Search**
```
Query: "righteousness and morality"
Query Vector: [0.11, -0.46, 0.79, ...]
         ↓
    Compare with stored vectors
         ↓
Find most similar verses (using distance calculation)
```

---

## Choosing the Right Database

### Comparison Table

| Feature | FAISS | Pinecone | ChromaDB | Weaviate |
|---------|-------|----------|----------|----------|
| **Setup** | Complex | Cloud-based | Simple | Moderate |
| **Cost** | Free | Paid | Free | Free |
| **Local Use** | ✅ | ❌ | ✅ | ✅ |
| **Learning Curve** | Steep | Easy | Very Easy | Moderate |
| **Python Integration** | Good | Excellent | Excellent | Good |
| **Persistence** | Manual | Automatic | Automatic | Automatic |
| **Ideal For** | Production/Large Scale | Enterprise | Beginners/Prototyping | Production |

### **Recommendation: ChromaDB** ✅
**Why ChromaDB?**
- ✅ **Zero Setup**: Works immediately with zero configuration
- ✅ **Lightweight**: ~50MB, no external dependencies
- ✅ **Persistent Storage**: Automatically saves data locally
- ✅ **Excellent for Beginners**: Simple, intuitive API
- ✅ **Perfect for Prototyping**: Ideal for testing before scaling

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR SYSTEM                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  CSV Files (Thirukural, Aathichoodi)                    │
│       ↓                                                  │
│  [1. CSV Loader Script]                                │
│       ↓                                                  │
│  Text Extraction (verse_text + meaning)                 │
│       ↓                                                  │
│  [2. Embedding Generation]                             │
│  (Using sentence-transformers pretrained model)        │
│       ↓                                                  │
│  Embeddings (384-dimensional vectors)                   │
│       ↓                                                  │
│  [3. ChromaDB Storage]                                 │
│  (Persistent local database)                           │
│       ↓                                                  │
│  [4. Semantic Search Script]                           │
│  (Query → Embedding → Similarity → Results)            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Installation & Setup

### Step 1: Install Required Libraries

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows
# or: source venv/bin/activate  # On macOS/Linux

# Install required packages
pip install chromadb pandas sentence-transformers scikit-learn
```

### Required Libraries Explained

| Library | Purpose | Why Needed |
|---------|---------|-----------|
| **chromadb** | Vector database | Store and search embeddings |
| **pandas** | Data processing | Read and manipulate CSV files |
| **sentence-transformers** | Embedding generation | Convert text to vectors |
| **scikit-learn** | ML utilities | Optional, for similarity calculations |

### Step 2: Verify Installation

```bash
python -c "import chromadb; import pandas; import sentence_transformers; print('All libraries installed successfully!')"
```

---

## Complete Implementation

### File Structure After Setup

```
Vector db/
├── VECTOR_DB_GUIDE.md (this file)
├── setup_vector_db.py (main implementation)
├── search_verses.py (query & search script)
├── chroma_db/ (created automatically)
│   └── (vector database files)
└── embeddings_cache/ (optional, stores embeddings)
```

---

## Testing & Querying

After running the scripts, you can perform semantic searches like:

1. **Search by Meaning**: "Find verses about righteousness and morality"
2. **Search by Theme**: "verses about controlling emotions"
3. **Search by Concept**: "importance of learning and knowledge"

---

## Performance Notes

- **First Run**: ~2-5 minutes (generating embeddings)
- **Subsequent Runs**: <100ms (loaded from cache)
- **Memory Usage**: ~500MB-1GB (depends on dataset size)
- **Storage**: ~100-200MB for database files

---

## Next Steps

1. Run `setup_vector_db.py` to create the database
2. Run `search_verses.py` to test queries
3. Integrate into your application
4. Scale to larger datasets if needed

---

## Troubleshooting

### Issue: "No module named 'chromadb'"
**Solution**: Run `pip install chromadb` in activated virtual environment

### Issue: "Model download takes too long"
**Solution**: First run takes time (~500MB download). Subsequent runs are instant.

### Issue: "Memory error on older machines"
**Solution**: Use simpler model: `all-MiniLM-L6-v2` (lighter weight)

### Issue: "Database locked error"
**Solution**: Ensure only one script accessing database at a time

---

## Additional Resources
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Vector Database Concepts](https://en.wikipedia.org/wiki/Vector_search)
