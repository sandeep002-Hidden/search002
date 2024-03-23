import html
from flask import Flask, jsonify, request,render_template
from filter import Filter
from search import search
from storage import DBStorage

app = Flask(__name__,template_folder="templates")

search_template = """
     <form action="/" method="post">
      <input id="input" type="text" name="query" placeholder="Enter to Search">
      <input id="btn" type="submit" value="Search">
    </form> 
    """

result_template ="""
<html>
<head>
<title>Result page</title>
<style>
</style>

</head>
<body>
<p class="site ">{rank}: {link} <span class="rel-button" onclick='relevant("{query}", "{link}");'></span></p>
<a  href="{link}">{title}</a>
<p class="snippet">{snippet}</p>
<hr>
<hr>
</body>
</html>
"""


def show_search_form():
    return render_template("index.html")


def run_search(query):
    results = search(query)
    fi = Filter(results)
    filtered = fi.filter()
    rendered = search_template
    filtered["snippet"] = filtered["snippet"].apply(lambda x: html.escape(x))
    for index, row in filtered.iterrows():
        rendered += result_template.format(**row)
    return rendered


@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()


@app.route("/relevant", methods=["POST"])
def mark_relevant():
    data = request.get_json()
    query = data["query"]
    link = data["link"]
    storage = DBStorage()
    storage.update_relevance(query, link, 10)
    return jsonify(success=True)


app.run(debug=True)