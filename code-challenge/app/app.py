from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

# import os

# cwd = os.getcwd()
# db_dir = f'sqlite:////{cwd}/db/app.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bonganimasemola/Development/coding/PHASE4/python-code-challenge-superheroes/code-challenge/app/db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
        return jsonify(heroes_data)

api.add_resource(Heroes, '/heroes')



class PowerDetail(Resource):
    def get(self, power_id):
        power = Power.query.get(power_id)
        if power:
            return jsonify({"id": power.id, "name": power.name, "description": power.description})
        else:
            return jsonify({"error": "Power not found"}), 404

    def patch(self, power_id):
        power = Power.query.get(power_id)
        if power:
            data = request.get_json()
            new_description = data.get('description')
            if new_description:
                power.description = new_description
                db.session.commit()
                return jsonify({"id": power.id, "name": power.name, "description": power.description})
            else:
                return jsonify({"error": "Description not provided"}), 400
        else:
            return jsonify({"error": "Power not found"}), 404

api.add_resource(PowerDetail, '/powers/<int:power_id>')

class HeroPowers(Resource):
    def post(self):
        data = request.get_json()
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')
        strength = data.get('strength')

        if hero_id is None or power_id is None or strength is None:
            return jsonify({"error": "Missing data"}), 400

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if hero is None or power is None:
            return jsonify({"error": "Hero or Power not found"}), 404

        hero_power = HeroPower(hero=hero, power=power, strength=strength)
        db.session.add(hero_power)
        db.session.commit()

        return jsonify({"id": hero_power.id, "hero_id": hero.id, "power_id": power.id, "strength": strength})

api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5556)
