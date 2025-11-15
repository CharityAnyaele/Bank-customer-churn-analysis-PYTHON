import streamlit as st
import pandas as pd
import plotly.express as px

# LOAD DATA
df = pd.read_csv('cleaned_data.csv')

# SIDEBAR FILTERS
st.sidebar.header("Filters")

# Country Filter
country_options = df["country"].unique()
country_filter = st.sidebar.multiselect(
    "Select country",
    options=country_options,
    default=country_options
)

# Gender Filter
gender_options = df["gender"].unique()
gender_filter = st.sidebar.multiselect(
    "Select gender",
    options=gender_options,
    default=gender_options
)

# Churn Filter
churn_options = df["churn"].unique()
churn_filter = st.sidebar.multiselect(
    "Churn Status (0 = Stayed, 1 = Churned)",
    options=churn_options,
    default=churn_options
)

# Credit Score Range
credit_min = int(df["credit_score"].min())
credit_max = int(df["credit_score"].max())
credit_range = st.sidebar.slider(
    "Credit Score Range",
    min_value=credit_min,
    max_value=credit_max,
    value=(credit_min, credit_max)
)

# APPLY FILTERS
filtered_df = df[
    (df["country"].isin(country_filter)) &
    (df["gender"].isin(gender_filter)) &
    (df["churn"].isin(churn_filter)) &
    (df["credit_score"].between(credit_range[0], credit_range[1]))
]

# TABS / MULTI-PAGE
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Churn Insights", "Financial Behavior", "Segmentation", "Correlations"]
)

# TAB 1 — OVERVIEW
with tab1:
    st.header("Customer Overview")

    # KPI Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Total customers_id", len(filtered_df))
    col2.metric("Avg credit_score", round(filtered_df["credit_score"].mean(), 2))
    col3.metric("Avg_balance", round(filtered_df["balance"].mean(), 2))

    # Gender Pie
    gender_pie = px.pie(
        filtered_df, names="gender",
        title="Gender Distribution", hole=0.4
    )
    st.plotly_chart(gender_pie)

    # Country Bar Chart
    country_bar = px.bar(
        filtered_df["country"].value_counts(),
        title="Customers by Country"
    )
    st.plotly_chart(country_bar)

# TAB 2 — CHURN INSIGHTS
with tab2:
    st.header("Churn Insights")

    churn_pie = px.pie(
        filtered_df, names="churn",
        title="Churn Breakdown (0 = Stayed, 1 = Churned)",
        hole=0.3
    )
    st.plotly_chart(churn_pie)
#with TAB 2 #only render within this block
    churn_by_country = df.groupby('country')['churn'].mean().reset_index()
    churn_by_country['churn'] *= 100

    churn_bar = px.bar(
    churn_by_country,
    x='country', y='churn',
    title='Churn Rate (%) by Country',
    color='churn',
    color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(churn_bar)


# TAB 3 — FINANCIAL BEHAVIOR
with tab3:
    st.header("Financial Behavior")

    balance_hist = px.histogram(
        filtered_df, x="balance", nbins=40,
        title="Balance Distribution"
    )
    st.plotly_chart(balance_hist)

    salary_balance = px.scatter(
        filtered_df, x="balance", y="estimated_salary",
        color="churn",
        title="Balance vs Estimated Salary"
    )
    st.plotly_chart(salary_balance)

# TAB 4 — CUSTOMER SEGMENTATION
with tab4:
    st.header("Segmentation (Country → Gender → Churn)")

    sunburst = px.sunburst(
        filtered_df,
        path=["country", "gender", "churn"],
        title="Customer Segmentation"
    )
    st.plotly_chart(sunburst)

# TAB 5 — CORRELATION ANALYSIS
with tab5:
    st.header("Correlation Heatmap")

    numeric_df = filtered_df.select_dtypes(include=["int64", "float64"])
    corr_matrix = numeric_df.corr()

    heatmap = px.imshow(
        corr_matrix,
        text_auto=True,
        title="Correlation Matrix"
    )
    st.plotly_chart(heatmap)