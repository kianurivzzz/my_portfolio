from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename

from bot_notifyer.bot import call_tg
from db import Database
from check_file import check_file
from config import SECRET_KEY

app = Flask(__name__, template_folder='lesson_templates')
app.config['SECRET_KEY'] = SECRET_KEY
app.debug = True

db = Database('db.sqlite3')


@app.route('/')
def index():
    return render_template('pages/index.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/projects')
def projects():
    all_projects = db.select_project()
    return render_template('pages/my-projects.html', projects=all_projects)


@app.route('/admin/add-projects', methods=['GET', 'POST'])
def adm_add_project():
    if request.method == 'POST':
        for key in request.form:
            if request.form[key] == '':
                flash(['Not all fields have been filled in!', 'red'])

        if 'file' not in request.files:
            flash(['Unable to read the file', 'red'])

        file = request.files['file']

        if file.filename == '':
            flash(['File not selected', 'red'])

        if file and check_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f'static/img/{filename}')

        db.insert_project(request.form['title'], request.form['description'], filename)
    return render_template('admin/add_project.html')


@app.route('/admin/del-projects', methods=['GET', 'POST'])
def adm_del_project():
    if request.method == 'POST':
        if request.form and 'id' in request.form:
            db.delete_project(request.form['id'])
            flash(['Project delete successfully', 'green'])
    return render_template('admin/del_project.html', projects=db.select_project())


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        for key in request.form:
            if request.form[key] == '':
                flash(['Not all fields are filled in!', 'red'])
        flash(['Review added successfully!', 'green'])
        db.insert_reviews(request.form['author'], request.form['text'], request.form['email'])

    return render_template('pages/reviews.html', reviews=db.select_reviews())


@app.route('/admin/del-reviews', methods=['GET', 'POST'])
def adm_del_reviews():
    if request.method == 'POST':
        if request.form and 'id' in request.form:
            db.delete_reviews(request.form['id'])
            flash(['Reviews delete successfully', 'green'])
    return render_template('admin/del_review.html', reviews=db.select_reviews())


@app.route('/contacts', methods=['GET', 'POST'])
def conctacts():
    if request.method == 'POST':
        for key in request.form:
            if request.form[key] == '':
                flash(['Not all fields are filled in!', 'red'])
                return render_template('pages/contacts.html')
        flash(['Your request has been successfully sent!', 'green'])

        name = request.form['name']
        question = request.form['question']
        email = request.form['email']
        phone_num = request.form['phone']

        text = f'Пришло уведемление❗️❗️❗️\nОт {name}\nТелефон: {phone_num}\nПочта: {email}\n\n{question}'
        call_tg(text)
    return render_template('pages/contacts.html')


if __name__ == '__main__':
    app.run()
