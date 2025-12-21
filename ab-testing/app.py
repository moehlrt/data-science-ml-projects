import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from scipy import stats

from consts import FAST_FOOD_MARKETING_DATASET

st.set_page_config(page_title="A/B Dashboard", layout="wide")
st.title("Fast Food Marketing Campaign")

st.sidebar.header("Dataset")
st.sidebar.markdown(
    "[Fast Food Marketing Campaign (Kaggle)](https://www.kaggle.com/datasets/chebotinaa/fast-food-marketing-campaign-ab-test)"
)

data_path = "Datasets/WA_Marketing-Campaign.csv"
src_const = FAST_FOOD_MARKETING_DATASET

@st.cache_data
def load_df(path: str) -> tuple[pd.DataFrame, bool]:
    df = pd.read_csv(path)
    for c in ["Promotion", "week", "SalesInThousands"]:
        if c not in df.columns:
            raise ValueError(f"Missing column: {c}")
    week_raw = df["week"]
    is_datetime = False
    if np.issubdtype(week_raw.dtype, np.number):
        # Numeric week indices
        df["_week_key"] = week_raw.astype(int)
    else:
        parsed = pd.to_datetime(week_raw, errors="coerce")
        if parsed.notna().mean() >= 0.8:
            df["_week_key"] = parsed
            is_datetime = True
        else:
            # Treat as categorical labels
            df["_week_key"] = week_raw.astype(str)
    df = df.dropna(subset=["SalesInThousands"])
    return df, is_datetime


try:
    df, is_dt = load_df(data_path)
except Exception as e:
    st.error(str(e))
    st.stop()

# Weekly means per promotion
weekly = (
    df.groupby(["Promotion", "_week_key"], as_index=False)["SalesInThousands"]
    .mean()
    .rename(columns={"SalesInThousands": "target", "_week_key": "week_key"})
)


# Overall mean per promotion with 95% CI based on per-week means
def ci_by_group(w: pd.DataFrame) -> pd.DataFrame:
    out = []
    for g, gdf in w.groupby("Promotion"):
        x = gdf["target"].dropna()
        m = x.mean()
        n = len(x)
        if n > 1 and x.std(ddof=1) > 0:
            se = x.std(ddof=1) / np.sqrt(n)
            lo, hi = stats.t.interval(0.95, df=n - 1, loc=m, scale=se)
        else:
            lo, hi = m, m
        out.append({"Promotion": g, "mean": m, "ci_low": lo, "ci_high": hi})
    return pd.DataFrame(out)


overall = ci_by_group(weekly)

# Consistent colors; same as in notebook
color_map = {"1": "#66c2a5", "2": "#fc8d62", "3": "#8da0cb"}

col1, col2 = st.columns(2)
with col1:
    st.subheader("Avg Weekly Sales per Promotion by week")
    df_line = weekly.sort_values("week_key").copy()
    df_line["Promotion_str"] = df_line["Promotion"].astype(str)
    if is_dt:
        x_col = "week_key"
        x_label = "Week"
        fig1 = px.line(
            df_line,
            x=x_col,
            y="target",
            color="Promotion_str",
            markers=True,
            labels={
                x_col: x_label,
                "target": "Average Weekly Sales",
                "Promotion_str": "Promotion",
            },
            color_discrete_map=color_map,
        )
    else:
        df_line["week_label"] = df_line["week_key"].astype(str)
        order = sorted(df_line["week_key"].unique())
        order_labels = [str(x) for x in order]
        fig1 = px.line(
            df_line,
            x="week_label",
            y="target",
            color="Promotion_str",
            markers=True,
            category_orders={"week_label": order_labels},
            labels={
                "week_label": "Week",
                "target": "Average Weekly Sales",
                "Promotion_str": "Promotion",
            },
            color_discrete_map=color_map,
        )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Average weekly Sales per Promotion with 95% CI")
    err_low = overall["mean"] - overall["ci_low"]
    err_high = overall["ci_high"] - overall["mean"]
    overall["Promotion_str"] = overall["Promotion"].astype(str)
    # X-axis must be exactly 1, 2, 3 in that order
    order_promos = ["1", "2", "3"]
    fig2 = px.bar(
        overall,
        x="Promotion_str",
        y="mean",
        color="Promotion_str",
        category_orders={"Promotion_str": order_promos},
        labels={"mean": "Average Weekly Sales", "Promotion_str": "Promotion"},
        text="mean",
        color_discrete_map=color_map,
    )
    fig2.update_traces(
        error_y=dict(type="data", array=err_high, arrayminus=err_low, visible=True),
        texttemplate="%{text:.2f}",
        textposition="outside",
    )
    st.plotly_chart(fig2, use_container_width=True)
