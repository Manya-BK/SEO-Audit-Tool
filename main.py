"""
Main entry point for SEO Audit Tool
"""
import argparse
import sys
from colorama import init, Fore, Style
from seo_audit.crawler import Crawler
from seo_audit.selenium_analyzer import SeleniumAnalyzer
from seo_audit.auditor import SEOAuditor
from seo_audit.reporter import Reporter

# Imports needed for the Streamlit Twisted Reactor fix
from multiprocessing import Process, Queue

# Initialize colorama for Windows
init(autoreset=True)


def print_banner():
    """Print welcome banner"""
    banner = f"""
{Fore.CYAN}{'='*60}
{Fore.CYAN}     SEO Audit Tool - Automated Technical SEO Analysis
{Fore.CYAN}{'='*60}
{Style.RESET_ALL}
    """
    print(banner)


def print_progress(message, status='info'):
    """Print progress message with color"""
    colors = {
        'info': Fore.BLUE,
        'success': Fore.GREEN,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
    }
    color = colors.get(status, Fore.WHITE)
    print(f"{color}[{status.upper()}] {message}{Style.RESET_ALL}")

def _crawl_subprocess_worker(queue, url, max_pages):
    """
    Isolated worker function that runs inside a brand new process.
    This allows Scrapy/Twisted to start and exit completely cleanly.
    """
    try:
        # Instantiate and run the crawler inside this fresh process context
        crawler = Crawler(start_url=url, max_pages=max_pages)
        pages_data = crawler.crawl()
        queue.put({"success": True, "data": pages_data})
    except Exception as e:
        queue.put({"success": False, "error": str(e)})

def run_audit(url, max_pages=3):
    """
    Safe wrapper execution for Streamlit interface to prevent 
    twisted.internet.error.ReactorNotRestartable
    """
    queue = Queue()
    
    # Spawn the crawl workflow inside a separate isolated sub-process
    process = Process(target=_crawl_subprocess_worker, args=(queue, url, max_pages))
    process.start()
    process.join()  # Wait for the crawling worker thread block to finish
    
    result = queue.get()
    
    if not result["success"]:
        print_progress(f"Subprocess crawl failed: {result['error']}", 'error')
        return None
        
    pages_data = result["data"]

    if not pages_data:
        return None

    auditor = SEOAuditor()

    # Pass empty dict for selenium_data during UI execution to match previous behavior
    audit_results = auditor.audit_site(
        pages_data,
        {}
    )

    return audit_results

def main():
    parser = argparse.ArgumentParser(
        description='Automated SEO Audit Tool - Crawls sites and produces technical SEO reports'
    )
    parser.add_argument('url', help='Starting URL to audit')
    parser.add_argument(
        '--max-pages',
        type=int,
        default=10,
        help='Maximum number of pages to crawl (default: 10)'
    )
    parser.add_argument(
        '--no-selenium',
        action='store_true',
        help='Skip Selenium analysis (faster but less comprehensive)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run browser in headless mode (default: True)'
    )
    parser.add_argument(
        '--output-dir',
        default='reports',
        help='Output directory for reports (default: reports)'
    )
    parser.add_argument(
        '--format',
        choices=['html', 'json', 'both'],
        default='both',
        help='Output format (default: both)'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    try:
        # Step 1: Crawl the site
        print_progress(f'Starting crawl of {args.url}...', 'info')
        print_progress(f'Maximum pages to crawl: {args.max_pages}', 'info')
        
        crawler = Crawler(start_url=args.url, max_pages=args.max_pages)
        pages_data = crawler.crawl()
        
        if not pages_data:
            print_progress('No pages were crawled. Check the URL and try again.', 'error')
            sys.exit(1)
        
        print_progress(f'Successfully crawled {len(pages_data)} pages', 'success')
        
        # Step 2: Analyze with Selenium (if enabled)
        selenium_data = {}
        if not args.no_selenium:
            print_progress('Analyzing pages with Selenium...', 'info')
            selenium_analyzer = SeleniumAnalyzer(headless=args.headless)
            
            for i, page_data in enumerate(pages_data, 1):
                url = page_data.get('url')
                print_progress(f'Analyzing page {i}/{len(pages_data)}: {url}', 'info')
                analysis = selenium_analyzer.analyze_page(url)
                selenium_data[url] = analysis
            
            selenium_analyzer.close()
            print_progress('Selenium analysis complete', 'success')
        else:
            print_progress('Skipping Selenium analysis', 'warning')
        
        # Step 3: Perform SEO audit
        print_progress('Performing SEO audit...', 'info')
        auditor = SEOAuditor()
        audit_results = auditor.audit_site(pages_data, selenium_data)
        
        print_progress(f'Overall SEO Score: {audit_results["overall_score"]}/100', 'success')
        
        # Step 4: Generate reports
        print_progress('Generating reports...', 'info')
        reporter = Reporter(output_dir=args.output_dir)
        
        report_files = []
        
        if args.format in ['html', 'both']:
            html_file = reporter.generate_html_report(audit_results, args.url)
            report_files.append(html_file)
            print_progress(f'HTML report saved: {html_file}', 'success')
        
        if args.format in ['json', 'both']:
            json_file = reporter.generate_json_report(audit_results, args.url)
            report_files.append(json_file)
            print_progress(f'JSON report saved: {json_file}', 'success')
        
        # Summary
        print(f"\n{Fore.GREEN}{'='*60}")
        print_progress('Audit Complete!', 'success')
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        print(f"Overall Score: {Fore.CYAN}{audit_results['overall_score']}/100{Style.RESET_ALL}")
        print(f"Pages Analyzed: {Fore.CYAN}{audit_results['total_pages']}{Style.RESET_ALL}")
        print(f"\nReports saved to:")
        for file in report_files:
            print(f"  {Fore.YELLOW}{file}{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print_progress('\nAudit interrupted by user', 'warning')
        sys.exit(1)
    except Exception as e:
        print_progress(f'Error: {str(e)}', 'error')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()