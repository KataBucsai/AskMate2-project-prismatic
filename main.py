from flask import Flask, render_template, request, redirect
import ui
import os
from importlib.machinery import SourceFileLoader
from werkzeug.utils import secure_filename
import app_logic

UPLOAD_FOLDER = 'static/uploads/img/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app_logic.app.route('/question/<question_id>/new-comment')
def new_comment(question_id):
    return render_template('new_comment.html', question_id=question_id)


@app_logic.app.route('/create_new_comment', methods=['POST'])
def add_new_comment():
    ui.add_item_to_comment_db('comment', request.form)
    return redirect('/question/' + request.form["question_id"])


@app_logic.app.route('/add_image/<id>', methods=['GET'])
def add_image_get(id):
    return render_template('file_upload.html')


@app_logic.app.route('/add_image/<id>', methods=['POST'])
def add_image_post(id):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ui.update_record('question', "image='/images/%s'" % (filename), "id=%s" % (id))
        return app_logic.redirect('/')


@app_logic.app.route('/add_answer_image/<id>', methods=['GET'])
def add_answer_image_get(id):
    return render_template('file_upload.html')


@app_logic.app.route('/add_answer_image/<id>', methods=['POST'])
def add_answer_image_post(id):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ui.update_record('answer', "image='/images/%s'" % (filename), "id=%s" % (id))
        answer = ui.get_record_from_sql_db('answer', "id=%s" % (id))
        question_id = answer[0][3]
        return app_logic.display_question(question_id, count_view=False)


if __name__ == '__main__':
    app_logic.app.run(debug=True)