from flask import Flask, render_template, request, redirect
import ui

app = Flask(__name__)


@app.route('/')
def list_questions():
    question_list = ui.get_table_from_sql_db('question')
    return render_template('list_questions.html', question_list=question_list)


@app.route('/create_new_question', methods=['POST'])
def create_new_question():
    ui.add_item_to_sql_db('question', request.form)
    return redirect('/')


@app.route('/question/new')
def new_question():
    return render_template('new_question.html')


@app.route('/question/<id>')
def display_question(id, count_view=True):
    question_list = ui.get_record_from_sql_db('question', "id=%s" % (id))
    title = question_list[0][4]
    message = question_list[0][5]
    view_number = question_list[0][2] + 1
    ui.update_record('question', "view_number=%s" % (view_number), "id=%s" % (id))
    answer_list = ui.get_record_from_sql_db('answer', "question_id=%s" % (id))
    return render_template('display_question.html', id=id, title=title, message=message, list_answers=answer_list)# view counter += 1


@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    return render_template('new_answer.html', question_id=question_id)


@app.route('/create_new_answer', methods=['POST'])
def add_new_answer():
    ui.add_item_to_answer_db('answer', request.form)
    return redirect('/question/' + request.form["question_id"])


@app.route('/vote_question_up')
def vote_question_up():
    id = request.args.get('id')
    question_list = ui.get_record_from_sql_db('question', "id=%s" % (id))
    vote_number = question_list[0][3] + 1
    ui.update_record('question', "vote_number=%s" % (vote_number), "id=%s" % (id))
    return redirect('/')


@app.route('/vote_question_down')
def vote_question_down():
    id = request.args.get('id')
    question_list = ui.get_record_from_sql_db('question', "id=%s" % (id))
    vote_number = question_list[0][3] - 1
    ui.update_record('question', "vote_number=%s" % (vote_number), "id=%s" % (id))
    return redirect('/')


@app.route('/vote_answer_up')
def vote_answer_up():
    id = request.args.get('id')
    answer_list = ui.get_record_from_sql_db('answer', "id=%s" % (id))
    vote_number = answer_list[0][2] + 1
    ui.update_record('answer', "vote_number=%s" % (vote_number), "id=%s" % (id))
    question_id = answer_list[0][3]
    return display_question(question_id, count_view=False)


@app.route('/vote_answer_down')
def vote_answer_down():
    id = request.args.get('id')
    answer_list = ui.get_record_from_sql_db('answer', "id=%s" % (id))
    vote_number = answer_list[0][2] - 1
    ui.update_record('answer', "vote_number=%s" % (vote_number), "id=%s" % (id))
    question_id = answer_list[0][3]
    return display_question(question_id, count_view=False)


@app.route('/delete/<question_id>', methods=['POST'])
def delete_question(question_id):
    ui.delete_record('answer', "question_id=%s" % (question_id))
    ui.delete_record('question_tag', "question_id=%s" % (question_id))
    ui.delete_record('comment', "question_id=%s" % (question_id))
    ui.delete_record('question', "id=%s" % (question_id))
    return redirect('/')