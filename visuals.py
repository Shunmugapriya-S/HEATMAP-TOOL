import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Page configuration
st.set_page_config(page_title="📊 Bivariate Frequency Heatmap Tool", layout="centered")

# Title and description
st.title("📊 Bivariate Frequency Heatmap Tool")
st.markdown("""
Upload a CSV file, select two categorical columns, and visualize the frequency of their combinations as a heatmap.
""")

# File uploader
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

# Main logic
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Show preview
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Select columns
    st.subheader("🧮 Select Columns for Heatmap")
    col1 = st.selectbox("Select Column 1", df.columns)
    col2 = st.selectbox("Select Column 2", df.columns, index=1 if len(df.columns) > 1 else 0)

    # Options
    show_relative = st.checkbox("Show Relative Frequencies (%)", value=False)
    fig_width = st.slider("📏 Figure Width", 5, 20, 8)
    fig_height = st.slider("📐 Figure Height", 5, 20, 6)

    if st.button("📊 Generate Heatmap"):
        try:
            # Drop missing values in selected columns
            df_clean = df[[col1, col2]].dropna()

            if df_clean.empty:
                st.warning("⚠️ Selected columns contain only missing values.")
            else:
                # Frequency table
                if show_relative:
                    freq_table = pd.crosstab(df_clean[col1], df_clean[col2], normalize='index') * 100
                    fmt = ".1f"
                else:
                    freq_table = pd.crosstab(df_clean[col1], df_clean[col2])
                    fmt = "d"

                # Plot heatmap
                fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                sns.heatmap(freq_table, annot=True, fmt=fmt, cmap="YlGnBu", ax=ax)
                ax.set_xlabel(col2)
                ax.set_ylabel(col1)
                st.subheader("🔥 Bivariate Frequency Heatmap")
                st.pyplot(fig)

                # Download heatmap
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                st.download_button("📥 Download Heatmap as PNG", buf.getvalue(), "bivariate_heatmap.png", "image/png")
        except Exception as e:
            st.error(f"⚠️ Error while generating heatmap: {e}")
else:
    st.info("👆 Please upload a CSV file to begin.")
