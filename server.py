from flask import Flask, request, send_from_directory, jsonify, render_template, redirect, make_response, send_file
from flask_cors import CORS, cross_origin
import re, os, datetime, time, json


app = Flask(__name__, static_url_path="")
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False
app.config["HOST"] = "0.0.0.0"
application = app
CORS(app, support_credentials=True)


films = json.load(open('./kinopoisk-top4800.json', 'r', encoding='utf-8'))
directors = json.load(open('./directors4800.json', 'r', encoding='utf-8'))
[film['data'].update({'directors': directors[str(film['data']['filmId'])]}) for film in films]

searchTypeMatch = {
    'title': lambda arr: arr['data']['nameRu'],
    'rating': lambda arr: arr['rating']['rating'],
    'year': lambda arr: arr['data']['year'],
}

def filmSearch(films, querry, searchType='title'):
    result = {}
    for film in films:
        if querry.lower().replace('ё', 'е') in film['data']['nameRu'].lower().replace('ё', 'е') or True in [querry.lower().replace('ё', 'е') in genre['genre'] for genre in film['data']['genres']]:
            result[str(searchTypeMatch[searchType](film)) + film['data']['nameRu']] = film
    foundedFilms = [result[key] for key in sorted(result, reverse=searchType == 'rating')]
    print(f'films founded: {len(foundedFilms)}')
    return foundedFilms


@app.route('/api/getfilms/')
@cross_origin(supports_credentials=True)
def getfilms():
    offset = int(request.args['offset'])
    filmcount = int(request.args['filmcount'])
    querry = request.args['q']
    searchType = request.args['s']
    return make_response(filmSearch(films, querry, searchType=searchType)[offset * filmcount:filmcount + offset * filmcount])



if __name__ == "__main__":
    app.run(host='0.0.0.0')
