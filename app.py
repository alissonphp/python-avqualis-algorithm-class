from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/turmas/')
def turmas():
    return render_template('turmas/lista.html')

@app.route('/turmas/nova', methods=['GET','POST'])
def nova():
    if request.method == 'POST':
        pass
    else:
        return render_template('turmas/criar.html')

if __name__ == "__main__":
    app.run(debug=True)