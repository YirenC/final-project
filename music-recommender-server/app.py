from flask import Flask, request, jsonify
from recommender.recommender import Recommender
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

recommendation_engine = Recommender()


@app.route('/', methods=['GET'])
def hello():
    return 'Welcome to the Music Recommender API!'


@app.route('/', methods=['POST'])
def upload():
    audio_file = request.files['file']
    audio_file.save('./upload_audio_file')
    genre, recommend_list = recommendation_engine.classify(
        './upload_audio_file')
    # print({'genre': genre, 'recommendations': recommend_list})
    return jsonify({'genre': genre, 'recommendations': recommend_list})


if __name__ == '__main__':
    app.run(debug=True)
