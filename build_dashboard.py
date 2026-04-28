import os
import re

# Read the markdown file
with open('nemo_eda_report.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Pattern to extract charts
charts_pattern = re.compile(
    r'### (.*?)\n'
    r'!\[.*?\]\((.*?)\)\n'
    r'.*?'
    r'\*\*분석 및 해석:\*\*\n(.*?)\n\n'
    r'\*\*해석 방법과 비즈니스 인사이트:\*\*\n(.*?)\n\n---',
    re.DOTALL
)

charts_data = charts_pattern.findall(md_content)

# Pattern to extract comprehensive insight
insights_pattern = re.compile(
    r'## 6\. 종합 인사이트 및 전략 제언\n(.*)',
    re.DOTALL
)
insights_match = insights_pattern.search(md_content)
insights_content = insights_match.group(1).strip() if insights_match else ""

# Convert markdown to html for the insights content
def md_to_html(text):
    text = text.replace('\n\n', '</p><p>')
    text = text.replace('**[비즈니스 실행 전략]**:', '<br><strong style="color:#38bdf8;">[비즈니스 실행 전략]:</strong>')
    text = text.replace('**[비즈니스 제언]**:', '<br><strong style="color:#38bdf8;">[비즈니스 제언]:</strong>')
    text = re.sub(r'### (.*?)\n', r'<h4>\1</h4>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return f'<p>{text}</p>'

html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>네모 앱 부동산 데이터 분석 대시보드</title>
    <link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard.css" rel="stylesheet" />
    <style>
        :root {{
            --bg-color: #0f172a;
            --text-color: #f8fafc;
            --accent-color: #38bdf8;
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }}
        body {{
            background-color: var(--bg-color); color: var(--text-color); line-height: 1.6;
            background-image: radial-gradient(circle at 15% 50%, rgba(56, 189, 248, 0.15), transparent 25%),
                              radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.15), transparent 25%);
            background-attachment: fixed;
        }}
        .glass {{
            background: var(--card-bg); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border); border-radius: 24px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }}
        .dashboard {{ display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }}
        .sidebar {{
            padding: 2rem; position: sticky; top: 0; height: 100vh; overflow-y: auto;
            border-right: 1px solid var(--card-border); background: rgba(15, 23, 42, 0.8);
        }}
        .sidebar h1 {{
            font-size: 1.5rem; margin-bottom: 2rem; font-weight: 700;
            background: linear-gradient(to right, #38bdf8, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .nav-links {{ list-style: none; }}
        .nav-links li {{ margin-bottom: 0.5rem; }}
        .nav-links a {{
            color: #94a3b8; text-decoration: none; display: block; padding: 0.75rem 1rem;
            border-radius: 12px; transition: all 0.3s ease; font-weight: 600;
        }}
        .nav-links a:hover, .nav-links a.active {{ background: rgba(56, 189, 248, 0.1); color: var(--accent-color); transform: translateX(5px); }}
        .main-content {{ padding: 2rem 4rem; overflow-x: hidden; }}
        .header {{ margin-bottom: 3rem; padding-bottom: 1rem; border-bottom: 1px solid var(--card-border); }}
        .header h2 {{ font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }}
        .header p {{ color: #94a3b8; font-size: 1.1rem; }}
        .insights-hero {{ padding: 3rem; margin-bottom: 4rem; position: relative; overflow: hidden; }}
        .insights-hero::before {{
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, #38bdf8, #8b5cf6, #ec4899);
        }}
        .insights-hero h3 {{ font-size: 1.8rem; margin-bottom: 1.5rem; color: #f1f5f9; }}
        .insights-hero h4 {{ color: var(--accent-color); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.3rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom:0.5rem;}}
        .insights-hero p {{ margin-bottom: 1.5rem; font-size: 1.05rem; color: #cbd5e1; }}
        .charts-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(600px, 1fr)); gap: 3rem; }}
        .chart-card {{ padding: 2rem; transition: transform 0.3s ease, box-shadow 0.3s ease; }}
        .chart-card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); border-color: rgba(56, 189, 248, 0.3); }}
        .chart-header {{ display: flex; align-items: center; margin-bottom: 1.5rem; }}
        .chart-number {{
            background: linear-gradient(135deg, #38bdf8, #8b5cf6); color: white; width: 32px; height: 32px;
            display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: bold; margin-right: 1rem; flex-shrink: 0;
        }}
        .chart-title {{ font-size: 1.4rem; font-weight: 600; }}
        .chart-image {{ width: 100%; border-radius: 16px; margin-bottom: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.05); background: white; }}
        .chart-insight {{ background: rgba(0, 0, 0, 0.2); padding: 1.5rem; border-radius: 16px; border-left: 4px solid var(--accent-color); }}
        .chart-insight h5 {{ color: var(--accent-color); margin-bottom: 0.5rem; font-size: 1.1rem; }}
        .chart-insight p {{ color: #cbd5e1; font-size: 0.95rem; margin-bottom:1rem; }}
        .badge {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; background: rgba(56, 189, 248, 0.2); color: #38bdf8; font-size: 0.8rem; font-weight: 600; margin-bottom: 1rem; }}
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: rgba(15, 23, 42, 0.8); }}
        ::-webkit-scrollbar-thumb {{ background: rgba(148, 163, 184, 0.3); border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(148, 163, 184, 0.5); }}
    </style>
</head>
<body>
    <div class="dashboard">
        <aside class="sidebar">
            <h1>NEMO INSIGHTS</h1>
            <ul class="nav-links">
                <li><a href="#summary" class="active">종합 인사이트</a></li>
"""

for i, (title, _, _, _) in enumerate(charts_data):
    html_template += f'                <li><a href="#chart-{i+1}">{title}</a></li>\n'

html_template += f"""            </ul>
        </aside>
        
        <main class="main-content">
            <header class="header">
                <h2>부동산 데이터 인사이트 대시보드</h2>
                <p>네모 앱 매물 데이터를 기반으로 한 다변량 분석 및 시장 전략 제언</p>
            </header>

            <section id="summary" class="insights-hero glass">
                <span class="badge">Executive Summary</span>
                <h3>종합 인사이트 및 전략 제언</h3>
                {md_to_html(insights_content)}
            </section>

            <div class="charts-grid">
"""

for i, (title, img_path, analysis, insight) in enumerate(charts_data):
    html_template += f"""
                <article id="chart-{i+1}" class="chart-card glass">
                    <div class="chart-header">
                        <div class="chart-number">{i+1}</div>
                        <h4 class="chart-title">{title}</h4>
                    </div>
                    <img src="{img_path}" alt="{title}" class="chart-image">
                    
                    <div class="chart-insight">
                        <h5>분석 및 해석</h5>
                        <p>{analysis.strip()}</p>
                        <h5>비즈니스 인사이트</h5>
                        <p>{insight.strip()}</p>
                    </div>
                </article>
"""

html_template += """
            </div>
        </main>
    </div>
    <script>
        // Simple active state for navigation
        const sections = document.querySelectorAll('section, article');
        const navLinks = document.querySelectorAll('.nav-links a');
        
        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                if (scrollY >= sectionTop - 100) {
                    current = section.getAttribute('id');
                }
            });
            
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href').includes(current)) {
                    link.classList.add('active');
                }
            });
        });
    </script>
</body>
</html>
"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("Dashboard created successfully!")
