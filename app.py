
NOTE ON THE AI FEATURE:
    You need a free Gemini API key from https://aistudio.google.com/apikey
    Paste it into the sidebar when the app runs (or set GEMINI_API_KEY as
    an environment variable). If no key is entered, the rest of the
    dashboard still works fine — only the "Ask AI" tab needs it.
"""

import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(page_title="PharmaSense", page_icon="💊", layout="wide")
st.title("💊 PharmaSense — Pharma Sales Analytics")
st.caption("A mini analytics + AI assistant for pharma sales operations data")

# ----------------------------------------------------------------------
# DATABASE HELPERS
# ----------------------------------------------------------------------
DB_PATH = "pharmasense.db"

@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    """Run a SQL query against the SQLite database and return a DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Base joined view we reuse a lot
BASE_QUERY = """
SELECT
    s.sale_id, s.sale_date, s.units_sold, s.revenue,
    r.rep_name, t.territory_name,
    h.hcp_name, h.specialty,
    p.product_name, p.category
FROM sales s
JOIN reps r ON s.rep_id = r.rep_id
JOIN territories t ON r.territory_id = t.territory_id
JOIN hcps h ON s.hcp_id = h.hcp_id
JOIN products p ON s.product_id = p.product_id
"""

df = run_query(BASE_QUERY)

# ----------------------------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------------------------
st.sidebar.header("Filters")
territory_filter = st.sidebar.multiselect(
    "Territory", options=sorted(df["territory_name"].unique()), default=None
)
product_filter = st.sidebar.multiselect(
    "Product", options=sorted(df["product_name"].unique()), default=None
)

filtered_df = df.copy()
if territory_filter:
    filtered_df = filtered_df[filtered_df["territory_name"].isin(territory_filter)]
if product_filter:
    filtered_df = filtered_df[filtered_df["product_name"].isin(product_filter)]

st.sidebar.markdown("---")
st.sidebar.header("🤖 AI Assistant Settings")
api_key = st.sidebar.text_input("Gemini API Key", type="password",
                                 help="Get a free key at https://aistudio.google.com/apikey")

# ----------------------------------------------------------------------
# TABS
# ----------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🗂️ Raw Data", "🤖 Ask AI"])

# ---------------- TAB 1: DASHBOARD ----------------
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{filtered_df['revenue'].sum():,.0f}")
    col2.metric("Total Units Sold", f"{filtered_df['units_sold'].sum():,}")
    col3.metric("Total Transactions", f"{len(filtered_df):,}")

    st.markdown("### Revenue by Territory")
    territory_rev = filtered_df.groupby("territory_name")["revenue"].sum().reset_index()
    fig1 = px.bar(territory_rev, x="territory_name", y="revenue",
                   labels={"territory_name": "Territory", "revenue": "Revenue (₹)"})
    st.plotly_chart(fig1, use_container_width=True)

    col4, col5 = st.columns(2)
    with col4:
        st.markdown("### Revenue by Product")
        product_rev = filtered_df.groupby("product_name")["revenue"].sum().reset_index()
        fig2 = px.pie(product_rev, names="product_name", values="revenue")
        st.plotly_chart(fig2, use_container_width=True)

    with col5:
        st.markdown("### Top 5 Sales Reps by Revenue")
        rep_rev = (filtered_df.groupby("rep_name")["revenue"]
                   .sum().sort_values(ascending=False).head(5).reset_index())
        fig3 = px.bar(rep_rev, x="rep_name", y="revenue",
                       labels={"rep_name": "Rep", "revenue": "Revenue (₹)"})
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### Sales Trend Over Time")
    trend = filtered_df.copy()
    trend["sale_date"] = pd.to_datetime(trend["sale_date"])
    trend = trend.groupby(trend["sale_date"].dt.to_period("W"))["revenue"].sum().reset_index()
    trend["sale_date"] = trend["sale_date"].astype(str)
    fig4 = px.line(trend, x="sale_date", y="revenue",
                    labels={"sale_date": "Week", "revenue": "Revenue (₹)"})
    st.plotly_chart(fig4, use_container_width=True)

# ---------------- TAB 2: RAW DATA ----------------
with tab2:
    st.markdown("### Filtered Sales Data")
    st.dataframe(filtered_df, use_container_width=True)
    st.download_button(
        "Download as CSV",
        filtered_df.to_csv(index=False).encode("utf-8"),
        "pharmasense_sales.csv",
        "text/csv"
    )

# ---------------- TAB 3: ASK AI ----------------
with tab3:
    st.markdown("""
    Ask a question about the sales data in plain English, e.g.:
    - *"Which territory has the highest revenue?"*
    - *"Show total units sold per product"*
    - *"Who is the top performing rep?"*
    """)
    question = st.text_input("Your question:")

    if st.button("Ask"):
        if not api_key:
            st.warning("Please enter your Gemini API key in the sidebar first.")
        elif not question:
            st.warning("Please type a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-3.5-flash")

                    schema_description = """
                    Tables:
                    sales(sale_id, rep_id, hcp_id, product_id, sale_date, units_sold, revenue)
                    reps(rep_id, rep_name, territory_id)
                    hcps(hcp_id, hcp_name, specialty, territory_id)
                    territories(territory_id, territory_name)
                    products(product_id, product_name, category)
                    """

                    prompt = f"""
                    You are a SQL expert. Given this SQLite schema:
                    {schema_description}

                    Write ONE valid SQLite SQL query (and nothing else, no
                    explanation, no markdown formatting) that answers this
                    question: "{question}"
                    """

                    response = model.generate_content(prompt)
                    sql_query = response.text.strip().strip("`").replace("sql\n", "")

                    st.markdown("**Generated SQL:**")
                    st.code(sql_query, language="sql")

                    result_df = run_query(sql_query)
                    st.markdown("**Answer:**")
                    st.dataframe(result_df, use_container_width=True)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

st.markdown("---")
st.caption("Built as a demo project — synthetic data only, not real pharma sales data.")
