from flask import Flask, request, jsonify
from models import engine, Location
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import math
from helper import haversine

app = Flask(__name__)

session = sessionmaker(bind=engine)
session = session()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/post_location', methods=['POST'])
def postLocation():
    data = request.get_json()
    if data:
        key = data['pin'] if data.get('pin') else None
        place_name = data['name'] if data.get('name') else None
        admin_name1 = data['admin'] if data.get('admin') else None
        latitude = float(data['lat']) if data.get('lat') else None
        longitude = float(data['lon']) if data.get('lon') else None
        accuracy = int(data['acc']) if data.get('acc') else 0

        if not (key and place_name and admin_name1 and latitude and longitude):
            return jsonify(msg='Incomplete data')

        flag = False
        res = session.query(Location).filter_by(key=key)
        if res.count() == 0:
            res = session.query(Location).all()
            for r in res:
                if math.isclose(latitude, r.latitude, abs_tol=0.0001):
                    if math.isclose(longitude, r.longtitude, abs_tol=0.0001):
                        flag = True
                        break
            if not flag:
                try:
                    loc = Location(key=key,
                                   place_name=place_name,
                                   admin_name1=admin_name1,
                                   latitude=latitude,
                                   longitude=longitude,
                                   accuracy=accuracy
                                   )

                    session.add(loc)
                    session.commit()
                    k = key
                    msg = 'Successful'
                    return jsonify(key=k, msg=msg)
                except:
                    session.rollback()
                    return jsonify(msg='Unsuccessful')
            else:
                return jsonify(msg="Already present")
        else:
            return jsonify(msg="Already present")

    else:
        return jsonify(msg="No data.")


@app.route('/get_using_postgres')
def getPsql():
    data = request.get_json()
    if data:
        lat = float(data['latitude'])
        lon = float(data['longitude'])
        radius = float(data['radius'])

        lst = []

        loc_given = func.ll_to_earth(lat, lon)
        radius_func = func.earth_box(loc_given, radius)
        loc_check = func.ll_to_earth(Location.latitude, Location.longtitude)
        distance = func.earth_distance(loc_given, loc_check)

        res = session.query(Location, radius_func).filter(distance / 1000 <= radius).all()
        c = 0
        for r in res:
            c += 1
            lst.append(r[0].key)
        return jsonify(nearby=lst, number=c, msg='Successful')
    else:
        return jsonify(msg='Unable to compute.')


@app.route('/get_using_self')
def getSelf():
    data = request.get_json()
    if data:
        lat = float(data['latitude'])
        lon = float(data['longitude'])
        radius = float(data['radius'])

        lst = []
        res = session.query(Location).all()
        c = 0
        A = (lat, lon)
        for r in res:
            if r.latitude and r.longtitude:
                d = haversine(lat, lon, float(r.latitude), float(r.longtitude))
                if d and d <= radius:
                    c += 1
                    lst.append(r.key)
        lst.sort()
        return jsonify(nearby=lst, number=c, msg='Successful')
    else:
        return jsonify(msg='Not implemented')


if __name__ == '__main__':
    app.run(debug=True)
