from . import content_api_blueprint
from .. import db
from ..models import Content,Serial,Serial_episode
from  flask import jsonify,request,abort
import re

@content_api_blueprint.route('/api/content',methods=['GET'])
def content():
    content = []
    for row in Content.query.all():
        print(row)
        #content.append(row.to_json())
    response = jsonify({'result': 'content'})
    return response

@content_api_blueprint.route('/api/content/add', methods =['POST'])
def add_content():

    request_data = request.get_json()
    title = (request_data['title']).strip()
    type_cotent = (request_data['type']).strip()
    standard_title = normalize(title)
    season = None
    episode = None

    if request_data:
        if 'season' in request_data:
            season = int(request_data['season'])
        if 'episode' in request_data:
            episode = int(request_data['episode'])


    if type_cotent == "UNICO":
        exists = db.session.query(Content.id).filter_by(standard_title=standard_title).first() is not None
        if(exists == False):
            content = Content()
            content.title = title
            content.standard_title = standard_title
            db.session.add(content)
            db.session.commit()
            return "Se agrego correctamente"
        else:
            return "Ya se encuentra registrado"

    if type_cotent == "SERIE":
        if season == None or episode == None:
            return 'El programa es tipo Serie, Suministra la season y el episode'

        title2 = title+'-'+str(season)+'-'+str(episode)
        standard_title2 = normalize(title2)
        exists = db.session.query(Content.id).filter_by(standard_title=standard_title2).first() is not None

        if(exists == False):
            content = Content()
            content.title = title2
            content.standard_title = standard_title2
            db.session.add(content)
            db.session.commit()
        else:
            return "Ya esta registrado"

        exists2 = db.session.query(Serial.id).filter_by(standard_title=standard_title).first() is not None

        if(exists2 == False):
            serial = Serial()
            serial.title=title
            serial.standard_title=standard_title
            db.session.add(serial)
            db.session.commit()

        content_id = db.session.query(Content).filter(Content.standard_title == standard_title2).first().id
        serial_id = db.session.query(Serial).filter(Serial.standard_title == standard_title).first().id
        exists3 = db.session.query(Serial_episode.id).filter_by(content_id=content_id,serial_id=serial_id ).first() is not None

        if(exists3 == False):
            serial_episode = Serial_episode()
            serial_episode.content_id=content_id
            serial_episode.serial_id = serial_id
            serial_episode.season = season
            serial_episode.episode = episode
            db.session.add(serial_episode)
            db.session.commit()
            return "Se creo serial_episode"

    return "Error verifica el tipo de programa"


@content_api_blueprint.route('/api/content/id/<id>',methods=['GET'])
def id_content(id):

    content_id = db.session.query(Content).filter(Content.id == id).first()
    dic_response  = {
        "title": content_id.title,
        "standard_title": content_id.standard_title
    }

    return dic_response


@content_api_blueprint.route('/api/content/title/<title>',methods=['GET'])
def title_content(title):

    standard_title = normalize(title)
    print(standard_title)
    content_title = db.session.query(Content).filter(Content.standard_title == standard_title).first()
    print(content_title)
    dic_response  = {
        "title": content_title.title,
        "synopsis": content_title.synopsis,
        "standard_title": content_title.standard_title
    }

    return dic_response



def normalize(s):

    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "n")
    )

    for a, b in replacements:

        s = s.replace(a, b).replace(a.upper(), b.upper())

    s = " ".join(re.split(r"\s+", s))
    s = s.strip().lower().capitalize()

    return s


