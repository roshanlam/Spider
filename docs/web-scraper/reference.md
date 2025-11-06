# Web Scraper Plugin - Quick Reference Card

## ⚡ Quick Commands

### Run the Crawler
```bash
poetry run python -m spider.main
```

### Query Data (Python)
```python
from spider.plugins.scraper_utils import ScraperDataQuery, get_statistics

# Create query instance
q = ScraperDataQuery()

# Get statistics
stats = get_statistics()
print(f"Total pages: {stats['total_pages']}")

# Get page data
page = q.get_page_data("http://example.com")
print(page['title'], page['word_count'])

# Search
results = q.search_by_title("keyword")

# Export
q.export_to_json("http://example.com", "out.json")
```

### Query Data (Command Line)
```bash
# Statistics
poetry run python -c "from spider.plugins.scraper_utils import get_statistics; print(get_statistics())"

# List all pages
poetry run python -c "from spider.plugins.scraper_utils import ScraperDataQuery; q = ScraperDataQuery(); pages = q.get_all_pages(); [print(f'{p[\"url\"]}: {p[\"title\"]}') for p in pages]"
```

### Database Queries
```bash
# View all scraped pages
psql -d crawlerdb -c "SELECT url, title, word_count FROM scraped_data;"

# Count pages
psql -d crawlerdb -c "SELECT COUNT(*) FROM scraped_data;"

# Export to CSV
psql -d crawlerdb -c "COPY scraped_data TO '/tmp/export.csv' CSV HEADER;"
```

## 📊 What Gets Scraped

| Category | Data Points |
|----------|------------|
| **Basic** | Title, description, keywords, author, language |
| **Content** | Word count, headings (h1-h6), content blocks |
| **Links** | Internal/external links with anchor text |
| **Images** | URLs, alt text, dimensions |
| **Forms** | Actions, methods, input fields |
| **Social** | OpenGraph, Twitter Card metadata |
| **Structured** | JSON-LD schema.org data |

## 🔧 Configuration

Edit `src/spider/config.yaml`:
```yaml
start_url: "http://example.com"
rate_limit: 1
threads: 8
database:
  url: "postgresql://roshan@localhost/crawlerdb"
```

## 📁 Important Files

```
src/spider/plugins/
  ├── web_scraper_plugin.py    # Main plugin
  └── scraper_utils.py          # Query utilities

WEB_SCRAPER_PLUGIN.md          # Full documentation
QUICKSTART_WEB_SCRAPER.md      # Quick start guide
examples/web_scraper_example.py # Code examples
test_web_scraper_plugin.py     # Test suite
```

## 🚀 Common Use Cases

### SEO Analysis
```python
pages = q.get_all_pages()
for p in pages:
    if not p['description']: print(f"No desc: {p['url']}")
```

### Find Forms
```python
forms = q.get_pages_with_forms()
```

### Link Analysis
```python
internal = q.get_internal_links("http://example.com")
external = q.get_external_links("http://example.com")
```

### Export Data
```python
q.export_to_json(url, "output.json")
```

## 💡 Tips

- Always use `poetry run python -m spider.main` (not `python src/...`)
- For SSL errors, use HTTP URLs or fix certificates
- Check logs for errors: look for "Scraped" messages
- Data is stored in PostgreSQL `scraped_data` table
- Query utilities make data access easy

## 🆘 Troubleshooting

**Import Error**: Use `poetry run python -m spider.main`
**SSL Error**: Use HTTP URLs or fix certificates
**DB Error**: Check `psql -d crawlerdb -c "SELECT 1;"`
**No Data**: Run crawler first, then query

## 📚 Learn More

- Full docs: `WEB_SCRAPER_PLUGIN.md`
- Examples: `examples/web_scraper_example.py`
- Tests: `test_web_scraper_plugin.py`
