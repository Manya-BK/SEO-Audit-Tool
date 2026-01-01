"""
SEO audit checks and scoring system
"""
from urllib.parse import urlparse
import re


class SEOAuditor:
    def __init__(self):
        self.checks = []
        
    def audit_page(self, page_data, selenium_data=None):
        """Perform comprehensive SEO audit on a page"""
        url = page_data.get('url', '')
        results = {
            'url': url,
            'checks': {},
            'score': 0,
            'max_score': 0,
        }
        
        # Title checks
        title_results = self._check_title(page_data)
        results['checks']['title'] = title_results
        results['score'] += title_results['score']
        results['max_score'] += title_results['max_score']
        
        # Meta description checks
        meta_desc_results = self._check_meta_description(page_data)
        results['checks']['meta_description'] = meta_desc_results
        results['score'] += meta_desc_results['score']
        results['max_score'] += meta_desc_results['max_score']
        
        # Heading checks
        heading_results = self._check_headings(page_data)
        results['checks']['headings'] = heading_results
        results['score'] += heading_results['score']
        results['max_score'] += heading_results['max_score']
        
        # Image checks
        image_results = self._check_images(page_data)
        results['checks']['images'] = image_results
        results['score'] += image_results['score']
        results['max_score'] += image_results['max_score']
        
        # URL checks
        url_results = self._check_url(url)
        results['checks']['url'] = url_results
        results['score'] += url_results['score']
        results['max_score'] += url_results['max_score']
        
        # Canonical checks
        canonical_results = self._check_canonical(page_data)
        results['checks']['canonical'] = canonical_results
        results['score'] += canonical_results['score']
        results['max_score'] += canonical_results['max_score']
        
        # Robots meta checks
        robots_results = self._check_robots(page_data)
        results['checks']['robots'] = robots_results
        results['score'] += robots_results['score']
        results['max_score'] += robots_results['max_score']
        
        # Language checks
        lang_results = self._check_language(page_data)
        results['checks']['language'] = lang_results
        results['score'] += lang_results['score']
        results['max_score'] += lang_results['max_score']
        
        # Link checks
        link_results = self._check_links(page_data)
        results['checks']['links'] = link_results
        results['score'] += link_results['score']
        results['max_score'] += link_results['max_score']
        
        # Performance checks (if Selenium data available)
        if selenium_data:
            perf_results = self._check_performance(selenium_data)
            results['checks']['performance'] = perf_results
            results['score'] += perf_results['score']
            results['max_score'] += perf_results['max_score']
            
            # Mobile-friendly checks
            mobile_results = self._check_mobile(selenium_data)
            results['checks']['mobile'] = mobile_results
            results['score'] += mobile_results['score']
            results['max_score'] += mobile_results['max_score']
            
            # Structured data checks
            structured_results = self._check_structured_data(selenium_data)
            results['checks']['structured_data'] = structured_results
            results['score'] += structured_results['score']
            results['max_score'] += structured_results['max_score']
        
        # Calculate percentage score
        if results['max_score'] > 0:
            results['score_percentage'] = round((results['score'] / results['max_score']) * 100, 2)
        else:
            results['score_percentage'] = 0
            
        return results
    
    def _check_title(self, page_data):
        """Check title tag"""
        title = page_data.get('title', '').strip()
        max_score = 10
        score = 0
        issues = []
        recommendations = []
        
        if not title:
            issues.append('Missing title tag')
            recommendations.append('Add a descriptive title tag')
        else:
            score += 5
            length = len(title)
            if 30 <= length <= 60:
                score += 5
            elif length < 30:
                score += 3
                issues.append(f'Title too short ({length} characters)')
                recommendations.append('Expand title to 30-60 characters')
            else:
                score += 2
                issues.append(f'Title too long ({length} characters)')
                recommendations.append('Shorten title to 60 characters or less')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'value': title,
        }
    
    def _check_meta_description(self, page_data):
        """Check meta description"""
        meta_desc = page_data.get('meta_description', '').strip()
        max_score = 10
        score = 0
        issues = []
        recommendations = []
        
        if not meta_desc:
            issues.append('Missing meta description')
            recommendations.append('Add a compelling meta description')
        else:
            score += 5
            length = len(meta_desc)
            if 120 <= length <= 160:
                score += 5
            elif length < 120:
                score += 3
                issues.append(f'Meta description too short ({length} characters)')
                recommendations.append('Expand meta description to 120-160 characters')
            else:
                score += 2
                issues.append(f'Meta description too long ({length} characters)')
                recommendations.append('Shorten meta description to 160 characters or less')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'value': meta_desc,
        }
    
    def _check_headings(self, page_data):
        """Check heading structure"""
        h1_tags = page_data.get('h1_tags', [])
        h2_tags = page_data.get('h2_tags', [])
        max_score = 10
        score = 0
        issues = []
        recommendations = []
        
        # Check H1
        h1_count = len([h for h in h1_tags if h.strip()])
        if h1_count == 0:
            issues.append('Missing H1 tag')
            recommendations.append('Add exactly one H1 tag per page')
        elif h1_count == 1:
            score += 5
        else:
            score += 2
            issues.append(f'Multiple H1 tags found ({h1_count})')
            recommendations.append('Use only one H1 tag per page')
        
        # Check H2 structure
        h2_count = len([h for h in h2_tags if h.strip()])
        if h2_count > 0:
            score += 5
        else:
            issues.append('No H2 tags found')
            recommendations.append('Add H2 tags to structure your content')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'h1_count': h1_count,
            'h2_count': h2_count,
        }
    
    def _check_images(self, page_data):
        """Check image alt attributes"""
        images = page_data.get('images', [])
        max_score = 10
        score = 0
        issues = []
        recommendations = []
        
        if not images:
            issues.append('No images found on page')
            return {
                'score': 0,
                'max_score': max_score,
                'issues': issues,
                'recommendations': recommendations,
                'total_images': 0,
                'images_with_alt': 0,
            }
        
        images_with_alt = 0
        for img in images:
            if img.get('alt', '').strip():
                images_with_alt += 1
        
        total_images = len(images)
        alt_percentage = (images_with_alt / total_images * 100) if total_images > 0 else 0
        
        if alt_percentage == 100:
            score = max_score
        elif alt_percentage >= 80:
            score = 7
            issues.append(f'{total_images - images_with_alt} images missing alt text')
            recommendations.append('Add alt text to all images')
        elif alt_percentage >= 50:
            score = 4
            issues.append(f'{total_images - images_with_alt} images missing alt text')
            recommendations.append('Add alt text to all images')
        else:
            score = 2
            issues.append(f'{total_images - images_with_alt} images missing alt text')
            recommendations.append('Add descriptive alt text to all images')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'total_images': total_images,
            'images_with_alt': images_with_alt,
            'alt_percentage': round(alt_percentage, 2),
        }
    
    def _check_url(self, url):
        """Check URL structure"""
        max_score = 10
        score = 0
        issues = []
        recommendations = []
        
        parsed = urlparse(url)
        path = parsed.path
        
        # Check URL length
        if len(url) <= 100:
            score += 3
        else:
            issues.append('URL too long')
            recommendations.append('Keep URLs under 100 characters')
        
        # Check for HTTPS
        if parsed.scheme == 'https':
            score += 4
        else:
            issues.append('URL not using HTTPS')
            recommendations.append('Use HTTPS for security and SEO')
        
        # Check for clean URL structure
        if not re.search(r'[?&]', path):
            score += 3
        else:
            issues.append('URL contains query parameters')
            recommendations.append('Use clean URLs without unnecessary parameters')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'url': url,
        }
    
    def _check_canonical(self, page_data):
        """Check canonical tag"""
        canonical = page_data.get('canonical', '').strip()
        max_score = 5
        score = 0
        issues = []
        recommendations = []
        
        if canonical:
            score = max_score
        else:
            issues.append('Missing canonical tag')
            recommendations.append('Add a canonical tag to prevent duplicate content issues')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'value': canonical,
        }
    
    def _check_robots(self, page_data):
        """Check robots meta tag"""
        robots = page_data.get('robots_meta', '').strip()
        max_score = 5
        score = max_score
        issues = []
        recommendations = []
        
        if robots and 'noindex' in robots.lower():
            score = 0
            issues.append('Page has noindex directive')
            recommendations.append('Remove noindex if page should be indexed')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'value': robots,
        }
    
    def _check_language(self, page_data):
        """Check HTML lang attribute"""
        html_lang = page_data.get('html_lang', '').strip()
        max_score = 5
        score = 0
        issues = []
        recommendations = []
        
        if html_lang:
            score = max_score
        else:
            issues.append('Missing HTML lang attribute')
            recommendations.append('Add lang attribute to HTML tag')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'value': html_lang,
        }
    
    def _check_links(self, page_data):
        """Check internal/external links"""
        links = page_data.get('links', [])
        max_score = 5
        score = 0
        issues = []
        recommendations = []
        
        internal_links = [l for l in links if not l.get('is_external', False)]
        external_links = [l for l in links if l.get('is_external', False)]
        
        if len(internal_links) > 0:
            score += 3
        else:
            issues.append('No internal links found')
            recommendations.append('Add internal links to improve site structure')
        
        if len(external_links) > 0:
            score += 2
        else:
            issues.append('No external links found')
            recommendations.append('Consider adding relevant external links')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'internal_links': len(internal_links),
            'external_links': len(external_links),
        }
    
    def _check_performance(self, selenium_data):
        """Check page performance"""
        max_score = 15
        score = 0
        issues = []
        recommendations = []
        
        load_time = selenium_data.get('load_time')
        if load_time is None:
            return {
                'score': 0,
                'max_score': max_score,
                'issues': ['Could not measure load time'],
                'recommendations': [],
            }
        
        if load_time < 2:
            score = max_score
        elif load_time < 3:
            score = 12
        elif load_time < 4:
            score = 8
            issues.append(f'Page load time is {load_time:.2f}s (target: <2s)')
            recommendations.append('Optimize page load time by minifying CSS/JS, optimizing images')
        else:
            score = 4
            issues.append(f'Page load time is {load_time:.2f}s (target: <2s)')
            recommendations.append('Significantly optimize page load time')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
            'load_time': round(load_time, 2),
        }
    
    def _check_mobile(self, selenium_data):
        """Check mobile-friendliness"""
        max_score = 10
        score = 0
        issues = []
        recommendations = []
        
        if selenium_data.get('mobile_friendly'):
            score += 5
        else:
            issues.append('Missing viewport meta tag')
            recommendations.append('Add viewport meta tag for mobile responsiveness')
        
        if selenium_data.get('has_social_meta'):
            score += 5
        else:
            issues.append('Missing social media meta tags')
            recommendations.append('Add Open Graph and Twitter Card meta tags')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
        }
    
    def _check_structured_data(self, selenium_data):
        """Check for structured data"""
        max_score = 10
        score = 0
        issues = []
        recommendations = []
        
        if selenium_data.get('has_structured_data'):
            score = max_score
        else:
            issues.append('No structured data found')
            recommendations.append('Add structured data (JSON-LD) to help search engines understand your content')
        
        return {
            'score': score,
            'max_score': max_score,
            'issues': issues,
            'recommendations': recommendations,
        }
    
    def audit_site(self, pages_data, selenium_data_dict=None):
        """Audit entire site"""
        site_results = {
            'pages': [],
            'overall_score': 0,
            'total_pages': len(pages_data),
        }
        
        total_score = 0
        total_max_score = 0
        
        for page_data in pages_data:
            url = page_data.get('url')
            selenium_data = selenium_data_dict.get(url) if selenium_data_dict else None
            page_result = self.audit_page(page_data, selenium_data)
            site_results['pages'].append(page_result)
            total_score += page_result['score']
            total_max_score += page_result['max_score']
        
        if total_max_score > 0:
            site_results['overall_score'] = round((total_score / total_max_score) * 100, 2)
        else:
            site_results['overall_score'] = 0
        
        return site_results

