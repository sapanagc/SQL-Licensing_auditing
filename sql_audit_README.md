# 🗄️ SQL Data Licensing Audit

A SQL-based data quality audit on 150 AI research articles, built to simulate real database querying workflows at AI and data licensing companies.

---

## 📋 Project Summary

| Metric | Result |
|---|---|
| Total articles audited | 145 (after deduplication) |
| Safe for AI training ✅ | 79 articles |
| Unlicensed ❌ | 30 articles |
| Proprietary ⚠️ | 12 articles |
| Low word count (<500) | ~12 articles |

---

## 🔍 What The Audit Does

Uses SQL queries to answer 7 key business questions:

1. **License type breakdown** — how many articles per license?
2. **Safe articles for AI training** — CC-BY, MIT, Apache-2.0 with 500+ words
3. **Problem articles** — unlicensed and low word count
4. **Topic analysis** — average word count per topic (CC-BY only)
5. **Country & language breakdown** — geographic distribution
6. **Audit summary** — single row snapshot of dataset health
7. **Export results** — CSV reports for each analysis

---

## 🛠️ SQL Commands Used

| Command | Purpose |
|---|---|
| `SELECT` | Choose columns to return |
| `FROM` | Specify the table |
| `WHERE` | Filter rows by condition |
| `GROUP BY` | Group rows for aggregation |
| `ORDER BY DESC/ASC` | Sort results |
| `COUNT(*)` | Count rows per group |
| `AVG()` | Calculate average |
| `MIN() / MAX()` | Find smallest/largest value |
| `ROUND()` | Round decimals |
| `IN()` | Filter by multiple values |
| `CASE WHEN` | Conditional logic in SQL |

---

## 🛠️ Tech Stack

- Python 3
- pandas
- sqlite3 (in-memory database)

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/sapanagc/sql-licensing-audit.git
cd sql-licensing-audit
```

**2. Install dependencies**
```bash
pip install pandas
```

**3. Run the audit**
```bash
python sql_audit.py
```

**4. Check outputs**

Three CSV reports are generated:
- `sql_license_breakdown.csv` — license type summary
- `sql_safe_articles.csv` — articles approved for AI training
- `sql_topic_analysis.csv` — topic analysis for CC-BY articles

---

## 📊 Key Findings

**Only 54% of articles are safe for AI training** — the rest are either unlicensed, proprietary, or too short.

**Top topics by average word count (CC-BY only):**
- Regulation — 3,816 words avg
- Safety — 3,674 words avg
- Privacy — 3,478 words avg

**License breakdown:**
- CC-BY: 53 articles (best for AI training)
- UNLICENSED: 30 articles (cannot use)
- CC-BY-NC: 24 articles (non-commercial only)

---

## 🔗 Related Projects

- [data-licensing-audit](https://github.com/sapanagc/data-licensing-audit) — pandas-based audit tool
- [ai-articles-audit](https://github.com/sapanagc/ai-articles-audit) — full audit on 150-row dataset

---

## 👤 Author

**sapanagc** — Aspiring Data Licensing Analyst  
Learning Python · Pandas · SQL for AI data licensing roles  
github.com/sapanagc
