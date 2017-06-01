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


@app.route('/list')
@app.route('/')
def list_questions():
    pass
    question_list = app_logic.list_questions_logic(request)
    return render_template('list_questions.html', question_list=question_list)


@app.route('/create_new_question', methods=['POST'])
def create_new_question():
    pass
    request = request.form
    app_logic.create_new_question_logic(request)
    return redirect('/')


@app.route('/question/new')
def new_question():
    pass
    users = app_logic.new_question_logic()
    return render_template('new_question.html', users=users)


@app.route('/question/<id>')
def display_question(id, count_view=True):
    pass
    result = app_logic.display_question_logic()
    return render_template('display_question.html', id=result['id'], title=result['title'],
                           message=result['message'], list_answers=result['answer_list'],
                           list_comments=result['comment_list'], list_answer_comments=result['answer_comment_list'],
                           tag_list=result['tag_list'])


@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    pass
    users = app_logic.new_answer()
    return render_template('new_answer.html', question_id=question_id, users=users)


@app.route('/create_new_answer', methods=['POST'])
def add_new_answer():
    pass
    request = request.form
    app_logic.add_new_answer_logic(request)
    return redirect('/question/' + request.form["question_id"])


@app.route('/vote_question_up')
def vote_question_up():
    pass
    id = request.args.get('id')
    app_logic.vote_question_up(id)
    return redirect('/')


@app.route('/vote_question_down')
def vote_question_down():
    pass
    id = request.args.get('id')
    app_logic.vote_question_down(id)
    return redirect('/')


@app.route('/vote_answer_up')
def vote_answer_up():
    pass
    id = request.args.get('id')
    question_id = app_logic.vote_answer_up_logic(id)
    return display_question(question_id, count_view=False)


@app.route('/vote_answer_down')
def vote_answer_down():
    pass
    id = request.args.get('id')
    question_id = app_logic.vote_answer_down_logic(id)
    return display_question(question_id, count_view=False)


@app.route('/delete/<question_id>', methods=['POST'])
def delete_question(question_id):
    pass
    app_logic.delete_question_logic(question_id)
    return redirect('/')


@app.route('/question/<question_id>/new-tag', methods=['POST'])
def add_tag(question_id):
    pass
    existing_tags = app_logic.add_tag_logic()
    return render_template("add_tag.html", question_id=question_id, existing_tags=existing_tags)


@app.route('/question/<question_id>/add_new_tag', methods=['POST'])
def add_new_tag(question_id):
    pass
    request = request.form
    app_logic.add_new_tag_logic(request)
    return redirect('/question/' + question_id)


@app.route('/search', methods=['GET'])
def search():
    pass
    search = request.args.get('q').replace(' ', '%')
    search_results = app_logic.search(search)
    return render_template('search_results.html', search_results=search_results)


@app.route('/delete_tag/<question_id>')
def delete_tag(question_id):
    pass
    tag_name = request.args.get('tag_name')
    app_logic.delete_tag_logic(tag_name)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-comment')
def new_question_comment(question_id):
    pass
    users = app_logic.new_question_comment_logic()
    return render_template('new_comment.html', question_id=question_id, comment_type="question", users=users)


@app.route('/create_new_comment', methods=['POST'])
def add_new_question_comment():
    pass
    request = request.form
    app_logic.add_new_question_comment_logic(request)
    return redirect('/question/' + request.form["question_id"])


@app.route('/answer/<answer_id>/new-comment')
def new_answer_comment(answer_id):
    pass
    users = app_logic.new_answer_comment_logic()
    return render_template('new_comment.html', answer_id=answer_id, comment_type="answer", users=users)


@app.route('/create_new_answer_comment', methods=['POST'])
def add_new_answer_comment():
    pass
    request = request.form
    question_id = app_logic.add_new_answer_comment_logic(request)
    return redirect('/question/' + str(question_id))


@app.errorhandler(404)
def page_not_found(e):
    pass
    return render_template('404.html'), 404


@app.route('/registration')
def new_registration():
    pass
    return render_template('registration.html')


@app.route('/registration/new', methods=['POST'])
def add_new_registration():
    pass
    user_name = request.form['new_registration']
    app_logic.add_new_registration_logic(user_name)
    return redirect('/')


@app.route('/tags')
def tags():
    pass
    tag_list = app_logic.tags_logic()
    return render_template('tag_page.html', tag_list=tag_list)


@app.route('/user/<user_id>')
def user_page(user_id):
    pass
    result = app_logic.user_page(user_id)
    return render_template('user_page.html', user_name=result['user_name'], question_list=result['question_list'],
                           answer_list=result['answer_list'], comment_list=result['comment_list'])


@app.route('/list_users')
def list_users():
    pass
    user_list = app_logic.list_users_logic()
    return render_template('list_users.html', user_list=user_list)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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