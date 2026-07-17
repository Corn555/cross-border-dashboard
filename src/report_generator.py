"""
模块：报告生成器
职责：将分析结果和图表整合为一份自包含的 HTML 报告。
"""
import os
import base64
from datetime import datetime


def _img_to_base64(path: str) -> str:
    """将图片文件编码为 base64 字符串，用于内嵌 HTML。"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_report(sales: dict, customers: dict, charts: list,
                    cleaning_stats: dict = None,
                    output_path: str = "output/reports/report.html") -> str:
    """
    生成自包含的 HTML 分析报告，内嵌所有图表。

    Args:
        sales: analyze_sales() 的返回结果。
        customers: analyze_customers() 的返回结果。
        charts: create_charts() 返回的图表文件路径列表。
        cleaning_stats: clean_data() 返回的清洗统计（可选）。
        output_path: 报告输出路径。

    Returns:
        str: 生成的 HTML 文件路径。
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 将图表转为 base64 内嵌
    chart_b64 = {}
    for path in charts:
        name = os.path.splitext(os.path.basename(path))[0]
        chart_b64[name] = _img_to_base64(path)

    # --- 构建 HTML ---
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>跨境电商销售数据分析报告</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", sans-serif;
    background: #f0f2f5; color: #333; line-height: 1.6;
  }}
  .container {{ max-width: 1000px; margin: 0 auto; padding: 30px 20px; }}
  .header {{
    background: linear-gradient(135deg, #1a3a5c 0%, #2c7bb6 100%);
    color: white; padding: 50px 40px; border-radius: 12px;
    margin-bottom: 30px; text-align: center;
  }}
  .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
  .header p {{ opacity: 0.85; font-size: 14px; }}
  .kpi-row {{
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 16px; margin-bottom: 30px;
  }}
  .kpi-card {{
    background: white; border-radius: 10px; padding: 24px 20px;
    text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }}
  .kpi-card .label {{ font-size: 13px; color: #888; margin-bottom: 6px; }}
  .kpi-card .value {{ font-size: 24px; font-weight: 700; color: #1a3a5c; }}
  .section {{
    background: white; border-radius: 10px; padding: 30px;
    margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }}
  .section h2 {{
    font-size: 20px; color: #1a3a5c; margin-bottom: 20px;
    padding-bottom: 10px; border-bottom: 2px solid #2c7bb6;
  }}
  .section img {{ width: 100%; border-radius: 6px; margin-top: 10px; }}
  table {{
    width: 100%; border-collapse: collapse; margin-top: 12px;
  }}
  th, td {{
    padding: 10px 14px; text-align: left;
    border-bottom: 1px solid #e8e8e8;
  }}
  th {{ background: #f7f8fa; font-weight: 600; color: #555; font-size: 13px; }}
  td {{ font-size: 14px; }}
  .highlight {{ color: #2c7bb6; font-weight: 600; }}
  .footer {{
    text-align: center; padding: 30px; color: #aaa; font-size: 13px;
  }}
  @media (max-width: 768px) {{
    .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
  }}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <h1>跨境电商销售数据分析报告</h1>
  <p>Cross-border E-commerce Sales Dashboard &bull; 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
</div>

<!-- KPI 卡片 -->
<div class="kpi-row">
  <div class="kpi-card">
    <div class="label">总营收</div>
    <div class="value">$ {sales["total_revenue"]:,.0f}</div>
  </div>
  <div class="kpi-card">
    <div class="label">总订单数</div>
    <div class="value">{sales["total_orders"]:,}</div>
  </div>
  <div class="kpi-card">
    <div class="label">总客户数</div>
    <div class="value">{customers["total_customers"]:,}</div>
  </div>
  <div class="kpi-card">
    <div class="label">平均客单价</div>
    <div class="value">$ {sales["avg_order_value"]:,.0f}</div>
  </div>
</div>
"""

    # 数据清洗摘要（如果有）
    if cleaning_stats:
        html += f"""
<div class="section">
  <h2>数据清洗摘要</h2>
  <table>
    <tr><td>清洗前行数</td><td class="highlight">{cleaning_stats.get("rows_before", "—"):,}</td></tr>
    <tr><td>清洗后行数</td><td class="highlight">{cleaning_stats.get("rows_after", "—"):,}</td></tr>
    <tr><td>总移除行数</td><td class="highlight">{cleaning_stats.get("total_removed", "—"):,}（{cleaning_stats.get("total_removed", 0) / cleaning_stats.get("rows_before", 1) * 100:.1f}%）</td></tr>
  </table>
</div>
"""

    # 月度营收趋势
    html += f"""
<div class="section">
  <h2>1. 月度营收趋势</h2>
  <img src="data:image/png;base64,{chart_b64['01_monthly_revenue']}" alt="月度营收趋势">
</div>
"""

    # Top 商品 + Top 国家（并列）
    html += f"""
<div class="section">
  <h2>2. 热销商品 & 核心市场</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
    <div>
      <h3 style="font-size:16px;color:#555;margin-bottom:10px;">Top 10 商品（按营收）</h3>
      <img src="data:image/png;base64,{chart_b64['02_top_products']}" alt="热销商品">
    </div>
    <div>
      <h3 style="font-size:16px;color:#555;margin-bottom:10px;">Top 10 国家（按营收）</h3>
      <img src="data:image/png;base64,{chart_b64['03_top_countries']}" alt="核心市场">
    </div>
  </div>
</div>
"""

    # 国家占比
    html += f"""
<div class="section">
  <h2>3. 各国营收占比</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:center;">
    <img src="data:image/png;base64,{chart_b64['04_country_pie']}" alt="各国营收占比">
    <div>
      <h3 style="font-size:16px;color:#555;margin-bottom:12px;">Top 5 国家详情</h3>
      <table>
        <tr><th>国家</th><th>营收</th><th>占比</th></tr>
"""
    country_all = sales["top_countries"]
    for _, row in country_all.head(5).iterrows():
        pct = row["Revenue"] / sales["total_revenue"] * 100
        html += f"""        <tr><td>{row['Country']}</td><td>$ {row['Revenue']:,.0f}</td><td>{pct:.1f}%</td></tr>
"""
    html += """      </table>
    </div>
  </div>
</div>
"""

    # 客户分析
    html += f"""
<div class="section">
  <h2>4. 客户价值分层（RFM 模型）</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
    <img src="data:image/png;base64,{chart_b64['05_rfm_segments']}" alt="客户分层">
    <img src="data:image/png;base64,{chart_b64['08_top_customers']}" alt="Top 客户">
  </div>
  <h3 style="font-size:16px;color:#555;margin-top:20px;">高价值客户 Top 5</h3>
  <table>
    <tr><th>客户 ID</th><th>最近购买（天前）</th><th>订单数</th><th>消费总额</th><th>分层</th></tr>
"""
    for _, row in customers["top_customers"].head(5).iterrows():
        html += (f"""    <tr><td>#{int(row['Customer ID'])}</td>"""
                 f"""<td>{int(row['Recency'])}</td>"""
                 f"""<td>{int(row['Frequency'])}</td>"""
                 f"""<td>$ {row['Monetary']:,.0f}</td>"""
                 f"""<td>{row['Segment']}</td></tr>\n""")
    html += """  </table>
</div>
"""

    # 客单价 + 散点
    html += f"""
<div class="section">
  <h2>5. 客单价 & 市场分析</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
    <img src="data:image/png;base64,{chart_b64['06_aov_trend']}" alt="客单价趋势">
    <img src="data:image/png;base64,{chart_b64['07_orders_vs_revenue']}" alt="订单vs营收">
  </div>
</div>
"""

    # 详细数据表
    monthly = sales["monthly_revenue"]
    html += """
<div class="section">
  <h2>6. 月度营收明细</h2>
  <table>
    <tr><th>月份</th><th>营收（$）</th></tr>
"""
    for _, row in monthly.iterrows():
        html += f"""    <tr><td>{row['Month'].strftime('%Y-%m')}</td><td>$ {row['Revenue']:,.0f}</td></tr>
"""
    html += """  </table>
</div>
"""

    # 页脚
    html += f"""
<div class="footer">
  <p>Cross-border E-commerce Sales Dashboard &copy; {datetime.now().year} &bull; 由 Python + Pandas + Matplotlib 生成</p>
</div>

</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    file_size = os.path.getsize(output_path) / 1024
    print(f"  HTML 报告已生成 → {output_path}  ({file_size:.1f} KB)")

    return output_path
