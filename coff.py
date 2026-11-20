
from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Database creation
db = sqlite3.connect("coffee.db")
db.execute("""
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY,
    name TEXT,
    votes INTEGER DEFAULT 0
)
""")

count = db.execute("SELECT COUNT(*) FROM coffee").fetchone()[0]

if count == 0:
    db.executemany(
        "INSERT INTO coffee (name, votes) VALUES (?, ?)",
        [
            ("Espresso", 0),
            ("Cappuccino", 0),
            ("Latte", 0),
            ("Cold Coffee", 0),
            ("Mocha", 0)
        ]
    )

db.commit()
db.close()


# Display coffee list
@app.route("/")
def home():

    db = sqlite3.connect("coffee.db")
    data = db.execute("SELECT * FROM coffee").fetchall()
    db.close()

    html = """
    <html>
    <head>
        <title>Coffee Rating</title>

        <style>
            body {
                background-color: #f5e6d3;
                font-family: Arial;
                text-align: center;
            }

            h1 {
                color: brown;
            }

            .item {
                background: white;
                padding: 15px;
                margin: 15px auto;
                width: 300px;
                border-radius: 10px;
            }

            button {
                background: orange;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>

        <h1>☕ Coffee Rating Application</h1>
        <h3>Vote for Your Favourite Coffee</h3>

        """

    for coffee in data:
        html += f"""
        <div class="item">

            <h2>{coffee[1]}</h2>

            <p>Total Votes: {coffee[2]}</p>

            <form action="/vote/{coffee[0]}" method="POST">
                <button type="submit">Vote</button>
            </form>

        </div>
        """

    html += """
    </body>
    </html>
    """

    return html


# Update vote
@app.route("/vote/<int:id>", methods=["POST"])
def vote(id):

    db = sqlite3.connect("coffee.db")

    db.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id = ?",
        (id,)
    )

    db.commit()
    db.close()

    return redirect("/")


# Run application
if __name__ == "__main__":
    app.run(debug=True)