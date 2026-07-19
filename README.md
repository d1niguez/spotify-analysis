# ♪ Has Music Gotten Sadder? — Spotify Audio Feature Analysis

**Live App:** [spotify-analysis-3cjkhueq6h2x9p8yq5o3ck.streamlit.app](https://spotify-analysis-3cjkhueq6h2x9p8yq5o3ck.streamlit.app)

## Overview
An exploratory data analysis of 400,000+ Spotify tracks released between 1960 and 2020, 
investigating long-term shifts in musical mood, energy, and popularity.

## The Question
Has music actually gotten sadder over time — and if so, what does that look like in the data?

## Key Findings
- **Valence has declined** steadily since the 1980s, meaning the average song has gotten measurably less "happy" over 40 years
- **Acousticness dropped sharply** after the 1970s as electronic production took over
- **"Dark bops" are rising** — high energy + low valence tracks grew from ~4% of all music in the 1960s to 6.6% by the 2010s, peaking that decade
- **Danceability is the strongest predictor of popularity**, while acousticness is the strongest negative predictor

## Features
- 📈 Valence trend line (1960–2020) with below-average shading
- 🎛️ Audio feature comparison by decade
- 🌑 "Dark bop" rise visualization by decade
- 📊 Feature correlation with popularity
- ☊ Interactive "What decade does your taste belong to?" mood matcher

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python | Core analysis |
| pandas | Data cleaning and transformation |
| matplotlib / seaborn | Visualizations |
| Streamlit | Web app deployment |
| GitHub | Version control |

## How to Run Locally
```bash
git clone https://github.com/d1niguez/spotify-analysis.git
cd spotify-analysis
pip install -r requirements.txt
streamlit run app.py
```

## Dataset
Spotify tracks dataset via Google Drive — 586,000 tracks with audio features 
including valence, energy, danceability, acousticness, tempo, and popularity.