from flask import Flask, request, render_template_string

app = Flask(__name__)



def reflected():
    query = request.args.get("query", "")
    return f"<h1>Search Results for: {query}</h1>"


comments = []  


def stored():
    if request.method == "POST":
        comment = request.form.get("comment", "")
        comments.append(comment)
    
    comment_list = "<br>".join(comments) 
    return f"<form method='POST'><textarea name='comment'></textarea><button type='submit'>Submit</button></form><h2>Comments:</h2>{comment_list}"



def dom():
    return '''
    <h1>DOM-Based XSS Demo</h1>
    <script>
        var param = new URLSearchParams(window.location.search).get('input');
        document.write("<div>" + param + "</div>");
    </script>
    '''



def template():
    user_input = request.args.get("input", "")
    template_code = f"<h1>Welcome {user_input}</h1>"
    return template_code

if __name__ == "__main__":
    app.run(debug=True)