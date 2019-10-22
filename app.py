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
        backref=db.backref('cursos', cascade="all, delete-orphan", lazy=True))

    semestre_id = db.Column(db.Integer, db.ForeignKey('semestre.id'),
        nullable=False)
    semestre = db.relationship('Semestre',
        backref=db.backref('semestres', cascade="all, delete-orphan", lazy=True))

    def __repr__(self):
        return '<Disciplina %r>' % self.disciplina

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Aluno %r>' % self.nome

class AlunoDisciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'),
        nullable=False)
    aluno = db.relationship('Aluno',
        backref=db.backref('alunos', cascade="all, delete-orphan", lazy=True))
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'),
        nullable=False)
    disciplina = db.relationship('Disciplina',
        backref=db.backref('disciplinas', lazy=True))
    media = db.Column(db.Float(2), nullable=True)
    media_final = db.Column(db.Float(2), nullable=True)
    situacao = db.Column(db.String(40), nullable=True)

class AlunoDisciplinaNota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_disciplina_id = db.Column(db.Integer, db.ForeignKey('aluno_disciplina.id'),
        nullable=False)
    aluno_disciplina = db.relationship('AlunoDisciplina',
        backref=db.backref('aluno_disciplina_nota', lazy=True))
    tipo = db.Column(db.String(5), nullable=False)
    nota = db.Column(db.Float(2), nullable=False)

class AlunoDisciplinaPresenca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_disciplina_id = db.Column(db.Integer, db.ForeignKey('aluno_disciplina.id'),
        nullable=False)
    aluno_disciplina = db.relationship('AlunoDisciplina',
        backref=db.backref('aluno_disciplina_presenca', lazy=True))
    data = db.Column(db.Date, nullable=False)
    presenca = db.Column(db.Boolean(), nullable=False)

"""
Rota para a página principal da aplicação
"""
@app.route('/')
def index():
    return render_template('dashboard.html')

"""
Lista dos semestres cadastrados
"""
@app.route('/semestres/')
def semestres():
    semestres = Semestre.query.order_by(Semestre.id).all()
    return render_template('semestres/lista.html', semestres=semestres)

"""
Rotas para cadastrar um novo semestre
Caso o verbo da requisição seja GET a aplicação mostrar o formulário para inserir um novo item
Se o verbo for POST insiro uma nova instância de semestre no banco de dados e redireciono para a lista
"""
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

"""
Recebendo o identificador do semestre (id) que deve ser um número inteiro
Consulto no banco de dados se existe registro com esse identificador
Caso exista, o registro é selecionado e excluído, senão, retorna um erro 404 (não encontrado)
"""
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

@app.route('/alunos/')
def todos_alunos():
    alunos = Aluno.query.order_by(Aluno.nome).all()
    return render_template('alunos/lista.html', alunos=alunos)

@app.route('/boletim/<int:aluno>')
def boletim(aluno):
    infos_aluno = Aluno.query.get_or_404(aluno)
    disciplinas_do_aluno = AlunoDisciplina.query.filter(AlunoDisciplina.aluno_id == aluno)
    return render_template('alunos/boletim.html', infos=infos_aluno, disciplinas_do_aluno=disciplinas_do_aluno)

@app.route('/alunos/<int:disciplina>', methods=['GET','POST'])
def alunos(disciplina):
    infos_disciplina = Disciplina.query.get_or_404(disciplina)
    alunos_da_disciplina = AlunoDisciplina.query.filter(AlunoDisciplina.disciplina_id == disciplina)
    
    if request.method == 'GET':
        return render_template('alunos/lista_disciplina.html', alunos=alunos_da_disciplina, disciplina=infos_disciplina)
    else:
        nome = request.form['nome']
        email = request.form['email']
        novo_aluno = Aluno(nome=nome, email=email)
        vincular_aluno_disciplina = AlunoDisciplina(aluno=novo_aluno, disciplina=infos_disciplina)
        try:
            db.session.add(novo_aluno)
            db.session.add(vincular_aluno_disciplina)
            db.session.commit()
            return render_template('alunos/lista_disciplina.html', alunos=alunos_da_disciplina, disciplina=infos_disciplina)
        except:
            return 'Houve um problema ao cadastrar o novo aluno e vincular a disciplina'

@app.route('/nota/<int:aluno_disciplina>/lancar', methods=['GET','POST'])
def registrar_nota(aluno_disciplina):
    infos = AlunoDisciplina.query.get_or_404(aluno_disciplina)
    if request.method == 'GET':
        return render_template('alunos/nota/registrar.html', infos=infos)
    else:
        tipo = request.form['tipo']
        nota = request.form['nota']
        try:
            registrar = AlunoDisciplinaNota(aluno_disciplina=infos, tipo=tipo, nota=nota)
            db.session.add(registrar)
            db.session.commit()
            verificar_notas(infos.id, tipo)
            return render_template('alunos/nota/registrar.html', infos=infos)
        except:
            return 'Houve um problema ao registrar a nota do aluno na disciplina'

@app.route('/presenca/<int:disciplina>/lancar', methods=['GET','POST'])
def registrar_presenca(disciplina):
    infos = Disciplina.query.get_or_404(disciplina)
    alunos_da_disciplina = AlunoDisciplina.query.filter(AlunoDisciplina.disciplina_id == disciplina)
    if request.method == 'GET':
        return render_template('alunos/presenca/registrar.html', infos=infos, alunos=alunos_da_disciplina)
    else:
        data = request.form['data']
        try:
            for ad in alunos_da_disciplina:
                presenca = request.form['aluno['+str(ad.aluno.id)+']']
                registrar = AlunoDisciplinaPresenca(aluno_disciplina_id=ad.id, data=data, presenca=presenca)
                db.session.add(registrar)
                db.session.commit()

            return render_template('alunos/presenca/registrar.html', infos=infos, alunos=alunos_da_disciplina)

        except: 
            return 'WIP'

def verificar_notas(id, tipo):
    if (tipo == 'P3' or tipo == 'REP' or tipo == 'RECFIN'):
        p1 = get_nota(id, 'P1')
        p2 = get_nota(id, 'P2')
        p3 = get_nota(id, 'P3')
        if tipo == 'REP':
            rep = get_nota(id, 'REP')
            if (p1 < p2 and p1 < p3):
                media = format((rep+p2+p3)/3, '.2f')
            elif (p2 < p1 and p2 < p3):
                media = format((p1+rep+p3)/3, '.2f')
            else:
                media = format((p1+p2+rep)/3, '.2f')
            atualizar_media(id, media)
        elif tipo == 'RECFIN':
            recfin = get_nota(id, 'RECFIN')
            media_o = ((p1+p2+p3)/3 + recfin)/2
            media = format(media_o, '.2f')
            atualizar_media_final(id, media)
        else:
            media = format((p1+p2+p3)/3, '.2f')
            atualizar_media(id, media)

def get_nota(id, tipo):
    res = AlunoDisciplinaNota.query.filter(AlunoDisciplinaNota.aluno_disciplina_id == id, AlunoDisciplinaNota.tipo == tipo).first()
    return res.nota

def atualizar_media(id, media):
    aluno_disciplina = AlunoDisciplina.query.get_or_404(id)
    aluno_disciplina.media = media
    db.session.commit()
    atualizar_situacao(id)

def atualizar_media_final(id, media):
    aluno_disciplina = AlunoDisciplina.query.get_or_404(id)
    aluno_disciplina.media_final = media
    db.session.commit()
    atualizar_situacao(id)

def atualizar_situacao(id):
    aluno_disciplina = AlunoDisciplina.query.get_or_404(id)
    if(aluno_disciplina.media_final != None and aluno_disciplina.media_final != ''):
        if(aluno_disciplina.media_final >= 6):
            aluno_disciplina.situacao = 'APROVADO NA FINAL'
        else:
            aluno_disciplina.situacao = 'REPROVADO'
    else:
        if(aluno_disciplina.media >= 7):
            aluno_disciplina.situacao = 'APROVADO'
        else:
            aluno_disciplina.situacao = 'REPROVADO'
    
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)