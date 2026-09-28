# 🎬 Nepali Movie Recommendation System

An end-to-end Machine Learning web application designed to recommend Nepali movies based on plot summaries, tags, genres, and metadata using Natural Language Processing (NLP) and Content-Based Filtering techniques. 

The application is powered by **TF-IDF Vectorization** and **Cosine Similarity**, integrated with external movie APIs (**TMDb & OMDb**) for real-time poster rendering and metadata, backed by a **Render API service**, and deployed interactively via **Streamlit Cloud**.

---

## 📌 Features

- 🧠 **Content-Based Filtering**: Recommends top similar movies based on semantic textual features.
- 🖼️ **Live Poster & Rating Fetching**: Dynamic API integration with TMDb & OMDb to retrieve real-time movie posters and IMDb ratings.
- ⚡ **Lightweight REST Microservice**: Uses a Render-hosted backend API service to manage data requests efficiently.
- 🖥️ **Interactive Web Interface**: Streamlined UI built with Streamlit for seamless movie searching and visual recommendation cards.

---

## 🛠️ Tech Stack & Tools

- **Core Language**: Python
- **Data Manipulation & Preprocessing**: Pandas, NumPy
- **Machine Learning & NLP**: Scikit-Learn (`TfidfVectorizer`, Cosine Similarity)
- **Web Framework & UI**: Streamlit
- **External APIs**: TMDb API, OMDb API
- **Deployment & Hosting**: Streamlit Cloud, Render Service

---

## ⚙️ How It Works (ML Pipeline)

1. **Data Preprocessing & Cleaning**: Text features (movie title, genres, overview tags) are normalized and combined into a consolidated tag feature vector.
2. **Text Vectorization**: Applied **TF-IDF (Term Frequency-Inverse Document Frequency)** to extract textual importance and convert tags into high-dimensional feature vectors.
3. **Similarity Scoring**: Computed pairwise **Cosine Similarity** matrix across all movie vectors to score content proximity.
4. **Recommendation Engine**: Given a target movie query, the system ranks and retrieves the top $N$ most similar titles and fetches missing poster assets via API.

---

## 🚀 Getting Started Locally

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Clone the Repository
```bash
git clone [https://github.com/pranjaalg/Nepali_Movie_Recommendation.git](https://github.com/pranjaalg/Nepali_Movie_Recommendation.git)
cd Nepali_Movie_Recommendation
