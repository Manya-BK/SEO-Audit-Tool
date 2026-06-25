"""
SEO Auditor module - Dynamically analyzes collected page matrices
"""

class SEOAuditor:
    def __init__(self):
        pass

    def audit_page(self, page_data, selenium_data):
        """Processes evaluations and captures dynamic parameters safely."""
        results = {
            "url": page_data.get("url", "Unknown URL"),
            "score": 0,
            "max_score": 0,
            "issues": [],
            "technologies": []
        }

        # 1. Parse Technologies
        detected = selenium_data.get("detected_technologies") or selenium_data.get("technologies") or page_data.get("technologies")
        if detected and isinstance(detected, list):
            results["technologies"] = detected
        else:
            results["technologies"] = ["HTML5", "CSS3", "JavaScript"]

        # 2. Check Meta Title
        results["max_score"] += 20
        title_val = page_data.get("title") or page_data.get("meta_title")
        if title_val:
            results["score"] += 20
            if len(title_val) > 60:
                results["issues"].append(f"Meta Title is too long ({len(title_val)} chars). Truncation might occur.")
        else:
            results["issues"].append("Missing Meta Title tag configuration.")

        # 3. Check Meta Description (Fixing the repetitive fallback bug)
        results["max_score"] += 20
        desc_val = page_data.get("description") or page_data.get("meta_description") or selenium_data.get("description")
        if desc_val:
            results["score"] += 20
            if len(desc_val) < 50:
                results["issues"].append("Meta Description text is too short for search snippet indexation optimization.")
        else:
            results["issues"].append("Missing Meta Description structural tag attributes.")

        # 4. Check H1 Headings Hierarchy
        results["max_score"] += 20
        
        # Pull h1 directly, check within a nested headings dict, or handle fallbacks cleanly
        h1_val = page_data.get("h1")
        if not h1_val and "headings" in page_data:
            headings_data = page_data["headings"]
            if isinstance(headings_data, dict):
                h1_val = headings_data.get("h1") or headings_data.get("H1")
            elif isinstance(headings_data, list):
                h1_val = headings_data

        if h1_val:
            results["score"] += 20
            if len(h1_val) > 1 if isinstance(h1_val, list) else False:
                results["issues"].append("Multiple H1 tags detected on this resource link sheet layout context.")
        else:
            results["issues"].append("Missing foundational H1 primary semantic heading marker element.")

        return results

    def audit_site(self, pages_data, selenium_data):
        """Compiles complete site metric array dictionary packages."""
        total_score = 0
        total_max_score = 0
        compiled_page_records = []
        global_issues_list = []

        for page in pages_data:
            page_url = page.get("url")
            specific_selenium_context = {}
            if isinstance(selenium_data, dict):
                specific_selenium_context = selenium_data.get(page_url, {})

            page_audit = self.audit_page(page, specific_selenium_context)
            compiled_page_records.append(page_audit)
            
            total_score += page_audit["score"]
            total_max_score += page_audit["max_score"]
            if page_audit["issues"]:
                global_issues_list.extend(page_audit["issues"])

        overall_score = int((total_score / total_max_score) * 100) if total_max_score > 0 else 100
        unique_issues = list(set(global_issues_list))

        ai_suggestions = []
        for issue in unique_issues:
            if "Title" in issue:
                ai_suggestions.append("Rewrite title structures to stay between 50-60 characters.")
            elif "Description" in issue:
                ai_suggestions.append("Incorporate primary keywords inside your page descriptions map attributes.")
            # Clean matching rule for heading structural errors:
            elif "H1" in issue or "heading" in issue:
                ai_suggestions.append("Add a single unique H1 tag to your page layout to establish a proper semantic content hierarchy.")
            else:
                ai_suggestions.append(f"Optimize configuration: Resolve layout problem statement element: '{issue}'")

        return {
            "overall_score": overall_score,
            "total_pages": len(pages_data),
            "total_issues": len(unique_issues),
            "pages_data": compiled_page_records,
            "top_issues": unique_issues if unique_issues else ["No critical structural errors found."],
            "ai_suggestions": ai_suggestions if ai_suggestions else ["Great job! Core parameters comply with best practices."]
        }