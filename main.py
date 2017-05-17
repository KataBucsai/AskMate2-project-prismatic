from flask import Flask, render_template, request, redirect
import data_manager
import os
from importlib.machinery import SourceFileLoader
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/img/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def list_questions():
    question_list = data_manager.get_table_from_sql_db('question')
    return render_template('list_questions.html', question_list=question_list)


@app.route('/create_new_question', methods=['POST'])
def create_new_question():
    data_manager.add_item_to_sql_db('question', request.form)
    return redirect('/')


@app.route('/question/new')
def new_question():
    return render_template('new_question.html')


@app.route('/question/<id>')
def display_question(id, count_view=True):
    question_list = data_manager.get_record_from_sql_db('question', "id=%s" % (id))
    title = question_list[0][4]
    message = question_list[0][5]
    view_number = question_list[0][2] + 1
    data_manager.update_record('question', "view_number=%s" % (view_number), "id=%s" % (id))
    answer_list = data_manager.get_record_from_sql_db('answer', "question_id=%s" % (id))
    return render_template('display_question.html', id=id, title=title, message=message, list_answers=answer_list)# view counter += 1
    

@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    return render_template('new_answer.html', question_id=question_id)


@app.route('/create_new_answer', methods=['POST'])
def add_new_answer():
    data_manager.add_item_to_answer_db('answer', request.form)
    return redirect('/question/' + request.form["question_id"])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_image/<id>', methods=['GET'])
def add_image_get(id):
    return render_template('file_upload.html')


@app.route('/add_image/<id>', methods=['POST'])
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
        data_manager.update_record('question', "image='/images/%s'" % (filename), "id=%s" % (id))
        return redirect('/')

@app.route('/add_answer_image/<id>', methods=['GET'])
def add_answer_image_get(id):
    return render_template('file_upload.html')


@app.route('/add_answer_image/<id>', methods=['POST'])
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
        data_manager.update_record('answer', "image='/images/%s'" % (filename), "id=%s" % (id))
        answer = data_manager.get_record_from_sql_db('answer', "id=%s" % (id))
        question_id = answer[0][3]
        return display_question(question_id, count_view=False)


@app.route('/vote_question_up')
def vote_question_up():
    id = request.args.get('id')
    question_list = data_manager.get_record_from_sql_db('question', "id=%s" % (id))
    vote_number = question_list[0][3] + 1
    data_manager.update_record('question', "vote_number=%s" % (vote_number), "id=%s" % (id))
    return redirect('/')


@app.route('/vote_question_down')
def vote_question_down():
    id = request.args.get('id')
    question_list = data_manager.get_record_from_sql_db('question', "id=%s" % (id))
    vote_number = question_list[0][3] - 1
    data_manager.update_record('question', "vote_number=%s" % (vote_number), "id=%s" % (id))
    return redirect('/')


@app.route('/vote_answer_up')
def vote_answer_up():
    id = request.args.get('id')
    answer_list = data_manager.get_record_from_sql_db('answer', "id=%s" % (id))
    vote_number = answer_list[0][2] + 1
    data_manager.update_record('answer', "vote_number=%s" % (vote_number), "id=%s" % (id))
    question_id = answer_list[0][3]
    return display_question(question_id, count_view=False)


@app.route('/vote_answer_down')
def vote_answer_down():
    id = request.args.get('id')
    answer_list = data_manager.get_record_from_sql_db('answer', "id=%s" % (id))
    vote_number = answer_list[0][2] - 1
    data_manager.update_record('answer', "vote_number=%s" % (vote_number), "id=%s" % (id))
    question_id = answer_list[0][3]
    return display_question(question_id, count_view=False)


@app.route('/delete/<question_id>', methods=['POST'])
def delete_question(question_id):
    file_name = current_file_path + "/data/question.csv"
    question_list = data_manager.get_table_from_file(file_name, (4, 5, 6))
    question_list_csv_format = data_manager.get_timeform_to_stamp(question_list)
    question_list_csv_format = data_manager.delete_item_from_table(question_list_csv_format, question_id)
    data_manager.write_table_to_file(file_name, question_list_csv_format, (4, 5, 6))

    file_name = current_file_path + "/data/answer.csv"
    answer_list = data_manager.get_table_from_file(file_name, (4, 5))
    question_id_list = []
    for row in answer_list:
        if row[3] == question_id:
            question_id_list.append(row[0])
    answer_list_csv_format = data_manager.get_timeform_to_stamp(answer_list)
    for question_id_to_delete in question_id_list:
        answer_list_csv_format = data_manager.delete_item_from_table(answer_list_csv_format, question_id_to_delete)
    data_manager.write_table_to_file(file_name, answer_list_csv_format, (4, 5))
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)