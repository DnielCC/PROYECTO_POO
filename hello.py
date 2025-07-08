from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms import SignupForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/Registro', methods=["GET", "POST"])
def show_signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Aquí iría la lógica de registro de usuario en la base de datos
        flash('¡Registro exitoso! (Simulado, sin base de datos)', 'success')
        return redirect(url_for('info'))
    return render_template("Registro.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login():
    form = RegisterForm()
    if form.validate_on_submit():
        # Aquí iría la lógica de autenticación
        flash('¡Inicio de sesión exitoso! (Simulado, sin base de datos)', 'success')
        return redirect(url_for('inicio'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('inicio'))

@app.route('/Registro/informacion', methods=['GET', 'POST'])
def info():
    # Aquí iría la lógica para actualizar información del usuario
    flash('Información actualizada exitosamente. (Simulado, sin base de datos)', 'success')
    return render_template('Info_users.html')

@app.route('/inicio/usuarios')
def inicio_usuarios():
    return render_template('inicio_usuarios.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('dashboard_admin.html')

if __name__ == "__main__":
    app.run(debug=True)

