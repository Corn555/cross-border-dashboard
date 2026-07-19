"""页面：关于项目。"""
import streamlit as st


def show():
    st.header("关于本项目")
    cfg = st.session_state.cfg
    proj = cfg["project"]

    st.markdown(f"""
    ### {proj['name']}

    **版本**: {proj['version']}

    基于 **四层架构** 构建的跨境电商销售数据分析平台：

    ```
    Presentation    main.py (CLI) + app.py (Web)    ← 双入口
    Application     src/pipeline/                    ← 流程编排
    Business        sales/customer analyzer          ← 纯计算
    Data            loader + cleaner                 ← I/O
    Infrastructure  config / logger / exceptions     ← 横切能力
    ```

    **分析能力**:
    - 销售 KPI：总营收、订单数、客单价、月度趋势
    - 商品分析：Top N 排行
    - 客户分析：RFM 分层（高/中/低价值）
    - 可视化：8 张 Matplotlib 图表
    - 报告：自包含 HTML（base64 内嵌图片）
    - 交互：国家筛选、Top N 调节

    **技术栈**: Python 3.12+, Pandas, Matplotlib, Streamlit, pytest, Ruff
    """)

    st.divider()
    st.caption("配置文件: config/config.yaml")
