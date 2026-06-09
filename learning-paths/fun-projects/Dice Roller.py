from flask import Flask, Response, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Dice Roller 🎲</title>
        <style>
            body {
                text-align: center;
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                padding-top: 50px;
            }

            h1 {
                font-size: 2.5rem;
                margin-bottom: 20px;
            }

            .dice {
                font-size: 10rem;
                transition: transform 0.5s;
            }

            .rolling {
                transform: rotate(360deg) scale(1.2);
            }

            button {
                font-size: 1.2rem;
                padding: 10px 20px;
                background-color: #4CAF50;
                border: none;
                border-radius: 8px;
                color: white;
                cursor: pointer;
                margin-top: 20px;
            }

            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>🎲 Dice Roller</h1>
        <div id="dice" class="dice">⚀</div>
        <button onclick="rollDice()">Roll the Dice</button>

        <script>
            const faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"];

            function rollDice() {
                const dice = document.getElementById('dice');
                dice.classList.add('rolling');

                setTimeout(() => {
                    fetch('/roll')
                        .then(res => res.json())
                        .then(data => {
                            dice.textContent = faces[data.value - 1];
                            dice.classList.remove('rolling');
                        });
                }, 1000);
            }
        </script>
    </body>
    </html>
    '''
    return Response(html, mimetype='text/html')

@app.route('/roll')
def roll_dice():
    value = random.randint(1, 6)
    return jsonify({'value': value})

if __name__ == '__main__':
    app.run(debug=True)
