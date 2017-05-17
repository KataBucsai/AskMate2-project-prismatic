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
    # SELECT tag.name FROM tag JOIN question_tag ON question_tag.tag_id=tag.id WHERE question_tag.question_id=1;
    tag_list = ui.get_record_from_tag('tag', 'question_tag ON question_tag.tag_id=tag.id', "question_tag.question_id=%s" % (id))
    return render_template('display_question.html', id=id, title=title, message=message, list_answers=answer_list, tag_list=tag_list)


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


@app.route('/question/<question_id>/new-tag', methods=['POST'])
def add_tag(question_id):
    existing_tags = ui.get_existing_tags()
    return render_template("add_tag.html", question_id=question_id, existing_tags=existing_tags)


@app.route('/question/<question_id>/add_new_tag', methods=['POST'])
def add_new_tag(question_id):
    if request.form['new_tag']:
        # insert a new tag into tag if it is not in it
        if not ui.get_record_from_sql_db('tag', "name='%s'" % (request.form['new_tag'])):
            ui.add_item_to_tag('tag', request.form['new_tag'])
        # get new tag's id
        new_tag_id_list = ui.get_tag_id_by_name(request.form['new_tag'])
        # add this to question_tag if it is not added yet
        if not ui.get_record_from_sql_db('question_tag', "question_id=%s AND tag_id=%s" % (question_id, new_tag_id_list[0][0])):
            ui.add_item_to_question_tag('question_tag', question_id, new_tag_id_list[0][0])
    else:
        # get the tag id of the existing tag
        existing_tag_id_list = ui.get_tag_id_by_name(request.form['existing_tag'])
        # if question_id, existing_tag_id_list[0][0] is NOT in question_tag table
        if not ui.get_record_from_sql_db('question_tag', "question_id=%s AND tag_id=%s" % (question_id, existing_tag_id_list[0][0])):
            ui.add_item_to_question_tag('question_tag', question_id, existing_tag_id_list[0][0])
    return redirect('/question/' + question_id)
