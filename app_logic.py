from flask import Flask, render_template, request, redirect
import ui
from datetime import datetime

app = Flask(__name__)


@app.route('/list')
@app.route('/')
def list_questions():
    if 'list' in str(request):
        limit = ''
    else:
        limit = ' LIMIT 5'
    question_list = ui.get_table_from_sql_db('question', limit)
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
    comment_list = ui.get_record_from_sql_db('comment', "question_id=%s" % (id))
    answer_comment_list = []
    for answer in answer_list:
        answer_comment_list.append(ui.get_record_from_sql_db('comment', "answer_id=%s" % (answer[0])))
    # SELECT tag.name FROM tag JOIN question_tag ON question_tag.tag_id=tag.id WHERE question_tag.question_id=1;
    tag_list = ui.get_record_from_tag('tag', 'question_tag ON question_tag.tag_id=tag.id',
                                      "question_tag.question_id=%s" % (id))
    return render_template('display_question.html', id=id, title=title,
                           message=message, list_answers=answer_list,
                           list_comments=comment_list, list_answer_comments=answer_comment_list,
                           tag_list=tag_list)


@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    users = ui.handle_query("""SELECT user_name FROM users ORDER BY user_name;""")
    return render_template('new_answer.html', question_id=question_id, users=users)


@app.route('/create_new_answer', methods=['POST'])
def add_new_answer():
    new_answer_user = request.form['new_answer_user']
    user_id = ui.handle_query("""SELECT id FROM users WHERE user_name='{}';""". format(new_answer_user))
    ui.handle_query("""INSERT INTO answer (submission_time, vote_number, question_id, message, users_id)
                    VALUES ('{}', {}, {}, '{}', {});""".format(
                    str(datetime.now())[:-7], 0, request.form['question_id'], request.form['new_answer_message'], user_id[0][0]))
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
    answer_list = ui.get_record_from_sql_db('answer', "question_id=%s" % (question_id))
    for record in answer_list:
        ui.delete_record('comment', "answer_id=%s" % (record[0]))
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
        if not ui.get_record_from_sql_db('tag', "name='%s'" % (request.form['new_tag'])):
            ui.add_item_to_tag('tag', request.form['new_tag'])
        new_tag_id_list = ui.get_tag_id_by_name(request.form['new_tag'])
        if not ui.get_record_from_sql_db('question_tag',
                                         "question_id=%s AND tag_id=%s" % (question_id, new_tag_id_list[0][0])):
            ui.add_item_to_question_tag('question_tag', question_id, new_tag_id_list[0][0])
    else:
        existing_tag_id_list = ui.get_tag_id_by_name(request.form['existing_tag'])
        if not ui.get_record_from_sql_db('question_tag',
                                         "question_id=%s AND tag_id=%s" % (question_id, existing_tag_id_list[0][0])):
            ui.add_item_to_question_tag('question_tag', question_id, existing_tag_id_list[0][0])
    return redirect('/question/' + question_id)


@app.route('/search', methods=['GET'])
def search():
    search = request.args.get('q').replace(' ', '%')
    search_results = ui.search_in_db("SELECT *, replace(title, '{}', '<mark>{}</mark>') AS highlighted_title, replace(answer.message, '{}', '<mark>{}</mark>') AS highlighted_message FROM question FULL JOIN answer ON question.id=answer.question_id WHERE title LIKE '%{}%' OR answer.message LIKE '%{}%'".format(search, search, search, search, search, search))
    return render_template('search_results.html', search_results=search_results)


@app.route('/delete_tag/<question_id>')
def delete_tag(question_id):
    tag_name = request.args.get('tag_name')
    tag_id = ui.get_record_from_sql_db('tag', "name='%s'" % (tag_name))[0][0]
    ui.delete_record('question_tag', "question_id=%s AND tag_id=%s" % (question_id, tag_id))
    tag_id_in_question_tag = ui.get_record_from_sql_db('question_tag', "tag_id=%s" % (tag_id))
    if not tag_id_in_question_tag:
        ui.delete_record('tag', "id=%s" % (tag_id))
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-comment')
def new_question_comment(question_id):
    return render_template('new_comment.html', question_id=question_id, comment_type="question")


@app.route('/create_new_comment', methods=['POST'])
def add_new_question_comment():
    ui.add_item_to_comment_db('comment', request.form)
    return redirect('/question/' + request.form["question_id"])


@app.route('/answer/<answer_id>/new-comment')
def new_answer_comment(answer_id):
    return render_template('new_comment.html', answer_id=answer_id, comment_type="answer")


@app.route('/create_new_answer_comment', methods=['POST'])
def add_new_answer_comment():
    ui.add_item_to_comment_db('comment', request.form)
    question_id = ui.get_record_from_sql_db('answer', 'id=%s' % (request.form["answer_id"]))[0][3]
    return redirect('/question/' + str(question_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/registration')
def new_registration():
    return render_template('registration.html')


@app.route('/registration/new', methods=['POST'])
def add_new_registration():
    user_name = request.form['new_registration']
    registration_date = datetime.today().strftime("%Y-%m-%d")
    print(registration_date)
    query = """INSERT INTO users (user_name, registration_date) VALUES ('%s', '%s')""" % (user_name, registration_date)
    ui.handle_query(query)
    return redirect('/')
