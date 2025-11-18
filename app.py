from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from flask import send_file
import os


app = Flask(__name__)
CORS(app)  # Add this line to fix CORS issues


# Load the CSV data
try:
    df = pd.read_csv('TOP 100 Songs of 2024 - Billboard Hot 100.csv')
    print(f"✓ Loaded {len(df)} songs from CSV")
except Exception as e:
    print(f"✗ Error loading CSV: {e}")
    df = pd.DataFrame()



@app.route('/')
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'message': 'Music Analytics API - Billboard Hot 100 2024',
        'endpoints': {
            'GET /stats/summary': 'Overall dataset statistics',
            'GET /stats/top/<n>': 'Top N songs by views (default 10)',
            'GET /stats/artist/<artist_name>': 'Stats for specific artist',
            'GET /stats/engagement': 'Engagement rate analysis',
            'GET /songs': 'List all songs with pagination',
            'GET /health': 'Health check'
        },
        'dataset_info': {
            'total_songs': len(df),
            'columns': list(df.columns)
        }
    })

@app.route('/dashboard')
def dashboard():
    try:
        return send_from_directory(os.getcwd(), 'index.html')
    except Exception as e:
        return jsonify({'error': f'Could not find index.html: {str(e)}'}), 404


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_loaded': len(df) > 0
    })

@app.route('/stats/summary')
def get_summary():
    """Get overall statistics using pandas summary methods"""
    try:
        summary = {
            'dataset_overview': {
                'total_songs': len(df),
                'date_range': {
                    'earliest': df['published'].min(),
                    'latest': df['published'].max()
                }
            },
            'views_statistics': {
                'total': int(df['views'].sum()),
                'mean': int(df['views'].mean()),
                'median': int(df['views'].median()),
                'std_dev': int(df['views'].std()),
                'min': int(df['views'].min()),
                'max': int(df['views'].max())
            },
            'likes_statistics': {
                'total': int(df['likes'].sum()),
                'mean': int(df['likes'].mean()),
                'median': int(df['likes'].median())
            },
            'comments_statistics': {
                'total': int(df['comments'].sum()),
                'mean': int(df['comments'].mean()),
                'median': int(df['comments'].median())
            },
            'top_song': df.nlargest(1, 'views')[['title', 'channel', 'views']].to_dict('records')[0],
            'unique_artists': int(df['channel'].nunique())
        }
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats/top/<int:n>')
@app.route('/stats/top')
def get_top_songs(n=10):
    """Get top N songs by views (default 10)"""
    try:
        if n > 100 or n < 1:
            return jsonify({'error': 'N must be between 1 and 100'}), 400
        
        top_songs = df.nlargest(n, 'views')[['title', 'channel', 'views', 'likes', 'comments']].to_dict('records')
        
        return jsonify({
            'count': len(top_songs),
            'songs': top_songs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats/artist/<artist_name>')
def get_artist_stats(artist_name):
    """Get statistics for a specific artist/channel"""
    try:
        # Filter for artist (case-insensitive partial match)
        artist_df = df[df['channel'].str.contains(artist_name, case=False, na=False)]
        
        if len(artist_df) == 0:
            return jsonify({'error': f'No songs found for artist: {artist_name}'}), 404
        
        stats = {
            'artist': artist_name,
            'songs_count': len(artist_df),
            'total_views': int(artist_df['views'].sum()),
            'total_likes': int(artist_df['likes'].sum()),
            'total_comments': int(artist_df['comments'].sum()),
            'avg_views_per_song': int(artist_df['views'].mean()),
            'songs': artist_df[['title', 'views', 'likes', 'comments']].to_dict('records')
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats/engagement')
def get_engagement():
    """Calculate and return engagement rate statistics"""
    try:
        df_copy = df.copy()
        # Engagement rate = (likes + comments) / views * 100
        df_copy['engagement_rate'] = ((df_copy['likes'] + df_copy['comments']) / df_copy['views'] * 100).round(2)
        
        top_engaged = df_copy.nlargest(10, 'engagement_rate')[['title', 'channel', 'views', 'likes', 'comments', 'engagement_rate']].to_dict('records')
        
        return jsonify({
            'description': 'Engagement rate = (likes + comments) / views * 100',
            'average_engagement_rate': float(df_copy['engagement_rate'].mean().round(2)),
            'top_engaged_songs': top_engaged
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/songs')
def list_songs():
    """List all songs with optional pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        if per_page > 100:
            per_page = 100
        
        # Calculate pagination
        start = (page - 1) * per_page
        end = start + per_page
        
        songs = df[['title', 'channel', 'views', 'likes', 'comments']].iloc[start:end].to_dict('records')
        
        return jsonify({
            'page': page,
            'per_page': per_page,
            'total_songs': len(df),
            'total_pages': (len(df) + per_page - 1) // per_page,
            'songs': songs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎵 Music Analytics API - Billboard Hot 100")
    print("="*50)
    print(f"✓ Dataset loaded: {len(df)} songs")
    print(f"✓ Server starting on http://localhost:5000")
    print("\nTry these endpoints:")
    print("  → http://localhost:5000/stats/summary")
    print("  → http://localhost:5000/stats/top/10")
    print("  → http://localhost:5000/stats/engagement")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)