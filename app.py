from pprint import pprint

from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from pymongo import MongoClient
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['MONGODB_DATABASE_URI'] = 'mongodb://192.168.0.12:27017/'
client = MongoClient('mongodb://192.168.0.12:27017/')
Bootstrap(app)

db = client.testdb


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_price = request.form.get('price', type=int)

        new_car = {'name': task_content, 'price': task_price}

        try:

            if task_content != "" and task_price != "":
                db.cars.insert_one(new_car)

            return redirect('/')
        except:
            return 'Error adding your request'

    else:

        tasks = []
        for doc in db.cars.find():
            car = {'name': doc['name']}

            cursor = db.cars.find({'price': {'$exists': True}}).limit(1)

            try:
                if cursor:
                    car.update({'price': doc['price']})
            except:
                pass

            tasks.append(car)

        return render_template('index.html', tasks=tasks)


@app.route('/delete/<name>')
def delete(name):
    delete_item = {'name': name}

    try:
        db.cars.remove(delete_item, 1)
        return redirect('/')
    except:
        return 'Problem deleting that task'


@app.route('/update/<string:name>/<int:price>', methods=['GET', 'POST'])
def update(name, price):
    update_item = {'name': name, 'price': price}

    if request.method == 'POST':
        task_content = request.form['content']
        task_price = request.form.get('price', type=int)

        try:

            db.cars.update_one(update_item, {'$set': {'name': task_content, 'price': task_price}})
            return redirect('/')
        except:
            return 'Problem updating your task'
    else:
        return render_template('update.html', task=update_item)


if __name__ == "__main__":
    app.run(debug=True)
