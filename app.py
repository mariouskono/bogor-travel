from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# =============================================================================
# LOAD DATA
# =============================================================================
try:
    df_wisata = pd.read_csv("df_wisata_bogor_final_prepared.csv")
    similarity_matrix = np.load("similarity_matrix.npy")
    PLACE_NAMES = df_wisata['nama_tempat_wisata'].unique().tolist()
    PLACE_NAMES.sort()
    print("Data berhasil dimuat!")
except Exception as e:
    print(f"Error loading data: {e}")
    df_wisata = pd.DataFrame()
    similarity_matrix = np.array([])
    PLACE_NAMES = []

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def home():
    return render_template('index.html', title="Beranda")

@app.route('/model')
def model():
    return render_template('model.html', title="Tentang Model")

@app.route('/recommender')
def recommender():
    return render_template('recommender.html', title="Uji Coba", places=PLACE_NAMES)

@app.route('/author')
def author():
    return render_template('author.html', title="Tentang Author")

# =============================================================================
# API (LOGIKA REKOMENDASI)
# =============================================================================
@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        selected_place = data.get('place')
        top_n = int(data.get('top_n', 5))
        max_dist = float(data.get('radius', 100))

        if selected_place not in df_wisata['nama_tempat_wisata'].values:
            return jsonify({'error': 'Tempat tidak ditemukan'}), 404

        idx = df_wisata[df_wisata['nama_tempat_wisata'] == selected_place].index[0]
        user_lat = df_wisata.iloc[idx]['latitude']
        user_lon = df_wisata.iloc[idx]['longitude']
        sim_scores = similarity_matrix[idx]

        df_rec = df_wisata.copy()
        df_rec['similarity'] = sim_scores
        df_rec['distance_km'] = haversine(user_lat, user_lon, df_rec['latitude'].values, df_rec['longitude'].values)

        df_filtered = df_rec[df_rec['distance_km'] <= max_dist]
        recs = df_filtered.sort_values(by='similarity', ascending=False)
        recs = recs[recs['nama_tempat_wisata'] != selected_place].head(top_n)

        results = []
        for _, row in recs.iterrows():
            # Handle NaN values safely
            img_link = row['link_gambar'] if pd.notna(row['link_gambar']) else 'https://via.placeholder.com/300x200?text=No+Image'
            kecamatan = row['kecamatan'] if pd.notna(row['kecamatan']) else 'Bogor'
            kab_kota = row['kabupaten_kota'] if pd.notna(row['kabupaten_kota']) else 'Jawa Barat'
            jml_rating = int(row['jumlah_rating']) if pd.notna(row['jumlah_rating']) else 0

            results.append({
                'nama': row['nama_tempat_wisata'],
                'kategori': row['kategori'],
                'rating': row['rating'],
                'jumlah_rating': jml_rating,
                'kecamatan': kecamatan,
                'kabupaten_kota': kab_kota,
                'lat': row['latitude'],
                'lon': row['longitude'],
                'sim': f"{row['similarity']:.1%}",
                'dist': f"{row['distance_km']:.2f} km",
                'image': img_link,
                'gmaps': row['link']
            })

        source_location = {'nama': selected_place, 'lat': user_lat, 'lon': user_lon}
        return jsonify({'source': source_location, 'recommendations': results})

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)