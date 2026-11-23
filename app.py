from secrets import token_hex
from urllib.parse import urlsplit

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
links = {}


@app.get("/")
def index():
    return render_template("index.html")


@app.route("/links/new", methods=["GET", "POST"])
def create_link():
    if request.method == "GET":
        return render_template("new_link.html")

    original_url = request.form.get("original_url", "").strip()
    title = request.form.get("title", "").strip()
    try:
        address = urlsplit(original_url)
        valid_url = (
            address.scheme in ("http", "https")
            and address.hostname
            and not any(char.isspace() or char == "\\" for char in original_url)
            and address.port != 0
        )
    except ValueError:
        valid_url = False

    if not valid_url:
        return render_template(
            "new_link.html", original_url=original_url, title=title,
            error="Введите полный адрес, который начинается с http:// или https://."
        ), 400

    code = token_hex(3)
    while code in links:
        code = token_hex(3)

    links[code] = {"title": title or address.hostname, "original_url": original_url}
    return redirect(url_for("list_links"), code=303)


@app.get("/links")
def list_links():
    return render_template("links.html", links=list(reversed(links.items())))


@app.get("/s/<code>")
def follow_link(code):
    link = links.get(code)
    if link is None:
        return render_template("link_not_found.html", code=code), 404

    return redirect(link["original_url"])