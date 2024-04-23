from flask import Flask, request, jsonify
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import json

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Empty search query'}), 400

    try:
        with open('quotes_index.pkl', 'rb') as f:
            tfidf_vectorizer, tfidf_matrix = pickle.load(f)
        query_vector = tfidf_vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        with open('quotes.json', 'r') as f:
            quotes = json.load(f)
        # Only sort by score, not the entire quote dictionary
        results = sorted([(score, quote) for score, quote in zip(similarities, quotes)], key=lambda x: x[0], reverse=True)
        # Now extract the quote dictionaries for the response
        results = [quote for score, quote in results]
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
