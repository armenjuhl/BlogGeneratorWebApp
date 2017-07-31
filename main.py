from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret" 
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:justblogit@localhost:8889/build-a-blog'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://armenblog:blog@localhost:8889/armenblog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    submitted = db.Column(db.Boolean)


    def __init__(self, title, body, submitted=True):
        self.title = title
        self.body = body
        self.submitted=submitted



@app.route('/', methods=['POST', 'GET'])
def index():
    blog_id = request.args.get('id')
    submitted_blogs = Blog.query.all()
    return render_template('blog.html', submitted_blogs=submitted_blogs)


@app.route('/blog', methods=['POST', 'GET'])
def show_posts(): 
    title = ''
    body = ''
    if request.method == 'GET':
        submitted_blogs = Blog.query.all()
        return render_template('blog.html', submitted_blogs=submitted_blogs, title=title, body=body)

@app.route('/landing', methods =['GET'])
def show_blog():
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('landing.html', blog=blog)
    
@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title = ''
    body = ''
    error_title = ''
    error_body = ''
    if request.method == 'POST':    
        title = request.form['title']
        body = request.form['body']
        
        if len(title) < 1:
            error_title = 'title must be longer than 1 character'
        if len(body) < 1:
            error_body = 'body must be longer than 1 character'
        if len(title) < 1 or len(body) < 1:
            return render_template('newpost.html', error_body=error_body, error_title=error_title)


        else:
            submitted= True
            newpost = Blog(title=title, body=body, submitted=True)
            db.session.add(newpost)
            db.session.commit()
            blog=newpost.id
            return redirect('/blog?id={0}'.format(blog))
    else:
        return render_template('newpost.html', title='title', body='body')

# @app.route('/delete-entry', methods=['POST'])
# def delete_entry():

#     blog_id = int(request.form['entry-id'])
#     entry = Blog.query.filter_by(title)
#     Blog.completed = False
#     db.session.delete(entry)
#     db.session.commit()

#     return redirect('/')


if __name__ == '__main__':
    app.run()
