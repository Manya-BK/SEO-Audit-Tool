# SEO Audit Tool

An automated SEO audit tool that crawls websites and produces comprehensive technical SEO reports with a Lighthouse-like scoring system.

## Features

- 🔍 **Web Crawling**: Uses Scrapy to crawl and discover pages on your website
- 🤖 **Dynamic Content Analysis**: Selenium integration for analyzing JavaScript-rendered content
- 📊 **Comprehensive SEO Checks**:
  - Title tags and meta descriptions
  - Heading structure (H1, H2)
  - Image alt attributes
  - URL structure and HTTPS
  - Canonical tags
  - Robots meta tags
  - HTML language attributes
  - Internal/external links
  - Page performance metrics
  - Mobile-friendliness
  - Structured data
  - Social media meta tags
- 🎯 **Lighthouse-like Scoring**: Each check is scored and contributes to an overall SEO score
- 📈 **Detailed Reports**: Generate beautiful HTML reports or JSON data for further analysis

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Chrome/Chromium** (required for Selenium):
   - The tool uses ChromeDriver which is automatically managed by `webdriver-manager`
   - Make sure you have Chrome or Chromium installed on your system

## Usage

### Basic Usage

```bash
python main.py https://example.com
```

### Advanced Options

```bash
# Crawl more pages
python main.py https://example.com --max-pages 50

# Skip Selenium analysis (faster, but less comprehensive)
python main.py https://example.com --no-selenium

# Generate only HTML report
python main.py https://example.com --format html

# Generate only JSON report
python main.py https://example.com --format json

# Custom output directory
python main.py https://example.com --output-dir my_reports
```

### Command Line Arguments

- `url` (required): Starting URL to audit
- `--max-pages`: Maximum number of pages to crawl (default: 10)
- `--no-selenium`: Skip Selenium analysis for faster execution
- `--headless`: Run browser in headless mode (default: True)
- `--output-dir`: Output directory for reports (default: reports)
- `--format`: Output format - html, json, or both (default: both)

## Output

The tool generates reports in the `reports/` directory (or your specified output directory):

- **HTML Report**: Beautiful, interactive HTML report with:
  - Overall SEO score
  - Summary statistics
  - Page-by-page analysis
  - Detailed check results with issues and recommendations
  - Color-coded scoring (green/yellow/red)

- **JSON Report**: Machine-readable JSON data for:
  - Further analysis
  - Integration with other tools
  - Automated processing

## SEO Checks Performed

### On-Page SEO
- ✅ Title tag presence and length (30-60 characters)
- ✅ Meta description presence and length (120-160 characters)
- ✅ H1 tag (exactly one per page)
- ✅ H2 tags for content structure
- ✅ Image alt attributes
- ✅ URL structure and length
- ✅ Canonical tags
- ✅ Robots meta tags
- ✅ HTML lang attribute

### Technical SEO
- ✅ HTTPS usage
- ✅ Page load time
- ✅ Mobile-friendliness (viewport meta tag)
- ✅ Structured data (JSON-LD, microdata)
- ✅ Social media meta tags (Open Graph, Twitter Cards)

### Site Structure
- ✅ Internal linking
- ✅ External linking

## Scoring System

The tool uses a Lighthouse-like scoring system where:
- Each check has a maximum score
- Scores are calculated based on best practices
- Overall score is a percentage (0-100)
- Color coding:
  - 🟢 Green: Passed (100% of points)
  - 🟡 Yellow: Warning (50-99% of points)
  - 🔴 Red: Failed (<50% of points)

## Example Output

```
============================================================
     SEO Audit Tool - Automated Technical SEO Analysis
============================================================

[INFO] Starting crawl of https://example.com...
[INFO] Maximum pages to crawl: 10
[SUCCESS] Successfully crawled 10 pages
[INFO] Analyzing pages with Selenium...
[SUCCESS] Selenium analysis complete
[INFO] Performing SEO audit...
[SUCCESS] Overall SEO Score: 85.5/100
[INFO] Generating reports...
[SUCCESS] HTML report saved: reports/seo_audit_20231215_143022.html
[SUCCESS] JSON report saved: reports/seo_audit_20231215_143022.json

============================================================
[SUCCESS] Audit Complete!
============================================================

Overall Score: 85.5/100
Pages Analyzed: 10

Reports saved to:
  reports/seo_audit_20231215_143022.html
  reports/seo_audit_20231215_143022.json
```

## Requirements

- Python 3.7+
- Chrome/Chromium browser
- Internet connection

## Dependencies

- `scrapy`: Web crawling framework
- `selenium`: Browser automation
- `beautifulsoup4`: HTML parsing
- `webdriver-manager`: Automatic ChromeDriver management
- `jinja2`: HTML template rendering
- `colorama`: Colored terminal output
- `pandas`: Data manipulation (for future enhancements)

## Limitations

- The tool respects `robots.txt` by default
- Rate limiting is applied to be respectful to servers
- Selenium analysis can be slow for large sites (use `--no-selenium` for faster scans)
- Some dynamic content may require additional wait time

## Future Enhancements

- [ ] Export to PDF
- [ ] Comparison reports (before/after)
- [ ] Scheduled audits
- [ ] Email notifications
- [ ] API endpoint for programmatic access
- [ ] More advanced performance metrics
- [ ] Core Web Vitals analysis
- [ ] Accessibility checks

## License

This project is open source and available for use and modification.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues, questions, or suggestions, please open an issue on the repository.

