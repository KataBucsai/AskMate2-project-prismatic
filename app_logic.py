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
    new_question_user = request.form['new_question_user']
    user_id = ui.handle_query("""SELECT id FROM users WHERE user_name='{}';""". format(new_question_user))
    ui.handle_query("""INSERT INTO question (submission_time, view_number, vote_number, title, message, users_id) 
                    VALUES ('{}', {}, {}, '{}', '{}', {});""".format(
                    str(datetime.now())[:-7], 0, 0, request.form['new_question_title'], request.form['new_question_message'], user_id[0][0]))
    return redirect('/')


@app.route('/question/new')
def new_question():
    users = ui.handle_query("""SELECT user_name FROM users ORDER BY user_name;""")
    return render_template('new_question.html', users=users)


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
    query = """SELECT users_id \
            FROM question
            WHERE id = %s""" % (id)
    user_id = ui.handle_query(query)[0][0]
    query = """UPDATE users \
            SET reputation = reputation + 5 \
            WHERE id = %s""" % user_id
    ui.handle_query(query)
    return redirect('/')


@app.route('/vote_question_down')
def vote_question_down():
    id = request.args.get('id')
    question_list = ui.get_record_from_sql_db('question', "id=%s" % (id))
    vote_number = question_list[0][3] - 1
    ui.update_record('question', "vote_number=%s" % (vote_number), "id=%s" % (id))
    query = """SELECT users_id \
            FROM question
            WHERE id = %s""" % (id)
    user_id = ui.handle_query(query)[0][0]
    query = """UPDATE users \
            SET reputation = reputation -2 \
            WHERE id = %s""" % user_id
    ui.handle_query(query)
    return redirect('/')


@app.route('/vote_answer_up')
def vote_answer_up():
    id = request.args.get('id')
    answer_list = ui.get_record_from_sql_db('answer', "id=%s" % (id))
    vote_number = answer_list[0][2] + 1
    ui.update_record('answer', "vote_number=%s" % (vote_number), "id=%s" % (id))
    question_id = answer_list[0][3]
    query = """SELECT users_id \
            FROM answer
            WHERE id = %s""" % (id)
    user_id = ui.handle_query(query)[0][0]
    query = """UPDATE users \
            SET reputation = reputation + 10 \
            WHERE id = %s""" % user_id
    ui.handle_query(query)
    return display_question(question_id, count_view=False)


@app.route('/vote_answer_down')
def vote_answer_down():
    id = request.args.get('id')
    answer_list = ui.get_record_from_sql_db('answer', "id=%s" % (id))
    vote_number = answer_list[0][2] - 1
    ui.update_record('answer', "vote_number=%s" % (vote_number), "id=%s" % (id))
    question_id = answer_list[0][3]
    query = """SELECT users_id \
            FROM answer
            WHERE id = %s""" % (id)
    user_id = ui.handle_query(query)[0][0]
    query = """UPDATE users \
            SET reputation = reputation - 2 \
            WHERE id = %s""" % user_id
    ui.handle_query(query)
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
    users = ui.handle_query("""SELECT user_name FROM users ORDER BY user_name;""")
    return render_template('new_comment.html', question_id=question_id, comment_type="question", users=users)


@app.route('/create_new_comment', methods=['POST'])
def add_new_question_comment():
    new_question_comment_user = request.form['new_question_comment_user']
    user_id = ui.handle_query("""SELECT id FROM users WHERE user_name='{}';""". format(new_question_comment_user))
    ui.handle_query("""INSERT INTO comment (question_id, answer_id, message, submission_time, users_id)
                    VALUES ({}, {}, '{}', '{}', {});""".format(request.form['question_id'], 'NULL',
                    request.form['new_comment_message'], str(datetime.now())[:-7], user_id[0][0]))
    return redirect('/question/' + request.form["question_id"])


@app.route('/answer/<answer_id>/new-comment')
def new_answer_comment(answer_id):
    users = ui.handle_query("""SELECT user_name FROM users ORDER BY user_name;""")
    return render_template('new_comment.html', answer_id=answer_id, comment_type="answer", users=users)


@app.route('/create_new_answer_comment', methods=['POST'])
def add_new_answer_comment():
    new_answer_comment_user = request.form['new_answer_comment_user']
    user_id = ui.handle_query("""SELECT id FROM users WHERE user_name='{}';""". format(new_answer_comment_user))
    ui.handle_query("""INSERT INTO comment (answer_id, message, submission_time, users_id)
                    VALUES ({}, '{}', '{}', {});""".format(request.form['answer_id'],
                    request.form['new_comment_message'], str(datetime.now())[:-7], user_id[0][0]))
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
    query = """INSERT INTO users (user_name, registration_date) VALUES ('%s', '%s')""" % (user_name, registration_date)
    ui.handle_query(query)
    return redirect('/')


@app.route('/tags')
def tags():
    tag_list = ui.handle_query("""SELECT t.id, t.name, COUNT(qt.question_id)
                                  FROM tag t
                                  LEFT JOIN question_tag qt
                                  ON qt.tag_id=t.id
                                  GROUP BY t.id
                                  ORDER BY COUNT(qt.question_id) DESC;""")
    return render_template('tag_page.html', tag_list=tag_list)
    

@app.route('/user/<user_id>')
def user_page(user_id):
    user_name = ui.handle_query("""SELECT user_name FROM users WHERE id=%s""" % (user_id))
    question_list = ui.handle_query("""SELECT id, title
                                       FROM question
                                       WHERE users_id='%s';""" % (user_id))
    answer_list = ui.handle_query("""SELECT a.message, q.id
                                     FROM answer a
                                     LEFT JOIN question q ON a.question_id=q.id
                                     WHERE a.users_id=%s;""" % (user_id))
    comment_list = ui.handle_query("""SELECT c.message, q.id
                                     FROM comment c
                                     LEFT JOIN question q ON c.question_id=q.id
                                     WHERE c.users_id=%s AND c.question_id IS NOT NULL
                                     UNION
                                     SELECT c.message, q.id
                                     FROM comment c
                                     LEFT JOIN answer a ON a.id=c.answer_id
                                     LEFT JOIN question q ON a.question_id=q.id
                                     WHERE c.users_id=%s AND c.answer_id IS NOT NULL;""" % (user_id, user_id))
    return render_template('user_page.html', user_name=user_name, question_list=question_list,
                           answer_list=answer_list, comment_list=comment_list)
  
  
@app.route('/list_users')
def list_users():
    query = """SELECT * \
            FROM users \
            ORDER BY id"""
    user_list = ui.handle_query(query)
    return render_template('list_users.html', user_list=user_list)
