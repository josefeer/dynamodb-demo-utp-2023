from flask import Flask, redirect, render_template, url_for, request, session
import boto3


TABLE_NAME= 'maestria'

app = Flask(__name__)
app.secret_key = 'secret'

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table(TABLE_NAME)

def _get_table_items():
    response = table.scan()
    return response.get('Items', '')


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/create')
def create():
    response = session.get('response')
    session.clear()

    return render_template('create.html', response=response)


@app.route('/create-item', methods=['POST'])
def create_item():
    name = request.form.get('nombre')
    birth_date = request.form.get('fecha')
    country = request.form.get('pais')

    items = _get_table_items()

    new_item = {
            'id': len(items) + 1,
            'fecha_nacimiento': str(birth_date),
            'nombre': str(name),
            'pais': str(country)
    }

    try:
        response = table.put_item(Item=new_item)
        session['response'] = response.get('ResponseMetadata').get('RequestId')
        return redirect(url_for('create'))
    except Exception as e:
        return f'Oops! Hubo un error tratando de insertar este item: {str(e)}'


@app.route('/read')
def read():
    items = _get_table_items()
    return render_template('read.html', items=items)


@app.route('/update')
def update():
    items = _get_table_items()
    response = session.get('response')
    session.clear()

    return render_template('update.html', items=items, response=response)


@app.route('/update-item', methods=['POST'])
def update_item():
    id = int(request.form.get('estudiante'))
    name = request.form.get('nombre')
    birth_date = request.form.get('fecha')
    country = request.form.get('pais')

    updated_item = {
            'id': id,
            'fecha_nacimiento': str(birth_date),
            'nombre': str(name),
            'pais': str(country)
    }

    try:
        response = table.put_item(Item=updated_item)
        session['response'] = response.get('ResponseMetadata').get('RequestId')
        return redirect(url_for('update'))
    except Exception as e:
        return f'Oops! Hubo un error tratando de actualizar este item: {str(e)}'


@app.route('/delete')
def delete():
    items = _get_table_items()
    return render_template('delete.html', items=items)


@app.route('/delete/<id>', methods=['POST'])
def delete_item(id):
    try:
        table.delete_item(Key={'id': int(id)})
        return redirect(url_for('delete'))
    except Exception as e:
        return f'Oops! Hubo un error tratando de borrar este item: {str(e)}'

