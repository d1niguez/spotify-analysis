import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Page config ──
st.set_page_config(page_title="Spotify Mood Analysis", page_icon="🎵", layout="wide")

@st.cache_data
def load_data():
    import gdown
    url = "https://drive.google.com/uc?id=1RHQ_jm6suE_0Zb2CDJwj1jMGLZ4xnvuN"
    output = "/tmp/tracks.csv"
    gdown.download(url, output, quiet=True)
    df = pd.read_csv(output)
    df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    df = df[(df['year'] >= 1960) & (df['year'] <= 2020)]
    df['decade'] = (df['year'] // 10 * 10).astype(int)
    return df

df = load_data()

# ── Header ──
st.title("♪ Has Music Gotten Sadder?")
st.markdown(f"Analyzing {len(df):,} Spotify tracks from 1960–2020")
st.divider()

# ── KPIs ──
col1, col2, col3 = st.columns(3)
col1.metric("Tracks Analyzed", f"{len(df):,}")
col2.metric("Avg Valence", f"{df['valence'].mean():.2f}")
col3.metric("Dark Bop Tracks", f"{len(df[(df['energy'] > 0.7) & (df['valence'] < 0.4)]):,}")

st.divider()

# ── Chart 1: Valence over time ──
st.subheader("Average Valence Over Time")
valence_by_year = df.groupby('year')['valence'].mean()
avg = valence_by_year.mean()

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(valence_by_year.index, valence_by_year.values, color='#7A8B7B', linewidth=2.5)
ax.axhline(avg, color='#E8A09A', linestyle='--', linewidth=1.2, label=f'Overall avg: {avg:.2f}')
ax.fill_between(valence_by_year.index, valence_by_year.values, avg,
                where=(valence_by_year.values < avg), alpha=0.15, color='#E8A09A')
ax.set_xlabel('Year')
ax.set_ylabel('Valence (0 = Sad, 1 = Happy)')
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

st.divider()

# ── Chart 2: Decade features ──
st.subheader("Audio Features by Decade")
decade_avg = df.groupby('decade')[['valence','energy','danceability','acousticness']].mean()

fig2, ax2 = plt.subplots(figsize=(14, 5))
decade_avg.plot(ax=ax2, marker='o', linewidth=2)
ax2.set_xlabel('Decade')
ax2.set_ylabel('Average Value (0–1)')
ax2.set_xticks(decade_avg.index)
ax2.set_xticklabels([f"{d}s" for d in decade_avg.index])
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

st.divider()

# ── Chart 3: Dark bop rise ──
st.subheader('Rise of the "Dark Bop"')
dark_bops = df[(df['energy'] > 0.7) & (df['valence'] < 0.4)]
dark_by_decade = dark_bops.groupby('decade').size()
total_by_decade = df.groupby('decade').size()
dark_pct = (dark_by_decade / total_by_decade * 100).round(1)

fig3, ax3 = plt.subplots(figsize=(12, 4))
dark_pct.plot(kind='bar', ax=ax3, color='#7A5C8A', edgecolor='none')
ax3.set_xlabel('Decade')
ax3.set_ylabel('% of All Tracks')
ax3.set_xticklabels([f"{d}s" for d in dark_pct.index], rotation=0)
ax3.grid(True, alpha=0.3, axis='y')
st.pyplot(fig3)

st.divider()

# ── Chart 4: Popularity correlations ──
st.subheader("What Makes a Song Popular?")
feature_cols = ['danceability','energy','valence','acousticness','speechiness','tempo']
correlations = df[feature_cols + ['popularity']].corr()['popularity'].drop('popularity').sort_values()

fig4, ax4 = plt.subplots(figsize=(10, 4))
colors = ['#E8A09A' if x < 0 else '#7A8B7B' for x in correlations]
correlations.plot(kind='barh', ax=ax4, color=colors, edgecolor='none')
ax4.axvline(0, color='black', linewidth=0.8)
ax4.set_xlabel('Correlation with Popularity')
ax4.grid(True, alpha=0.3, axis='x')
st.pyplot(fig4)

st.divider()

# ── Feature 4: What decade does your taste belong to? ──
st.subheader("☊ What Decade Does Your Taste Belong To?")
st.markdown("Move the sliders to match your music preferences:")

c1, c2 = st.columns(2)
with c1:
    user_valence = st.slider("Valence (Sad → Happy)", 0.0, 1.0, 0.5)
    user_energy = st.slider("Energy (Calm → Intense)", 0.0, 1.0, 0.5)
with c2:
    user_danceability = st.slider("Danceability", 0.0, 1.0, 0.5)
    user_acousticness = st.slider("Acousticness", 0.0, 1.0, 0.5)

user_profile = pd.Series({
    'valence': user_valence,
    'energy': user_energy,
    'danceability': user_danceability,
    'acousticness': user_acousticness
})

decade_profiles = df.groupby('decade')[['valence','energy','danceability','acousticness']].mean()
distances = decade_profiles.sub(user_profile).pow(2).sum(axis=1).pow(0.5)
best_decade = distances.idxmin()

descriptions = {
    1960: "You belong in the 1960s — folk, soul, and the birth of rock. Raw, acoustic, and emotionally rich.",
    1970: "You belong in the 1970s — classic rock, disco, and funk. High energy with a lot of heart.",
    1980: "You belong in the 1980s — synth-pop and arena rock. Big sounds, big feelings.",
    1990: "You belong in the 1990s — grunge, R&B, and hip-hop taking over. Moody but danceable.",
    2000: "You belong in the 2000s — pop-punk, early streaming era. Loud and proud.",
    2010: "You belong in the 2010s — the dark bop era. High energy, emotionally complex.",
    2020: "You belong in the 2020s — bedroom pop and hyperpop. Experimental and introspective."
}

st.success(f"ᯓ♪ Your taste belongs in the **{best_decade}s**")
st.info(descriptions.get(best_decade, "A unique decade all your own."))