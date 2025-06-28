from flask import Flask, render_template,redirect,url_for,request
from forms import SignupForm

app = Flask('__name__')
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'


@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/Forms', methods=["GET", "POST"])
def show_signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('inicio'))
    return render_template("Forms.html", form=form)

@app.route('/login', methods=["GET","POST"])
def user_login():
    return render_template('login.html')



@app.route('/login/informacion', methods=['GET', 'POST'])  
def info(): 
    return render_template('Vusuario.html')

@app.route('/inicio/usuarios')
def inicio_usuarios(): 
    return render_template('inicio_usuarios.html')
