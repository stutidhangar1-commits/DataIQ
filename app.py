import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DataIQ", page_icon="📊", layout="wide")

st.title("📊 DataIQ")
st.write("Smart Data Analysis Dashboard")

file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if file:
    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

    # Dashboard
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing Values", int(df.isnull().sum().sum()))

    menu = st.sidebar.selectbox("Choose Feature", [
        "Preview", "Data Cleaning", "Filtering",
        "GroupBy", "Visualization", "Correlation", "Download"
    ])

    if menu == "Preview":
        st.dataframe(df)
        st.write(df.describe(include="all"))

    elif menu == "Data Cleaning":
        st.write("Missing Values:", df.isnull().sum())
        if st.button("Remove Duplicates"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed!")

        col = st.selectbox("Select Column", df.columns)
        if st.button("Fill Missing Values"):
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode.iloc[0])
            st.success("Missing Values Filled!")

        st.dataframe(df)

    elif menu == "Filtering":
        col = st.selectbox("Select Column", df.columns)
        value = st.selectbox("Select Value", df[col].dropna().unique())
        st.dataframe(df[df[col] == value])

    elif menu == "GroupBy":
        col = st.selectbox("Group Column", df.columns)
        nums = df.select_dtypes("number").columns.tolist()
        if nums:
            val = st.selectbox("Numerical Column", nums)
            op = st.selectbox("Operation", ["sum", "mean", "count", "max", "min"])
            result = df.groupby(col)[val].agg(op).reset_index()
            st.dataframe(result)
            st.bar_chart(result.set_index(col))
        else:
            st.warning("No numerical columns found.")

    elif menu == "Visualization":
        nums = df.select_dtypes("number").columns.tolist()
        if nums:
            x = st.selectbox("X Axis", df.columns)
            y = st.selectbox("Y Axis", nums)
            chart = st.selectbox("Chart", ["Bar", "Line", "Scatter", "Histogram", "Box"])

            if chart == "Bar":
                fig = px.bar(df, x=x, y=y)
            elif chart == "Line":
                fig = px.line(df, x=x, y=y)
            elif chart == "Scatter":
                fig = px.scatter(df, x=x, y=y)
            elif chart == "Histogram":
                fig = px.histogram(df, x=y)
            else:
                fig = px.box(df, y=y)

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numerical columns found.")

    elif menu == "Correlation":
        nums = df.select_dtypes("number")
        if nums.shape[1] >= 2:
            fig = px.imshow(nums.corr(), text_auto=True,
                            title="Correlation Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least two numerical columns.")

    elif menu == "Download":
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "DataIQ_Cleaned.csv",
            "text/csv"
        )

st.caption("Created with Python | DataIQ")