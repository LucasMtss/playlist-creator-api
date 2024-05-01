from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
CORS(app)

# Configuração da autenticação do Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="db70ddf807564ace98b1d9436440984a", client_secret="21151b18a6e148f288ec15f26c450fc3", scope="playlist-modify-private", redirect_uri="http://localhost:5173"))

def search_artist(artist_name):
    result = sp.search(q=artist_name, type='artist', limit=20)
    artists = result['artists']['items']
    return artists

def top_tracks(artist_id):
    tracks = sp.artist_top_tracks(artist_id, country='BR')
    return tracks['tracks']

def create_playlist(playlist_name, track_uris):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
    playlist_id = playlist['id']
    sp.playlist_add_items(playlist_id, track_uris)

@app.route('/buscar-artistas', methods=['GET'])
def buscar_artistas():
    artist_name = request.args.get('nome')
    print('name', artist_name)
    if artist_name:
        artists = search_artist(artist_name)
        print(jsonify(artists))
        return jsonify(artists)
    else:
        return jsonify({'error': 'É necessário fornecer um parâmetro "q" com o nome do artista'})

@app.route('/buscar-musicas-mais-tocadas', methods=['GET'])
def buscar_musicas_mais_tocadas():
    artist_id = request.args.get('artist_id')
    if artist_id:
        tracks = top_tracks(artist_id)
        return jsonify(tracks)
    else:
        return jsonify({'error': 'É necessário fornecer um parâmetro "artist_id" com o ID do artista'})

@app.route('/criar-playlist', methods=['POST'])
def criar_playlist():
    data = request.json
    if 'playlist_name' in data and 'track_uris' in data:
        playlist_name = data['playlist_name']
        track_uris = data['track_uris']
        create_playlist(playlist_name, track_uris)
        return jsonify({'message': 'Playlist criada com sucesso!'})
    else:
        return jsonify({'error': 'É necessário fornecer os parâmetros "playlist_name" e "track_uris"'})

if __name__ == '__main__':
    app.run(debug=True)
