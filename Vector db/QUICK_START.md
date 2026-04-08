# Quick Start Guide - Vector Database Setup

## Overview

This guide will help you set up vector database for semantic search on your Tamil literature datasets in **5 simple steps**.

---

## 📋 Prerequisites

- Python 3.8 or higher
- Your CSV files (Thirukural and Aathichoodi) already in place
- ~1.5 GB free disk space
- ~2-3 GB RAM available during setup

---

## 🚀 5-Step Quick Start

### **Step 1: Prepare Your Environment**

Open a terminal/command prompt in your project directory and run:

```bash
# Navigate to your project directory
cd d:\projects\Vector db

# Create a virtual environment (recommended)
python -m venv venv

# Activate it
venv\Scripts\activate

# Or on macOS/Linux:
# source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

---

### **Step 2: Install Required Libraries**

```bash
pip install chromadb pandas sentence-transformers
```

**What this does:**
- `chromadb`: Vector database for storing embeddings
- `pandas`: Read and process CSV files  
- `sentence-transformers`: Convert text to embeddings

**Installation time:** 2-5 minutes

---

### **Step 3: Run the Setup Script**

```bash
python setup_vector_db.py
```

**What happens:**
1. Loads your CSV files
2. Generates embeddings for all verses (~2-5 minutes)
3. Stores them in ChromaDB
4. Creates a local database in `chroma_db/` folder

**Expected output:**
```
======================================================================
   TAMIL LITERATURE VECTOR DATABASE SETUP
======================================================================

📚 Loading Thirukural data...
   ✓ Loaded 1330 verses

📚 Loading Aathichoodi data...
   ✓ Loaded 10 verses

✓ Total documents loaded: 1340
  - Thirukural: 1330 verses
  - Aathichoodi: 10 verses

🤖 Initializing embedding model: all-MiniLM-L6-v2
   This may take 30-60 seconds on first run (downloading model)...
   ✓ Model loaded successfully

⚡ Generating embeddings for 1340 documents...
   100%|████████████████| 1340/1340 [02:45<00:00, 8.10 docs/sec]
   ✓ Generated 1340 embeddings
   Embedding dimension: 384 dimensions

💾 Initializing ChromaDB...
   ✓ ChromaDB initialized

📦 Storing embeddings in ChromaDB collection: 'tamil_literature'
   ✓ Stored 1340 documents with embeddings

======================================================================
   ✓ VECTOR DATABASE SETUP COMPLETED SUCCESSFULLY!
======================================================================
```

---

### **Step 4: Test with Interactive Search**

```bash
python search_verses.py
```

**This starts interactive search mode:**
```
================================================================================
   TAMIL LITERATURE SEMANTIC SEARCH
================================================================================

🔄 Initializing search components...
   ✓ ChromaDB client initialized
   ✓ Collection 'tamil_literature' loaded
   ✓ Collection contains 1340 documents
   Loading embedding model: all-MiniLM-L6-v2...
   ✓ Embedding model loaded

================================================================================
   INTERACTIVE SEARCH MODE
   (Type 'quit' or 'exit' to stop)
================================================================================
```

Now you can enter search queries!

---

### **Step 5: Try Example Searches**

Run the script with example flag:

```bash
python search_verses.py --examples
```

Or try specific queries:

```bash
# Single search
python search_verses.py --query "righteousness and morality" --results 5

# More results
python search_verses.py --query "knowledge and learning" --results 10
```

---

## 🔍 How to Use the Search

### Interactive Mode (Most User-Friendly)

```bash
python search_verses.py
```

Then type search queries like:
```
🔍 Enter search query: controlling anger and emotions
   Number of results (default 5): 5
```

### Command-Line Mode (Quick Single Search)

```bash
python search_verses.py --query "your search term" --results 7
```

### Example Searches to Try

1. **"righteousness and moral duty"** - Find verses about dharma/ethics
2. **"controlling emotions and anger"** - Find verses about self-control
3. **"importance of learning"** - Find verses about education
4. **"compassion and generosity"** - Find verses about kindness
5. **"detachment from sensory pleasures"** - Find verses about renunciation
6. **"governance and justice"** - Find verses about ruling
7. **"friendship and enmity"** - Find verses about relationships

---

## 📊 Understanding Search Results

Each result shows:

```
─────────────────────────────────────────────────────────────────────────────
RESULT #1
─────────────────────────────────────────────────────────────────────────────
ID: thirukural_1
Source: Thirukural
Verse Number: 1
Chapter: கடவுள் வாழ்த்து

📊 Similarity: 89.5% [████████████████████░░░░░░░░░░░░░░░░░░]

📖 Verse(Text):
   அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு.

💭 Meaning:
   Letters begin with 'A'; The world begins with the Divine. 
   Just as all letters have 'A' as their foundation, the entire universe 
   has the Supreme Being as its foundation.
```

**Similarity Score:** 
- 95-100% = Highly relevant
- 80-95% = Very relevant
- 70-80% = Relevant
- <70% = Less relevant

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named 'chromadb'" | Run `pip install chromadb` in activated venv |
| "CSV file not found" | Check file paths in `setup_vector_db.py` (lines 18-19) |
| "Database not found" | Run `setup_vector_db.py` first to create database |
| "Slow search" | This is normal for first run; results cache afterwards |
| "Memory error" | Restart and ensure 2GB+ RAM available |
| "Model download taking too long" | This is normal (~500MB); first run only |

---

## 📁 What Gets Created

After setup, your directory structure will look like:

```
Vector db/
├── VECTOR_DB_GUIDE.md           (Comprehensive guide you read earlier)
├── QUICK_START.md               (This file!)
├── setup_vector_db.py           (Setup script)
├── search_verses.py             (Search script)
├── Thirukural DB/
│   └── thirukkural_final.csv
├── Aathichoodi/
│   └── aathichoodi.csv
└── chroma_db/                   (Created automatically)
    ├── chroma.sqlite3
    ├── chroma.sqlite3-shm
    └── chroma.sqlite3-wal
```

The `chroma_db/` folder contains your vector embeddings and is ~200-300MB.

---

## ⚡ Performance Notes

| Operation | Time | Notes |
|-----------|------|-------|
| First setup | 2-5 min | Model download + embedding generation |
| One search query | <100ms | Instant after first run |
| Memory during setup | ~1.5 GB | Loading embeddings |
| Database disk size | ~200-300 MB | For 1340 verses |

---

## 🎯 Next Steps

1. ✅ Follow the 5 steps above
2. ✅ Run test searches to verify setup
3. ✅ Integrate into your application
4. ✅ Customize embedding model if needed (see VECTOR_DB_GUIDE.md)

---

## 💡 Tips & Tricks

### Better Search Results
- Use 3-5 word queries for best results
- Include concepts, not just keywords
- Example: "controlling anger" instead of just "anger"

### Rerun Setup After Updates
If you update your CSV files:
```bash
# Remove old database
rm -r chroma_db  # On Windows: rmdir /s chroma_db

# Rerun setup with new data
python setup_vector_db.py
```

### Use Different Models
Change `EMBEDDING_MODEL` in scripts:
- `"all-MiniLM-L6-v2"` - Fast, 384 dimensions (default)
- `"all-mpnet-base-v2"` - More accurate, 768 dimensions  
- `"all-distilroberta-v1"` - Balanced, 768 dimensions

---

## ❓ FAQ

**Q: Do I need an internet connection?**
A: Only for initial package installation and model download. After that, everything is local.

**Q: Can I add more verses later?**
A: Yes, add them to CSV and rerun `setup_vector_db.py`. Old data is preserved.

**Q: Is the database encrypted?**
A: It's a local SQLite database. For production, add encryption as needed.

**Q: Can I use this in a web application?**
A: Yes! See integration examples in VECTOR_DB_GUIDE.md

**Q: Why is embedding generation slow?**
A: It's CPU-intensive but one-time. Search queries are instant.

---

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Read VECTOR_DB_GUIDE.md for detailed explanations
3. Check that CSV file paths are correct
4. Ensure Python 3.8+ and sufficient RAM

---

## 🎓 Learning Path

1. **Now:** Complete the 5-step setup
2. **Next:** Read VECTOR_DB_GUIDE.md to understand the concepts
3. **Then:** Explore search_verses.py code to understand implementation
4. **Finally:** Integrate into your own applications

---

## Summary

You now have a **production-ready semantic search system** that can:
- ✅ Search 1340+ Tamil verses by meaning
- ✅ Find related verses instantly
- ✅ Power AI-based question answering
- ✅ Scale to larger datasets

**Total setup time: ~10 minutes**

Happy searching! 🔍📚
