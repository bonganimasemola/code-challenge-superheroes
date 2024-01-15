from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power

# import os

# cwd = os.getcwd()
# db_dir = f'sqlite:////{cwd}/db/app.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bonganimasemola/Development/coding/PHASE4/python-code-challenge-superheroes/code-challenge/app/db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_data)


@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name}
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_data)


@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404
    
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()

    if 'description' in data:
        power.description = data['description']

    db.session.commit()

    power_data = {'id': power.id, 'name': power.name, 'description': power.description}
    return jsonify(power_data)

if __name__ == '__main__':
    app.run(port=5555)
