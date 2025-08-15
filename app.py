import streamlit as st
import pickle
import numpy as np

# -------------------- Load Data -------------------- #
popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_score = pickle.load(open("similarity_score.pkl", "rb"))

# -------------------- Streamlit Config -------------------- #
st.set_page_config(page_title="Book Recommender", page_icon="📚", layout="wide")
st.title("📚 Book Recommender System")

# -------------------- Tabs -------------------- #
tab1, tab2 = st.tabs(["Popular Books", "Recommend Books"])

# -------------------- Popular Books Tab -------------------- #
with tab1:
    st.subheader("Top Popular Books")
    cols = st.columns(5)
    for i in range(min(50, len(popular_df))):
        with cols[i % 5]:
            st.image(popular_df['Image-URL-M'].values[i], use_container_width=True)
            st.markdown(f"**{popular_df['Book-Title'].values[i]}**")
            st.caption(f"by {popular_df['Book-Author'].values[i]}")
            st.write(f"⭐ {popular_df['avg_ratings'].values[i]} | 🗳 {popular_df['num_ratings'].values[i]} votes")

# -------------------- Recommendation Tab -------------------- #
with tab2:
    st.subheader("Get Book Recommendations")
    user_input = st.text_input("Enter a Book Title", key="rec_input")

    if st.button("Recommend", key="rec_button"):
        # Case-insensitive search
        lower_index = [title.lower() for title in pt.index]
        user_input_lower = user_input.lower()

        if user_input_lower in lower_index:
            index = lower_index.index(user_input_lower)
            similar_items = sorted(
                list(enumerate(similarity_score[index])),
                key=lambda x: x[1],
                reverse=True
            )[1:6]

            st.write("### Recommended Books:")
            rec_cols = st.columns(5)
            for idx, (book_idx, score) in enumerate(similar_items):
                temp_df = books[books['Book-Title'] == pt.index[book_idx]].drop_duplicates('Book-Title')
                title = temp_df["Book-Title"].values[0]
                author = temp_df["Book-Author"].values[0]
                image_url = temp_df["Image-URL-M"].values[0]

                with rec_cols[idx % 5]:
                    st.image(image_url, use_container_width=True)
                    st.markdown(f"**{title}**")
                    st.caption(f"by {author}")
        else:
            st.error("❌ Book not found in dataset. Please check the title and try again.")
