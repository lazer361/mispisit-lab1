from datetime import datetime
from os import environ
from secrets import token_hex
from urllib.parse import urlsplit

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import DateTime, String, Text, create_engine, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

app = Flask(__name__)
engine = create_engine(environ["DATABASE_URL"])


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    original_url: Mapped[str] = mapped_column(Text)
    short_code: Mapped[str] = mapped_column(String(6), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


Base.metadata.create_all(engine)


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
            and len(address.hostname) <= 255
            and not any(char.isspace() or char == "\\" for char in original_url)
            and address.port != 0
        )
    except ValueError:
        valid_url = False

    error = None
    if not valid_url:
        error = "Введите полный адрес, который начинается с http:// или https://."
    elif len(title) > 255:
        error = "Название должно содержать не больше 255 символов."
    if error:
        return render_template(
            "new_link.html", original_url=original_url, title=title, error=error
        ), 400

    with Session(engine) as session, session.begin():
        while True:
            statement = insert(Link).values(
                title=title or address.hostname,
                original_url=original_url,
                short_code=token_hex(3),
            ).on_conflict_do_nothing(index_elements=[Link.short_code]).returning(Link.id)
            if session.scalar(statement) is not None:
                break

    return redirect(url_for("list_links"), code=303)


@app.get("/links")
def list_links():
    with Session(engine) as session:
        links = session.scalars(select(Link).order_by(Link.id.desc())).all()
    return render_template("links.html", links=links)


@app.get("/s/<code>")
def follow_link(code):
    with Session(engine) as session:
        link = session.scalar(select(Link).where(Link.short_code == code))
    if link is None:
        return render_template("link_not_found.html", code=code), 404

    return redirect(link.original_url)