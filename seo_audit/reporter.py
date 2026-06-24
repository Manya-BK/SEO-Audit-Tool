"""
Report generator for SEO audit results
"""
import json
from datetime import datetime
from jinja2 import Template
import os


class Reporter:
    def __init__(self, output_dir='reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_html_report(self, audit_results, site_url):
        """Generate HTML report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{self.output_dir}/seo_audit_{timestamp}.html'
        
        # Calculate summary statistics
        summary = self._calculate_summary(audit_results)
        
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Report - {{ site_url }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .header {
            border-bottom: 2px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }

        .header-top{
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            flex-wrap:wrap;
        }
        .download-btn{
            background:#2563eb;
            color:white;
            padding:12px 20px;
            border-radius:10px;
            text-decoration:none;
            font-weight:bold;
            border:none;
            cursor:pointer;
        }

        .download-btn:hover{
            background:#1d4ed8;
        }

        .site-url{
            color:#777;
            font-size:20px;
            margin-top:5px;
        }

        .header-date{
            color:#555;
            font-size:18px;
            font-weight:500;
        }

        .meta-info {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        .header-info{
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-top:20px;
            gap:20px;
            flex-wrap:wrap;
        }

        .site-url{
            color:#777;
            font-size:20px;
        }

        .header-date{
            color:#555;
            font-size:18px;
            font-weight:500;
        }

        .download-btn{
            background:#2563eb;
            color:white;
            padding:12px 24px;
            border-radius:10px;
            text-decoration:none;
            font-weight:600;
        }

        .download-btn:hover{
            background:#1d4ed8;
        }
        
        .score-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            margin: 30px auto;
            width: 420px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        .score-card h2 {
            margin-bottom: 20px;
            color: #2c3e50;
        }

        .score-circle {
            width: 240px;
        height: 240px;
        margin: 20px auto;
        border-radius: 50%;
        background:
        conic-gradient(
            #2563eb 0deg,
            #22c55e 180deg,
            #eab308 280deg,
            #f97316 320deg,
            #e5e7eb 320deg
        );
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        }

        .score-circle::before {
            content: "";
            width: 180px;
            height: 180px;
            background: white;
            border-radius: 50%;
            position: absolute;
        }

        .score-value {
            position: relative;
            z-index: 2;
            font-size: 55px;
            font-weight: bold;
        }

        .score-value span {
            display: block;
            font-size: 22px;
            color: gray;
        }

        .score-status {
            display: inline-block;
            background: #22c55e;
            color: white;
            padding: 8px 22px;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 15px;
        }

        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .summary-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
        .summary-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        .summary-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }
        .page-section {
            margin: 40px 0;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }
        .page-header {
            background: #34495e;
            color: white;
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .page-header:hover {
            background: #2c3e50;
        }
        .page-url {
            font-weight: bold;
            word-break: break-all;
        }
        .page-score {
            background: white;
            color: #2c3e50;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .page-content {
            padding: 20px;
            display: none;
        }
        .page-content.active {
            display: block;
        }
        .check-item {
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #95a5a6;
        }
        .check-item.passed {
            border-left-color: #27ae60;
        }
        .check-item.warning {
            border-left-color: #f39c12;
        }
        .check-item.failed {
            border-left-color: #e74c3c;
        }
        .check-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .check-name {
            font-weight: bold;
            font-size: 1.1em;
            color: #2c3e50;
        }
        .check-score {
            font-weight: bold;
            color: #7f8c8d;
        }
        .issues-list, .recommendations-list {
            margin-top: 10px;
        }
        .issues-list li {
            color: #e74c3c;
            margin: 5px 0;
        }
        .recommendations-list li {
            color: #27ae60;
            margin: 5px 0;
        }
        ul {
            list-style-position: inside;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 10px;
        }
        .badge-success {
            background: #27ae60;
            color: white;
        }
        .badge-warning {
            background: #f39c12;
            color: white;
        }
        .badge-danger {
            background: #e74c3c;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
    <div class="header">
        
        <h1>SEO Audit Report - {{ site_name }}</h1>

        <div class="header-info">
            <span class="site-url">{{ site_url }}</span>

            <span class="header-date">
                {{ timestamp }}
            </span>

            <button class="download-btn" onclick="window.print()">
                Download Report
            </button>
        </div>

    </div>

</div>
        
<div class="score-card">
    <h2>Overall SEO Score</h2>

    <div class="score-circle">
        <div class="score-value">
            {{ audit_results.overall_score }}
            <span>/100</span>
        </div>
    </div>

    <div class="score-status">
        Good
    </div>

    <p class="score-message">
        Your website is well-optimized!
    </p>
</div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Pages</h3>
                <div class="value">{{ summary.total_pages }}</div>
            </div>
            <div class="summary-card">
                <h3>Average Score</h3>
                <div class="value">{{ summary.average_score }}</div>
            </div>
            <div class="summary-card">
                <h3>Pages with Issues</h3>
                <div class="value">{{ summary.pages_with_issues }}</div>
            </div>
            <div class="summary-card">
                <h3>Total Issues</h3>
                <div class="value">{{ summary.total_issues }}</div>
            </div>
        </div>
        
        <h2 style="margin: 40px 0 20px 0; color: #2c3e50;">Page-by-Page Analysis</h2>
        
        {% for page in audit_results.pages %}
        <div class="page-section">
            <div class="page-header" onclick="togglePage({{ loop.index0 }})">
                <div class="page-url">{{ page.url }}</div>
                <div class="page-score">{{ page.score_percentage }}%</div>
            </div>
            <div class="page-content" id="page-{{ loop.index0 }}">
                {% for check_name, check_data in page.checks.items() %}
                <div class="check-item {{ 'passed' if check_data.score == check_data.max_score else 'warning' if check_data.score >= check_data.max_score * 0.5 else 'failed' }}">
                    <div class="check-header">
                        <span class="check-name">{{ check_name.replace('_', ' ').title() }}</span>
                        <span class="check-score">{{ check_data.score }}/{{ check_data.max_score }}</span>
                    </div>
                    {% if check_data.issues %}
                    <ul class="issues-list">
                        {% for issue in check_data.issues %}
                        <li>{{ issue }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                    {% if check_data.recommendations %}
                    <ul class="recommendations-list">
                        {% for rec in check_data.recommendations %}
                        <li>{{ rec }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
    
    <script>
        function togglePage(index) {
            const content = document.getElementById('page-' + index);
            content.classList.toggle('active');
        }
        
        // Expand first page by default
        document.addEventListener('DOMContentLoaded', function() {
            if (document.getElementById('page-0')) {
                document.getElementById('page-0').classList.add('active');
            }
        });
    </script>
</body>
</html>
        """
        
        site_name = site_url.replace("https://", "").replace("http://", "").replace("www.", "").split(".")[0].capitalize()

        template = Template(html_template)

        html_content = template.render(
            site_name=site_name,
            site_url=site_url,
            timestamp=datetime.now().strftime('%d %b %Y | %I:%M %p'),
            audit_results=audit_results,
            summary=summary
        )

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
    
    def generate_json_report(self, audit_results, site_url):
        """Generate JSON report"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{self.output_dir}/seo_audit_{timestamp}.json'

        report_data = {
            'site_url': site_url,
            'timestamp': datetime.now().isoformat(),
            'overall_score': audit_results['overall_score'],
            'total_pages': audit_results['total_pages'],
            'pages': audit_results['pages'],
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def _calculate_summary(self, audit_results):
        """Calculate summary statistics"""
        pages = audit_results.get('pages', [])
        total_pages = len(pages)
        
        if total_pages == 0:
            return {
                'total_pages': 0,
                'average_score': 0,
                'pages_with_issues': 0,
                'total_issues': 0,
            }
        
        total_score = sum(page.get('score_percentage', 0) for page in pages)
        average_score = round(total_score / total_pages, 2)
        
        pages_with_issues = 0
        total_issues = 0
        
        for page in pages:
            page_issues = 0
            for check_data in page.get('checks', {}).values():
                page_issues += len(check_data.get('issues', []))
            
            if page_issues > 0:
                pages_with_issues += 1
                total_issues += page_issues
        
        return {
            'total_pages': total_pages,
            'average_score': average_score,
            'pages_with_issues': pages_with_issues,
            'total_issues': total_issues,
        }