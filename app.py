from flask import Flask, render_template, request, jsonify
import pandas as pd

# Function to calculate similarity score between user preferences and songs
def calculate_similarity(song, preferences):
    score = 0
    for feature in preferences:
        weight = preferences[feature]
        song_value = song[feature]
        score += weight * song_value
    return score

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/calculate", methods=['POST'])
def calculate():
	# Load the dataset
	file_path = 'data/dataSetFinal.csv'
	df = pd.read_csv(file_path)

	if request.method == 'POST' :
		preferences = {}
		features = ['bpm', 'nrgy', 'dnce', 'dB', 'live', 'val', 'dur', 'acous', 'spch', 'pop']
		for feature in features:
			rating = request.form[f'{feature}']
			preferences[feature] = int(rating)

		df['similarity_score'] = df.apply(lambda x: calculate_similarity(x, preferences), axis=1)
		top_songs = df.nlargest(10, 'similarity_score')[['title', 'artist']]
		top_songs_list = top_songs.to_dict(orient='records')
	# return render_template("index.html", data=top_songs)
	return render_template("index.html", data=top_songs_list)
	# return jsonify(top_songs_list)

if __name__ == '__main__':
	app.run(debug=True)