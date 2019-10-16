from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/schoolar.db'
db = SQLAlchemy(app)

class Semestre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semestre = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Semestre %r>' % self.semestre

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curso = db.Column(db.String(120), unique=True, nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Curso %r>' % self.curso

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disciplina = db.Column(db.String(120), unique=True, nullable=False)

    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'),
        nullable=False)
    curso = db.relationship('Curso',
        backref=db.backref('cursos', lazy=True))

    semestre_id = db.Column(db.Integer, db.ForeignKey('semestre.id'),
        nullable=False)
    semestre = db.relationship('Semestre',
        backref=db.backref('semestres', lazy=True))

    def __repr__(self):
        return '<Disciplina %r>' % self.disciplina

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return '<Aluno %r>' % self.nome

class AlunoDisciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'),
        nullable=False)
    aluno = db.relationship('Aluno',
        backref=db.backref('alunos', lazy=True))
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'),
        nullable=False)
    disciplina = db.relationship('Disciplina',
        backref=db.backref('disciplinas', lazy=True))

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/semestres/')
def semestres():
    semestres = Semestre.query.order_by(Semestre.id).all()
    return render_template('semestres/lista.html', semestres=semestres)

@app.route('/semestres/novo', methods=['GET','POST'])
def novo_semestre():
    if request.method == 'POST':
        identificador_semestre = request.form['identificador']
        novo_semestre = Semestre(semestre=identificador_semestre)
        try:
            db.session.add(novo_semestre)
            db.session.commit()
            return redirect('/semestres/')
        except:
            return 'Houve um problema ao iniciar o novo semestre'
    else:
        return render_template('semestres/criar.html')

@app.route('/semestres/delete/<int:id>')
def deletar_semestre(id):
    semestre_a_deletar = Semestre.query.get_or_404(id)
    try:
        db.session.delete(semestre_a_deletar)
        db.session.commit()
        return redirect('/semestres/')
    except:
        return 'Houve um problema ao deletar o semestre'

@app.route('/cursos/')
def cursos():
    cursos = Curso.query.order_by(Curso.id).all()
    return render_template('cursos/lista.html', cursos=cursos)

@app.route('/cursos/novo', methods=['GET','POST'])
def novo_curso():
    if request.method == 'POST':
        curso = request.form['curso']
        codigo = request.form['codigo']
        novo_curso = Curso(curso=curso, codigo=codigo)
        try:
            db.session.add(novo_curso)
            db.session.commit()
            return redirect('/cursos/')
        except:
            return 'Houve um problema ao criar o novo curso'
    else:
        return render_template('cursos/criar.html')

@app.route('/cursos/delete/<int:id>')
def deletar_curso(id):
    curso_a_deletar = Curso.query.get_or_404(id)
    try:
        db.session.delete(curso_a_deletar)
        db.session.commit()
        return redirect('/cursos/')
    except:
        return 'Houve um problema ao deletar o curso'

@app.route('/disciplinas/')
def disciplinas():
    disciplinas = Disciplina.query.order_by(Disciplina.id).all()
    return render_template('disciplinas/lista.html', disciplinas=disciplinas)

@app.route('/disciplinas/nova', methods=['GET','POST'])
def nova_disciplina():
    if request.method == 'POST':
        disciplina = request.form['disciplina']
        curso_id = request.form['curso_id']
        semestre_id = request.form['semestre_id']
        nova_disciplina = Disciplina(disciplina=disciplina, semestre_id=semestre_id, curso_id=curso_id)
        try:
            db.session.add(nova_disciplina)
            db.session.commit()
            return redirect('/disciplinas/')
        except:
            return 'Houve um problema ao criar a nova disciplina'
    else:
        semestres = Semestre.query.order_by(Semestre.id).all()
        cursos = Curso.query.order_by(Curso.id).all()

        return render_template('disciplinas/criar.html', semestres=semestres, cursos=cursos)

@app.route('/disciplinas/delete/<int:id>')
def deletar_disciplina(id):
    disciplina_a_deletar = Disciplina.query.get_or_404(id)
    try:
        db.session.delete(disciplina_a_deletar)
        db.session.commit()
        return redirect('/disciplinas/')
    except:
        return 'Houve um problema ao deletar a disciplina'


if __name__ == "__main__":
    app.run(debug=True)