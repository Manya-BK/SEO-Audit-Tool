import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from main import run_audit

st.set_page_config(
    page_title="SEO Copilot",
    page_icon="🚀",
    layout="wide"
)

# Header
st.title("🚀 SEO Copilot")
st.caption("AI-Powered SEO Audit Tool")

# URL Input + Button
col1, col2 = st.columns([5, 1])

with col1:
    url = st.text_input(
        "Website URL",
        placeholder="https://example.com"
    )

with col2:
    st.write("")
    st.write("")
    run_button = st.button("Run Audit", use_container_width=True)

# Run Audit
if run_button:

    if not url:
        st.warning("Please enter a website URL.")
        st.stop()

    with st.spinner("Running SEO Audit..."):
        results = run_audit(
            url,
            max_pages=3
        )

    if results:

        st.success("Audit Complete!")

        from datetime import datetime

        st.caption(
            f"Scanned on {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
        )

        # Dashboard Layout
        col1, col2, col3, col4 = st.columns([1.3, 1, 1, 1])
        with col1:

            score = float(results["overall_score"])

            st.subheader("SEO Score")

            # Circular Donut / Gauge implementation
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={
                    "font": {"size": 45, "color": "white"},
                    "suffix": "/100"
                },
                gauge={
                    "axis": {"range": [0, 100], "visible": False},
                    "bar": {"color": "#22c55e", "thickness": 0.15}, # Active ring color
                    "bgcolor": "#1f2937", # Track color
                    "borderwidth": 0,
                }
            ))

            fig.update_layout(
                height=250, # Matches the height of the metric cards perfectly
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="main_seo_circular"
            )
            
            if score >= 80:
                st.success("Excellent")
            elif score >= 60:
                st.warning("Needs Improvement")
            else:
                st.error("Poor")

        # Custom Cards with min-height matching
        with col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #111827, #1e293b);
                padding: 25px;
                border-radius: 20px;
                border: 1px solid #1f2937;
                min-height: 250px;
                box-shadow: 0 0 15px rgba(59,130,246,0.25);
                margin-bottom: 15px;
            ">
                <div style="
                    width: 50px; height: 50px;
                    background: #2563eb; border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 24px;
                ">📄</div>
                <h4 style="margin-top: 15px; margin-bottom: 5px; color: #9ca3af;">Pages Analyzed</h4>
                <h1 style="margin: 0; font-size: 2.5rem;">{results["total_pages"]}</h1>
                <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 14px;">Pages Crawled</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #111827, #1e293b);
                padding: 25px;
                border-radius: 20px;
                border: 1px solid #1f2937;
                min-height: 250px;
                box-shadow: 0 0 15px rgba(249,115,22,0.25);
                margin-bottom: 15px;
            ">
                <div style="
                    width: 50px; height: 50px;
                    background: #ea580c; border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 24px;
                ">⚠️</div>
                <h4 style="margin-top: 15px; margin-bottom: 5px; color: #9ca3af;">Issues Found</h4>
                <h1 style="margin: 0; font-size: 2.5rem;">{results.get("total_issues",0)}</h1>
                <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 14px;">SEO Problems</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #111827, #1e293b);
                padding: 25px;
                border-radius: 20px;
                border: 1px solid #1f2937;
                min-height: 250px;
                box-shadow: 0 0 15px rgba(34,197,94,0.25);
                margin-bottom: 15px;
            ">
                <div style="
                    width: 50px; height: 50px;
                    background: #16a34a; border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 24px;
                ">🛡️</div>
                <h4 style="margin-top: 15px; margin-bottom: 5px; color: #9ca3af;">Website Status</h4>
                <h1 style="margin: 0; font-size: 2.5rem; color: #22c55e;">Good</h1>
                <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 14px;">Overall Health</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Score Breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Score Breakdown")
            labels = ["On-Page SEO", "Technical SEO", "Content Quality", "Accessibility", "Performance"]
            values = [25, 20, 12, 10, 11]

            fig = px.pie(values=values, names=labels, hole=0.55)
            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )
            st.plotly_chart(fig, use_container_width=True, key="score_breakdown")

        with col2:
            st.subheader("Audit Summary")
            c1, c2 = st.columns(2)
            with c1:
                st.success("✅ Passed\n\n68")
            with c2:
                st.warning("⚠️ Warnings\n\n12")

            c3, c4 = st.columns(2)
            with c3:
                st.error("❌ Failed\n\n8")
            with c4:
                st.info("📄 Total Checks\n\n88")

        st.divider()
        st.subheader("Category Scores")

        cat1, cat2, cat3, cat4, cat5 = st.columns(5)
        categories = [
            ("On-Page SEO", 85, "Good"),
            ("Technical SEO", 80, "Good"),
            ("Content Quality", 75, "Good"),
            ("Accessibility", 65, "Needs Improvement"),
            ("Performance", 60, "Needs Improvement")
        ]
        cols = [cat1, cat2, cat3, cat4, cat5]

        for col, (title, score, status) in zip(cols, categories):
            with col:
                st.markdown(f"""
                <div style="background:#1e293b; padding:15px; border-radius:15px; text-align:center;">
                    <h5 style="margin:0;">{title}</h5>
                </div>
                """, unsafe_allow_html=True)

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    number={"suffix": "%", "font": {"size": 24}},
                    gauge={
                        "axis": {"range": [0, 100], "visible": False},
                        "bar": {"color": "#2563eb", "thickness": 0.25},
                        "bgcolor": "white",
                        "borderwidth": 0,
                        "steps": [{"range": [0, 100], "color": "#f3f4f6"}]
                    }
                ))
                fig.update_layout(
                    height=140,
                    margin=dict(l=5, r=5, t=10, b=5),
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig, use_container_width=True, key=f"cat_{title}")

                if score >= 80:
                    st.success(status)
                elif score >= 70:
                    st.warning(status)
                else:
                    st.error(status)

        # Detailed Score Breakdown
        st.divider()
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Detailed Score Breakdown")
            table_data = {
                "Check": ["Title Tag", "Meta Description", "H1 Tag", "Meta Robots", "Canonical Tag", "XML Sitemap", "Robots.txt", "Image Alt Text"],
                "Category": ["On-Page SEO", "On-Page SEO", "On-Page SEO", "Technical SEO", "Technical SEO", "Technical SEO", "Technical SEO", "Content Quality"],
                "Status": ["Passed", "Passed", "Passed", "Passed", "Failed", "Passed", "Passed", "Warning"],
                "Points": ["10/10", "10/10", "10/10", "5/5", "0/5", "5/5", "5/5", "3/5"]
            }
            st.dataframe(table_data, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("Pass / Warning / Fail Distribution")
            fig = px.pie(
                values=[68, 12, 8],
                names=["Passed", "Warnings", "Failed"],
                hole=0.65,
                color_discrete_sequence=["#22c55e", "#eab308", "#ef4444"]
            )
            fig.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="distribution_chart")

        # Core Web Vitals
        st.divider()
        st.subheader("Core Web Vitals (Performance)")
        v1, v2, v3, v4, v5 = st.columns(5)
        with v1:
            st.metric("LCP", "1.8s")
            st.progress(85)
            st.success("Good")
        with v2:
            st.metric("CLS", "0.05")
            st.progress(90)
            st.success("Good")
        with v3:
            st.metric("INP", "120 ms")
            st.progress(88)
            st.success("Good")
        with v4:
            st.metric("FCP", "1.2s")
            st.progress(82)
            st.success("Good")
        with v5:
            st.metric("TTFB", "0.6s")
            st.progress(84)
            st.success("Good")

        # --- SMART DYNAMIC TOP PAGES SECTION ---
        st.divider()
        st.subheader("Top Pages Analyzed")
        
        dynamic_pages = []
        
        # Check standard dictionary keys where your page information list usually lives
        pages_list = results.get("pages") or results.get("pages_data") or results.get("detailed_results", [])
        
        if isinstance(pages_list, list) and len(pages_list) > 0:
            for page in pages_list:
                page_url = page.get("url") if isinstance(page, dict) else getattr(page, 'url', str(page))
                
                # Intelligent status validation based on findings rather than general score limits
                has_issues = False
                if isinstance(page, dict):
                    if page.get("error") or not page.get("title") or not page.get("meta_description"):
                        has_issues = True

                dynamic_pages.append({
                    "Page": page_url,
                    "Status": "Warning" if has_issues else "Passed",
                    "SEO Score": f"{page.get('score', results['overall_score'])}/100"
                })
        else:
            # Match fallback status to overall SEO grading boundaries
            if score >= 80:
                fallback_status = "Passed"
            elif score >= 60:
                fallback_status = "Warning"
            else:
                fallback_status = "Failed"
                
            dynamic_pages.append({
                "Page": url,
                "Status": fallback_status,
                "SEO Score": f"{score}/100"
            })
            
        st.dataframe(dynamic_pages, use_container_width=True, hide_index=True)
        # ----------------------------------------

        # Tech Stack
        st.divider()
        st.subheader("Technology Detected")
        t1, t2, t3, t4, t5, t6 = st.columns(6)
        t1.info("📊 Google Analytics")
        t2.info("☁️ Cloudflare")
        t3.info("⚡ jQuery")
        t4.info("🐘 PHP")
        t5.info("🟢 Nginx")
        t6.info("📚 Bootstrap")

        # Issues & Recommendations
        st.divider()
        col_issue, col_rec = st.columns(2)
        with col_issue:
            st.subheader("Top Issues To Fix")
            st.error("Missing Alt Text for Images")
            st.warning("Meta Description Missing")
            st.warning("Broken Internal Links")
            st.warning("Page Speed Needs Improvement")
        with col_rec:
            st.subheader("AI Recommendations")
            st.info("Add descriptive alt text to images.")
            st.info("Add a compelling meta description.")
            st.info("Improve page speed and optimize assets.")
            st.info("Fix broken internal links.")