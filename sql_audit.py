# ============================================================
#  SQL Data Licensing Audit
#  Author: sapanagc
#  Purpose: Audit AI articles dataset using SQL queries
# ============================================================

import pandas as pd
import sqlite3

# ── Step 1: Load and Clean Data ──────────────────────────────
df = pd.read_csv("ai_articles_large.csv")

# Clean the data
df = df.drop_duplicates(subset=["article_id"])
df["author"] = df["author"].fillna("Unknown")
df["license_type"] = df["license_type"].fillna("UNLICENSED")
df["published_date"] = pd.to_datetime(df["published_date"])

print("=" * 55)
print("  STEP 1: DATA LOADED & CLEANED")
print("=" * 55)
print(f"Shape after cleaning: {df.shape}")

# ── Step 2: Load into SQL Database ───────────────────────────
conn = sqlite3.connect(":memory:")
df.to_sql("articles", conn, index=False, if_exists="replace")
print("\n✅ Data loaded into SQL database")

# ── Step 3: License Type Breakdown ───────────────────────────
print("\n" + "=" * 55)
print("  STEP 3: LICENSE TYPE BREAKDOWN")
print("=" * 55)

license_breakdown = pd.read_sql("""
    SELECT license_type, 
           COUNT(*) as article_count,
           ROUND(AVG(word_count), 0) as avg_word_count
    FROM articles
    GROUP BY license_type
    ORDER BY article_count DESC
""", conn)
print(license_breakdown)

# ── Step 4: Articles Safe for AI Training ────────────────────
print("\n" + "=" * 55)
print("  STEP 4: ARTICLES SAFE FOR AI TRAINING")
print("=" * 55)

safe_articles = pd.read_sql("""
    SELECT title, source, license_type, word_count
    FROM articles
    WHERE license_type IN ('CC-BY', 'MIT', 'Apache-2.0')
    AND word_count > 500
    ORDER BY word_count DESC
""", conn)
print(f"Safe articles for AI training: {len(safe_articles)}")
print(safe_articles.head(10))

# ── Step 5: Problem Articles ──────────────────────────────────
print("\n" + "=" * 55)
print("  STEP 5: PROBLEM ARTICLES")
print("=" * 55)

# Unlicensed articles
unlicensed = pd.read_sql("""
    SELECT title, source, word_count
    FROM articles
    WHERE license_type = 'UNLICENSED'
    ORDER BY word_count DESC
""", conn)
print(f"\nUnlicensed articles (cannot use): {len(unlicensed)}")
print(unlicensed.head(5))

# Low word count articles
low_words = pd.read_sql("""
    SELECT title, license_type, word_count
    FROM articles
    WHERE word_count < 500
    ORDER BY word_count ASC
""", conn)
print(f"\nLow word count articles (<500 words): {len(low_words)}")
print(low_words)

# ── Step 6: Topic Analysis ────────────────────────────────────
print("\n" + "=" * 55)
print("  STEP 6: TOPIC ANALYSIS (CC-BY only)")
print("=" * 55)

topic_analysis = pd.read_sql("""
    SELECT topic,
           COUNT(*) as article_count,
           ROUND(AVG(word_count), 0) as avg_word_count,
           MIN(word_count) as min_words,
           MAX(word_count) as max_words
    FROM articles
    WHERE license_type = 'CC-BY'
    GROUP BY topic
    ORDER BY avg_word_count DESC
""", conn)
print(topic_analysis)

# ── Step 7: Country & Language Breakdown ─────────────────────
print("\n" + "=" * 55)
print("  STEP 7: COUNTRY & LANGUAGE BREAKDOWN")
print("=" * 55)

country_breakdown = pd.read_sql("""
    SELECT country, language,
           COUNT(*) as article_count,
           ROUND(AVG(word_count), 0) as avg_word_count
    FROM articles
    GROUP BY country, language
    ORDER BY article_count DESC
""", conn)
print(country_breakdown.head(10))

# ── Step 8: Audit Summary ─────────────────────────────────────
print("\n" + "=" * 55)
print("  STEP 8: AUDIT SUMMARY")
print("=" * 55)

summary = pd.read_sql("""
    SELECT 
        COUNT(*) as total_articles,
        SUM(CASE WHEN license_type IN ('CC-BY','MIT','Apache-2.0') 
                 AND word_count > 500 THEN 1 ELSE 0 END) as safe_for_training,
        SUM(CASE WHEN license_type = 'UNLICENSED' THEN 1 ELSE 0 END) as unlicensed,
        SUM(CASE WHEN license_type = 'Proprietary' THEN 1 ELSE 0 END) as proprietary,
        SUM(CASE WHEN word_count < 500 THEN 1 ELSE 0 END) as low_word_count
    FROM articles
""", conn)
print(summary)

# ── Step 9: Export Results ────────────────────────────────────
license_breakdown.to_csv("sql_license_breakdown.csv", index=False)
safe_articles.to_csv("sql_safe_articles.csv", index=False)
topic_analysis.to_csv("sql_topic_analysis.csv", index=False)

print("\n✅ SQL Audit complete! Reports exported.")
conn.close()
