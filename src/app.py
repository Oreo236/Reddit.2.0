import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

post_id_counter = 2
comment_id_counter = 2

posts = {
        0: {
        "id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98",
        },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98",
        "comments": [
                {"id": 0,
                "upvotes": 8,
                "text": "Wow, my first Reddit gold!",
                "username": "alicia98"
                },
                {"id": 1,
                "upvotes": 4,
                "text": "Congrats to me",
                "username": "alicia98"
                },
            ]
        }

}
@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here
@app.route("/api/posts/")
def get_all_posts():
    """
    Gets and Returns All Posts
    """
    res = {"posts" : list(posts.values())}
    return json.dumps(res), 200

@app.route("/api/posts/", methods = ["POST"])
def create_posts():
    """
    Creates And Returns New Posts
    """
    global post_id_counter
    body = json.loads(request.data)
    title = body.get("title", "")
    link = body.get("link", "")
    username = body.get("username", "")
    if (title or link or username) == "":
        return json.dumps({"error": "Bad request"}), 400
    post = {
        "id" : post_id_counter,
        "upvotes" : 1,
        "title" : title,
        "link" : link,
        "username" : username,

    }
    posts[post_id_counter] = post
    post_id_counter += 1
    return json.dumps(post), 201

@app.route("/api/posts/<int:post_id>/")
def get_post(post_id):
    """
    Gets and Returns A Specific Post
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200

@app.route("/api/posts/<int:post_id>/", methods = ["DELETE"])
def delete_post(post_id):
    """
    Deletes A Specific Post
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    del posts[post_id]
    return json.dumps(post), 200

@app.route("/api/posts/<int:post_id>/comments/")
def get_comments(post_id):
    """
    Gets and Returns All Comments On Specific Post
    """
    post = posts.get(post_id, [])

    if post == []:
        return json.dumps({"error": "Post not found"}), 404
    
    comments = post.get("comments", [])
    res = {"comments" : comments}
    return json.dumps(res), 200

@app.route("/api/posts/<int:post_id>/comments/", methods = ["POST"])
def post_comments(post_id):
    """
    Creates and Returns New Comment On Specific Post
    """
    global comment_id_counter
    post = posts.get(post_id, [])
    if post == []:
        return json.dumps({"error": "Post not found"}), 404
    body = json.loads(request.data)
    text = body.get("text", [])
    username = body.get("username", [])
    if text is None:
        return json.dumps({"error": "No text"}), 400
    if username is None:
        return json.dumps({"error": "No username"}), 400
    if post.get("comments") is None:
        post["comments"] = []
    comment = {
        "id" : comment_id_counter,
        "upvotes" : 1,
        "text" : text,
        "username" : username,
    }
    post["comments"].append(comment)
    comment_id_counter += 1
    return json.dumps(comment), 201

@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods = ["POST"])
def edit_comments(post_id, comment_id):
    """
    Edits and Returns A Comment On Specific Post
    """
    global post_id_counter
    global comment_id_counter
    post = posts.get(post_id, [])
    if post == []:
        return json.dumps({"error": "Post not found"}), 404
    comments = post.get("comments", [])
    comment = ""
    for comment_jj in comments:
        if comment_jj["id"] == comment_id:
            comment = comment_jj
    
    if comment != "":
        body = json.loads(request.data)
        text = body.get("text", "")
        if text == "":
            return json.dumps({"error": "Bad request"}), 400
        comment["text"] = text
        return json.dumps(comment), 200
    else:
        return json.dumps({"error": "Comment not found"}), 404

 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
