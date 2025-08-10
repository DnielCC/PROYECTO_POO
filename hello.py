from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from forms import SignupForm, RegisterForm
from config import ConexionDB
import mysql.connector

conexion = ConexionDB()

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# ------------ RUTA DE INICIO --------
@app.route('/')
def inicio():
    return render_template('inicio.html')
#----------------------------------------

# ---------- RUTA DE REGISTRO Y LOGIN ----------
@app.route('/Registro', methods=["GET", "POST"])
def show_signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        contra = form.password.data
        tipo_usuario = 'aspirante'

        consulta = conexion.get_datos(f"SELECT * FROM login WHERE correo = '{email}'")

        if len(consulta) > 0:
            return render_template("Registro.html", form=form)

        if form.password.data != form.confirmpassword.data:
            return render_template("Registro.html", form=form)

        resultado = conexion.insert_datos(
            f"INSERT INTO login (correo, contra, tipo_usuario) VALUES ('{email}', '{contra}', '{tipo_usuario}')"
        )

        if resultado == 'ok':
            # Obtener el ID del usuario recién creado
            user_query = conexion.get_datos(f"SELECT id FROM login WHERE correo = '{email}'")
            if user_query:
                user_id = user_query[0][0]
                # Crear sesión automáticamente
                session['user_id'] = user_id
                session['user_type'] = tipo_usuario
                session['username'] = email  # Usar email como username temporal
                
                flash('¡Registro exitoso! Ahora completa tu información.', 'success')
                return redirect(url_for('info'))
            else:
                flash('Usuario creado pero error al obtener ID. Por favor inicia sesión.', 'error')
                return redirect(url_for('user_login'))
        else:
            flash(f'Error al registrar: {resultado}', 'error')

    return render_template("Registro.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login():
    form = RegisterForm()
    if form.validate_on_submit():
        correo = form.Email.data
        password = form.password.data

        query = f"SELECT id, tipo_usuario, username FROM login WHERE correo = '{correo}' AND contra = '{password}'"
        resultado = conexion.get_datos(query)

        if resultado:
            session['user_id'] = resultado[0][0]
            session['user_type'] = resultado[0][1]
            session['username'] = resultado[0][2]  # Almacenar el username en sesión
            flash('Inicio de sesión exitoso.', 'success')

            if session['user_type'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif session['user_type'] == 'reclutador':
                return redirect(url_for('reclutador_vacantes'))
            else:
                return redirect(url_for('inicio_usuarios'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')

    return render_template('login.html', form=form)
#------------END RUTA DE REGISTRO Y LOGIN ----------


# ---------- RUTA DE INFORMACIÓN DEL USUARIO ----------
@app.route('/Registro/informacion', methods=['GET', 'POST'])
def info():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        empleo = request.form.get('empleos_deseados')
        experiencia = request.form.get('experiencia_previa')
        grado = request.form.get('grado_estudio')
        ciudad = request.form.get('ciudad')
        cp = request.form.get('codigo_postal')

        # Obtener el ID del usuario desde la sesión
        id_usuario = session['user_id']

        try:

            # Buscar ID de empleo
            id_empleo = conexion.get_datos(
                f"SELECT id FROM empleos WHERE empleo LIKE BINARY '{empleo}' LIMIT 1")
            if not id_empleo:
                flash("Error: empleo no encontrado.", 'error')
                return redirect(url_for('info'))
            id_empleo = id_empleo[0][0]

            # Buscar ID de experiencia
            id_exp = conexion.get_datos(
                f"SELECT id FROM experiencia WHERE experiencia LIKE BINARY '{experiencia}' LIMIT 1")
            if not id_exp:
                flash("Error: experiencia no encontrada.", 'error')
                return redirect(url_for('info'))
            id_exp = id_exp[0][0]

            # Buscar ID de grado de estudios
            id_grado = conexion.get_datos(
                f"SELECT id FROM grado_estudios WHERE grado LIKE BINARY '{grado}' LIMIT 1")
            if not id_grado:
                flash("Error: grado de estudios no encontrado.", 'error')
                return redirect(url_for('info'))
            id_grado = id_grado[0][0]

            # Buscar ID de ciudad
            id_ciudad = conexion.get_datos(
                f"SELECT id FROM ciudad_referencia WHERE ciudad LIKE BINARY '{ciudad}' LIMIT 1")
            if not id_ciudad:
                flash("Error: ciudad no encontrada.", 'error')
                return redirect(url_for('info'))
            id_ciudad = id_ciudad[0][0]

            # Insertar CP si no existe
            id_cp_data = conexion.get_datos(f"SELECT id FROM cp WHERE cp = '{cp}' LIMIT 1")
            if not id_cp_data:
                conexion.insert_datos(f"INSERT INTO cp (cp) VALUES ('{cp}')")
                id_cp_data = conexion.get_datos(f"SELECT id FROM cp WHERE cp = '{cp}' ORDER BY id DESC LIMIT 1")
            id_cp = id_cp_data[0][0]

            insert_info = f"""
            INSERT INTO informacion (
                id_usuario, nombre, apellidos, id_empleos, id_experiencia, id_grado_estudios, id_ciudad, id_cp
            ) VALUES (
                {id_usuario}, '{nombre}', '{apellidos}', {id_empleo}, {id_exp}, {id_grado}, {id_ciudad}, {id_cp}
            )
            """
            resultado = conexion.insert_datos(insert_info)

            if resultado == 'ok':
                flash('Información guardada correctamente.', 'success')
                return redirect(url_for('inicio_usuarios'))
            else:
                flash(f'Error en el guardado: {resultado}', 'error')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')

    return render_template('Info_users.html')

@app.route('/inicio/usuarios')
def inicio_usuarios():
    # Obtener todas las vacantes activas de la base de datos
    query_vacantes = """
        SELECT v.id, v.titulo, e.nombre as empresa, 
               CONCAT(u.ciudad, ', ', u.estado, ', ', u.pais) as ubicacion,
               tt.nombre as tipo_contrato, v.descripcion, 
               v.salario_minimo, v.salario_maximo, mt.nombre as modalidad,
               es.estatus as estado, v.fecha_publicacion
        FROM vacantes v
        INNER JOIN empresas e ON v.id_empresa = e.id
        INNER JOIN ubicaciones u ON v.id_ubicacion = u.id
        INNER JOIN tipos_trabajo tt ON v.id_tipo_trabajo = tt.id
        INNER JOIN modalidades_trabajo mt ON v.id_modalidad_trabajo = mt.id
        LEFT JOIN estado_vacantes ev ON v.id = ev.id_vacante
        LEFT JOIN estatus es ON ev.id_estatus = es.id
        WHERE es.estatus = 'Activa' OR es.estatus IS NULL
        ORDER BY v.fecha_publicacion DESC
    """
    
    vacantes = conexion.get_datos(query_vacantes)
    
    # Formatear las vacantes para el template
    vacantes_formateadas = []
    for vacante in vacantes:
        vacantes_formateadas.append({
            'id': vacante[0],
            'titulo': vacante[1],
            'empresa': vacante[2],
            'ubicacion': vacante[3],
            'tipo_contrato': vacante[4],
            'descripcion': vacante[5],
            'salario_min': vacante[6],
            'salario_max': vacante[7],
            'modalidad': vacante[8],
            'estado': vacante[9],
            'fecha_creacion': vacante[10]
        })
    
    return render_template('inicio_usuarios.html', vacantes=vacantes_formateadas)


@app.route('/user/perfil')
def perfil_usuario():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    user_id = session['user_id']

    query = f"""
        SELECT nombre, apellidos, 
               empleos.empleo, experiencia.experiencia, 
               grado_estudios.grado, ciudad_referencia.ciudad, cp.cp
        FROM informacion
        INNER JOIN empleos ON informacion.id_empleos = empleos.id
        INNER JOIN experiencia ON informacion.id_experiencia = experiencia.id
        INNER JOIN grado_estudios ON informacion.id_grado_estudios = grado_estudios.id
        INNER JOIN ciudad_referencia ON informacion.id_ciudad = ciudad_referencia.id
        INNER JOIN cp ON informacion.id_cp = cp.id
        WHERE informacion.id_usuario = {user_id}
    """

    resultado = conexion.get_datos(query)

    if resultado:
        datos = resultado[0]
        usuario = {
            'nombre_completo': datos[0] + ' ' + datos[1],
            'empleo': datos[2],
            'experiencia': datos[3],
            'grado': datos[4],
            'ciudad': datos[5],
            'codigo_postal': datos[6]
        }
    else:
        flash("Perfil no encontrado. Completa tu información.", "info")
        usuario = None

    return render_template('user_perfil.html', usuario=usuario)


@app.route('/user/postulaciones')
def mis_postulaciones():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))
    
    user_id = session['user_id']
    
    # Obtener las postulaciones del usuario con información completa
    query_postulaciones = """
        SELECT p.id, p.fecha_postulacion, es.estatus as estado, p.fecha_postulacion as fecha_actualizacion,
               v.titulo, e.nombre as empresa, 
               CONCAT(u.ciudad, ', ', u.estado, ', ', u.pais) as ubicacion,
               v.salario_minimo, v.salario_maximo, 
               mt.nombre as modalidad, tt.nombre as tipo_contrato
        FROM postulaciones p
        INNER JOIN vacantes v ON p.id_vacante = v.id
        INNER JOIN empresas e ON v.id_empresa = e.id
        INNER JOIN ubicaciones u ON v.id_ubicacion = u.id
        INNER JOIN modalidades_trabajo mt ON v.id_modalidad_trabajo = mt.id
        INNER JOIN tipos_trabajo tt ON v.id_tipo_trabajo = tt.id
        INNER JOIN estatus es ON p.id_estatus = es.id
        WHERE p.id_usuario = %s
        ORDER BY p.fecha_postulacion DESC
    """
    
    postulaciones = conexion.get_datos_parametrizados(query_postulaciones, (user_id,))
    
    # Formatear las postulaciones para el template
    postulaciones_formateadas = []
    for postulacion in postulaciones:
        postulaciones_formateadas.append({
            'id': postulacion[0],
            'fecha_postulacion': postulacion[1],
            'estado': postulacion[2],
            'fecha_actualizacion': postulacion[3],
            'titulo': postulacion[4],
            'empresa': postulacion[5],
            'ubicacion': postulacion[6],
            'salario_min': postulacion[7],
            'salario_max': postulacion[8],
            'modalidad': postulacion[9],
            'tipo_contrato': postulacion[10]
        })
    
    return render_template('mis_postulaciones.html', postulaciones=postulaciones_formateadas)

@app.route('/aplicar_vacante', methods=['POST'])
def aplicar_vacante():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para continuar'})
    
    user_id = session['user_id']
    vacante_id = request.form.get('vacante_id')
    
    if not vacante_id:
        return jsonify({'success': False, 'message': 'ID de vacante no proporcionado'})
    
    # Verificar si ya se postuló a esta vacante
    query_verificar = "SELECT id FROM postulaciones WHERE id_usuario = %s AND id_vacante = %s"
    postulacion_existente = conexion.get_datos_parametrizados(query_verificar, (user_id, vacante_id))
    
    if postulacion_existente:
        return jsonify({'success': False, 'message': 'Ya te has postulado a esta vacante'})
    
    # Crear la postulación (usando la estructura correcta de la tabla)
    query_insertar = """
        INSERT INTO postulaciones (id_usuario, id_vacante, id_estatus, fecha_postulacion)
        VALUES (%s, %s, 4, NOW())
    """
    
    resultado = conexion.insert_datos_parametrizados(query_insertar, (user_id, vacante_id))
    
    if resultado == 'ok':
        return jsonify({'success': True, 'message': 'Postulación enviada exitosamente'})
    else:
        return jsonify({'success': False, 'message': 'Error al enviar la postulación'})

@app.route('/cancelar_postulacion', methods=['POST'])
def cancelar_postulacion():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para continuar'})
    
    user_id = session['user_id']
    postulacion_id = request.form.get('postulacion_id')
    
    if not postulacion_id:
        return jsonify({'success': False, 'message': 'ID de postulación no proporcionado'})
    
    # Verificar que la postulación pertenece al usuario y está en estado pendiente (id_estatus = 4)
    query_verificar = "SELECT id FROM postulaciones WHERE id = %s AND id_usuario = %s AND id_estatus = 4"
    postulacion_existente = conexion.get_datos_parametrizados(query_verificar, (postulacion_id, user_id))
    
    if not postulacion_existente:
        return jsonify({'success': False, 'message': 'Postulación no encontrada o no se puede cancelar'})
    
    # Cambiar el estado a cancelada (id_estatus = 6 para Rechazado)
    query_actualizar = "UPDATE postulaciones SET id_estatus = 6 WHERE id = %s"
    resultado = conexion.update_datos_parametrizados(query_actualizar, (postulacion_id,))
    
    if resultado.startswith('Registros actualizados'):
        return jsonify({'success': True, 'message': 'Postulación cancelada exitosamente'})
    else:
        return jsonify({'success': False, 'message': 'Error al cancelar la postulación'})

@app.route('/calificar_vacante', methods=['POST'])
def calificar_vacante():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para continuar'})
    
    user_id = session['user_id']
    data = request.get_json()
    vacante_id = data.get('vacante_id')
    calificacion = data.get('calificacion')
    
    if not vacante_id or not calificacion:
        return jsonify({'success': False, 'message': 'Datos incompletos'})
    
    if calificacion < 1 or calificacion > 5:
        return jsonify({'success': False, 'message': 'Calificación inválida'})
    
    # Verificar si ya calificó esta vacante
    query_verificar = "SELECT id FROM calificaciones_vacantes WHERE id_usuario = %s AND id_vacante = %s"
    calificacion_existente = conexion.get_datos_parametrizados(query_verificar, (user_id, vacante_id))
    
    if calificacion_existente:
        # Actualizar calificación existente
        query_actualizar = "UPDATE calificaciones_vacantes SET calificacion = %s, fecha_calificacion = NOW() WHERE id_usuario = %s AND id_vacante = %s"
        resultado = conexion.update_datos_parametrizados(query_actualizar, (calificacion, user_id, vacante_id))
    else:
        # Insertar nueva calificación
        query_insertar = "INSERT INTO calificaciones_vacantes (id_usuario, id_vacante, calificacion, fecha_calificacion) VALUES (%s, %s, %s, NOW())"
        resultado = conexion.insert_datos_parametrizados(query_insertar, (user_id, vacante_id, calificacion))
    
    if resultado:
        return jsonify({'success': True, 'message': 'Calificación enviada exitosamente'})
    else:
        return jsonify({'success': False, 'message': 'Error al enviar la calificación'})

#----------END RUTA DE INFORMACIÓN DEL USUARIO ----------

#----------ADMIN DASHBOARD----------
@app.route('/admin/dashboard')
def admin_dashboard():
    print("DEBUG: Iniciando admin_dashboard")
    
    # Obtener usuarios admin y reclutadores
    query_usuarios = """
        SELECT 
            id, correo, tipo_usuario, username
        FROM login
        WHERE tipo_usuario IN ('admin', 'reclutador')
    """
    print(f"DEBUG: Ejecutando query usuarios: {query_usuarios}")
    usuarios = conexion.get_datos(query_usuarios)
    print(f"DEBUG: Usuarios encontrados: {usuarios}")
    print(f"DEBUG: Tipo de usuarios: {type(usuarios)}")
    print(f"DEBUG: Longitud de usuarios: {len(usuarios) if usuarios else 0}")
    
    # Obtener aspirantes con su información
    query_aspirantes = """
        SELECT 
            i.id_usuario,
            i.nombre,
            i.apellidos,
            l.correo,
            COALESCE(e.empleo, 'No especificado') as empleo_deseado,
            COALESCE(exp.experiencia, 'No especificado') as experiencia,
            COALESCE(g.grado, 'No especificado') as grado_estudios,
            COALESCE(c.ciudad, 'No especificado') as ciudad
        FROM informacion i
        INNER JOIN login l ON i.id_usuario = l.id
        LEFT JOIN empleos e ON i.id_empleos = e.id
        LEFT JOIN experiencia exp ON i.id_experiencia = exp.id
        LEFT JOIN grado_estudios g ON i.id_grado_estudios = g.id
        LEFT JOIN ciudad_referencia c ON i.id_ciudad = c.id
        WHERE l.tipo_usuario = 'aspirante'
        ORDER BY i.nombre, i.apellidos
    """
    print(f"DEBUG: Ejecutando query aspirantes: {query_aspirantes}")
    aspirantes = conexion.get_datos(query_aspirantes)
    print(f"DEBUG: Aspirantes encontrados: {aspirantes}")
    print(f"DEBUG: Tipo de aspirantes: {type(aspirantes)}")
    print(f"DEBUG: Longitud de aspirantes: {len(aspirantes) if aspirantes else 0}")
    
    print(f"DEBUG: Renderizando template con usuarios={usuarios} y aspirantes={aspirantes}")
    return render_template('dashboard_admin.html', usuarios=usuarios, aspirantes=aspirantes)

@app.route('/admin/agregar_usuario', methods=['POST'])
def agregar_usuario():
    username = request.form['username']
    correo = request.form['correo']
    contra = request.form['contra']
    tipo_usuario = request.form['tipo_usuario']
    
    if tipo_usuario in ['admin', 'reclutador']:
        query = f"""
            INSERT INTO login (username, correo, contra, tipo_usuario) 
            VALUES ('{username}', '{correo}', '{contra}', '{tipo_usuario}')
        """
        conexion.insert_datos(query)
        flash('Usuario agregado correctamente.', 'success')
    else:
        flash('Solo puedes agregar administradores o reclutadores.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = conexion.get_datos(f"SELECT tipo_usuario FROM login WHERE id={id}")
    if usuario and usuario[0][0] in ['admin', 'reclutador']:
        conexion.insert_datos(f"DELETE FROM login WHERE id={id}")
        flash('Usuario eliminado correctamente.', 'success')
    else:
        flash('No puedes eliminar aspirantes desde aquí.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/editar_usuario/<int:id>', methods=['POST'])
def editar_usuario(id):
    username = request.form['username']
    correo = request.form['correo']
    contra = request.form['contra']
    tipo_usuario = request.form['tipo_usuario']
    
    if tipo_usuario in ['admin', 'reclutador']:
        update_fields = [
            f"username='{username}'",
            f"correo='{correo}'",
            f"tipo_usuario='{tipo_usuario}'"
        ]
        if contra:  # Solo actualiza si se escribió algo
            update_fields.append(f"contra='{contra}'")
        
        update_query = f"UPDATE login SET {', '.join(update_fields)} WHERE id={id}"
        conexion.insert_datos(update_query)
        flash('Usuario editado correctamente.', 'success')
    else:
        flash('Solo puedes editar administradores o reclutadores.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/editar_aspirante/<int:id>', methods=['POST'])
def editar_aspirante(id):
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    correo = request.form['correo']
    empleo_deseado = request.form['empleo_deseado']
    experiencia = request.form['experiencia']
    grado_estudios = request.form['grado_estudios']
    ciudad = request.form['ciudad']
    
    try:
        # Actualizar correo en tabla login
        update_login = f"UPDATE login SET correo='{correo}' WHERE id={id}"
        conexion.insert_datos(update_login)
        
        # Actualizar información en tabla informacion
        update_info = f"""
            UPDATE informacion 
            SET nombre='{nombre}', apellidos='{apellidos}'
            WHERE id_usuario={id}
        """
        conexion.insert_datos(update_info)
        
        flash('Aspirante editado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al editar aspirante: {e}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/eliminar_aspirante/<int:id>', methods=['POST'])
def eliminar_aspirante(id):
    try:
        # Eliminar de informacion primero (por foreign key)
        conexion.insert_datos(f"DELETE FROM informacion WHERE id_usuario={id}")
        # Luego eliminar de login
        conexion.insert_datos(f"DELETE FROM login WHERE id={id}")
        flash('Aspirante eliminado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar aspirante: {e}', 'error')
    
    return redirect(url_for('admin_dashboard'))
#----------END ADMIN DASHBOARD----------


# --------- RECLUTADOR DASHBOARD ---------
@app.route('/reclutador/dashboard')
def reclutador_dashboard():
    
    return render_template('reclutador/vacantes.html')

@app.route('/reclutador/vacantes')
def reclutador_vacantes():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))
    
    user_id = session['user_id']
    
    # Consulta para obtener las vacantes del usuario logueado
    query = '''
        SELECT v.id, v.titulo, e.nombre as empresa, 
               CONCAT(u.ciudad, ', ', u.estado, ', ', u.pais) as ubicacion,
               DATE_FORMAT(v.fecha_publicacion, '%d %b %Y') as fecha_publicacion,
               (SELECT COUNT(*) FROM postulaciones p WHERE p.id_vacante = v.id) as postulaciones,
               es.estatus as estado
        FROM vacantes v
        INNER JOIN empresas e ON v.id_empresa = e.id
        INNER JOIN ubicaciones u ON v.id_ubicacion = u.id
        LEFT JOIN estado_vacantes ev ON v.id = ev.id_vacante
        LEFT JOIN estatus es ON ev.id_estatus = es.id
        WHERE v.id_usuario = {user_id}
        ORDER BY v.fecha_publicacion DESC
    '''.format(user_id=user_id)
    vacantes = conexion.get_datos(query)
    
    # Consulta de catálogo de estatus (solo los primeros 3 estados)
    estatus_catalogo = conexion.get_datos('SELECT id, estatus FROM estatus WHERE id IN (1,2,3) ORDER BY id')
    
    # Calcular estadísticas
    total_vacantes = len(vacantes)
    vacantes_activas = len([v for v in vacantes if v[6] == 'Activa'])
    total_postulaciones = sum([v[5] for v in vacantes])
    promedio_postulaciones = round(total_postulaciones / total_vacantes, 1) if total_vacantes > 0 else 0
    
    return render_template('reclutador/vacantes.html', 
                         vacantes=vacantes, 
                         estatus_catalogo=estatus_catalogo,
                         total_vacantes=total_vacantes,
                         vacantes_activas=vacantes_activas,
                         total_postulaciones=total_postulaciones,
                         promedio_postulaciones=promedio_postulaciones)


@app.route('/reclutador/postulaciones')
def reclutador_postulaciones():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))
    
    user_id = session['user_id']
    
    try:
        print(f"DEBUG: user_id = {user_id}")
        
        # Consulta para obtener postulaciones de las vacantes del reclutador
        query = '''
            SELECT 
                i.nombre,
                i.apellidos,
                l.correo,
                i.id,
                p.id_usuario,
                v.id,
                v.titulo,
                COALESCE(e.nombre, 'Sin empresa') as empresa_nombre,
                p.fecha_postulacion,
                es.estatus,
                p.id
            FROM postulaciones p
            INNER JOIN vacantes v ON p.id_vacante = v.id
            INNER JOIN login l ON p.id_usuario = l.id
            INNER JOIN informacion i ON l.id = i.id_usuario
            INNER JOIN estatus es ON p.id_estatus = es.id
            LEFT JOIN empresas e ON v.id_empresa = e.id
            WHERE v.id_usuario = %s
            ORDER BY p.fecha_postulacion DESC
        '''
        
        print(f"DEBUG: Query = {query}")
        print(f"DEBUG: Params = {user_id}")
        
        # Usar parámetros seguros para evitar SQL injection
        postulaciones = conexion.get_datos_parametrizados(query, (user_id,))
        
        print(f"DEBUG: Resultado de consulta = {postulaciones}")
        print(f"DEBUG: Tipo de resultado = {type(postulaciones)}")
        print(f"DEBUG: Longitud = {len(postulaciones) if postulaciones else 0}")
        
        # Calcular las estadísticas de las tarjetas
        total_postulaciones = 0
        en_revision = 0
        aceptadas = 0
        rechazadas = 0
        
        if postulaciones:
            total_postulaciones = len(postulaciones)
            en_revision = len([p for p in postulaciones if p[9] == 'En Revisión'])
            aceptadas = len([p for p in postulaciones if p[9] == 'Aceptado'])
            rechazadas = len([p for p in postulaciones if p[9] == 'Rechazado'])
            
            print(f"DEBUG: Estadísticas - Total: {total_postulaciones}, En Revisión: {en_revision}, Aceptadas: {aceptadas}, Rechazadas: {rechazadas}")

        return render_template(
            'reclutador/postulaciones.html',
            postulaciones=postulaciones,
            total_postulaciones=total_postulaciones,
            en_revision=en_revision,
            aceptadas=aceptadas,
            rechazadas=rechazadas
        )
        
    except Exception as e:
        print(f"DEBUG: ERROR = {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f'Error al cargar las postulaciones: {str(e)}', 'error')
        return render_template(
            'reclutador/postulaciones.html',
            postulaciones=[],
            total_postulaciones=0,
            en_revision=0,
            aceptadas=0,
            rechazadas=0
        )

@app.route('/reclutador/postulaciones/<int:id>/cambiar-estado', methods=['POST'])
def cambiar_estado_postulacion(id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'}), 401
    
    try:
        data = request.get_json()
        nuevo_estado = data.get('estado')
        
        if not nuevo_estado:
            return jsonify({'success': False, 'message': 'Estado no especificado'}), 400
        
        # Mapear el estado a ID
        estado_map = {
            'En Revisión': 4,
            'Aceptado': 5,
            'Rechazado': 6
        }
        
        id_estado = estado_map.get(nuevo_estado)
        if not id_estado:
            return jsonify({'success': False, 'message': 'Estado inválido'}), 400
        
        # Verificar que la postulación pertenece a una vacante del reclutador
        user_id = session['user_id']
        query_verificacion = '''
            SELECT p.id FROM postulaciones p
            INNER JOIN vacantes v ON p.id_vacante = v.id
            WHERE p.id = %s AND v.id_usuario = %s
        '''
        
        resultado = conexion.get_datos_parametrizados(query_verificacion, (id, user_id))
        if not resultado:
            return jsonify({'success': False, 'message': 'Postulación no encontrada o no autorizada'}), 404
        
        # Actualizar el estado
        query_update = 'UPDATE postulaciones SET id_estatus = %s WHERE id = %s'
        resultado_update = conexion.update_datos_parametrizados(query_update, (id_estado, id))
        
        if resultado_update.startswith('Registros actualizados'):
            return jsonify({'success': True, 'message': 'Estado actualizado correctamente'})
        else:
            return jsonify({'success': False, 'message': resultado_update}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error interno: {str(e)}'}), 500

@app.route('/reclutador/candidato/<int:id>')
def reclutador_candidato(id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver este perfil', 'error')
        return redirect(url_for('user_login'))
    
    try:
        conexion = ConexionDB()
        if not conexion.connection:
            flash('Error de conexión a la base de datos', 'error')
            return redirect(url_for('reclutador_postulaciones'))
        
        # Obtener información del candidato
        query_candidato = '''
            SELECT 
                i.nombre,
                i.apellidos,
                l.correo as email,
                i.id_empleos,
                i.id_experiencia,
                i.id_grado_estudios,
                i.id_ciudad,
                i.id_cp
            FROM informacion i
            INNER JOIN login l ON i.id_usuario = l.id
            WHERE i.id_usuario = %s
        '''
        
        candidato_data = conexion.get_datos_parametrizados(query_candidato, (id,))
        
        if not candidato_data:
            flash('Candidato no encontrado', 'error')
            return redirect(url_for('reclutador_postulaciones'))
        
        candidato = candidato_data[0]
        
        # Obtener nombres descriptivos de los IDs
        empleo_query = "SELECT nombre FROM empleos WHERE id = %s"
        experiencia_query = "SELECT nombre FROM experiencia WHERE id = %s"
        estudios_query = "SELECT nombre FROM grado_estudios WHERE id = %s"
        ciudad_query = "SELECT ciudad FROM ubicaciones WHERE id = %s"
        cp_query = "SELECT cp FROM codigos_postales WHERE id = %s"
        
        # Obtener empleo deseado
        empleo_result = conexion.get_datos_parametrizados(empleo_query, (candidato[3],)) if candidato[3] else None
        empleo_deseado = empleo_result[0][0] if empleo_result else None
        
        # Obtener experiencia
        experiencia_result = conexion.get_datos_parametrizados(experiencia_query, (candidato[4],)) if candidato[4] else None
        experiencia = experiencia_result[0][0] if experiencia_result else None
        
        # Obtener grado de estudios
        estudios_result = conexion.get_datos_parametrizados(estudios_query, (candidato[5],)) if candidato[5] else None
        grado_estudios = estudios_result[0][0] if estudios_result else None
        
        # Obtener ciudad
        ciudad_result = conexion.get_datos_parametrizados(ciudad_query, (candidato[6],)) if candidato[6] else None
        ciudad = ciudad_result[0][0] if ciudad_result else None
        
        # Obtener código postal
        cp_result = conexion.get_datos_parametrizados(cp_query, (candidato[7],)) if candidato[7] else None
        codigo_postal = cp_result[0][0] if cp_result else None
        
        # Crear objeto candidato con datos procesados
        candidato_info = {
            'nombre': candidato[0],
            'apellidos': candidato[1],
            'email': candidato[2],
            'empleo_deseado': empleo_deseado,
            'experiencia': experiencia,
            'grado_estudios': grado_estudios,
            'ciudad': ciudad,
            'codigo_postal': codigo_postal
        }
        
        return render_template('reclutador/candidato.html', candidato=candidato_info)
        
    except Exception as e:
        print(f"Error en reclutador_candidato: {e}")
        flash('Error al cargar el perfil del candidato', 'error')
        return redirect(url_for('reclutador_postulaciones'))

@app.route('/reclutador/crear_vacante', methods=['GET', 'POST'])
def reclutador_crear_vacante():
    if request.method == 'POST':
        conexion = None
        cursor = None
        try:
            # Obtener datos del formulario
            titulo = request.form['job_title']
            nombre_empresa = request.form['company']
            ubicacion_str = request.form['location']
            tipo_trabajo = request.form['job_type']
            modalidad = request.form['work_mode']
            salario_min = request.form.get('salary_min')
            salario_max = request.form.get('salary_max')
            experiencia = request.form['experience_level']
            fecha_limite = request.form.get('deadline')
            num_vacantes = request.form.get('vacancies_count', 1)
            descripcion = request.form['job_description']
            requisitos = request.form['requirements']
            beneficios = request.form.get('benefits', '')
            email_contacto = request.form['contact_email']
            telefono_contacto = request.form.get('contact_phone', '')
            habilidades_req = [h.strip() for h in request.form.get('skills', '').split(',') if h.strip()]
            habilidades_des = [h.strip() for h in request.form.get('nice_to_have', '').split(',') if h.strip()]

            # Procesar ubicación (ciudad, estado, país)
            ubicacion_parts = [part.strip() for part in ubicacion_str.split(',')]
            ciudad = ubicacion_parts[0] if len(ubicacion_parts) > 0 else ''
            estado = ubicacion_parts[1] if len(ubicacion_parts) > 1 else ''
            pais = ubicacion_parts[2] if len(ubicacion_parts) > 2 else ''

            # Mapear valores de los select a IDs de la base de datos
            tipo_trabajo_map = {
                'full-time': 1,
                'part-time': 2,
                'contract': 3,
                'internship': 4
            }
            
            modalidad_map = {
                'presencial': 1,
                'remote': 2,
                'hybrid': 3
            }
            
            experiencia_map = {
                'entry': 1,
                'junior': 2,
                'mid': 3,
                'senior': 4,
                'lead': 5
            }

            # Iniciar conexión usando tu clase ConexionDB
            conexion = ConexionDB()
            if not conexion.connection:
                flash(f'Error de conexión: {conexion.errMss}', 'danger')
                return redirect(url_for('reclutador_crear_vacante'))

            cursor = conexion.connection.cursor(dictionary=True)

            # 1. Insertar empresa si no existe
            cursor.execute("SELECT id FROM empresas WHERE nombre = %s", (nombre_empresa,))
            empresa = cursor.fetchone()
            if not empresa:
                cursor.execute("INSERT INTO empresas (nombre) VALUES (%s)", (nombre_empresa,))
                empresa_id = cursor.lastrowid
                conexion.connection.commit()
            else:
                empresa_id = empresa['id']

            # 2. Insertar ubicación si no existe
            cursor.execute(
                "SELECT id FROM ubicaciones WHERE ciudad = %s AND estado = %s AND pais = %s",
                (ciudad, estado, pais)
            )
            ubicacion = cursor.fetchone()
            if not ubicacion:
                cursor.execute(
                    "INSERT INTO ubicaciones (ciudad, estado, pais) VALUES (%s, %s, %s)",
                    (ciudad, estado, pais)
                )
                ubicacion_id = cursor.lastrowid
                conexion.connection.commit()
            else:
                ubicacion_id = ubicacion['id']

            # 3. Insertar la vacante (ahora incluye id_usuario)
            id_usuario = session.get('user_id')
            cursor.execute(
                """INSERT INTO vacantes (
                    id_usuario, id_empresa, titulo, id_ubicacion, id_tipo_trabajo, 
                    id_modalidad_trabajo, salario_minimo, salario_maximo, 
                    id_nivel_experiencia, fecha_limite, numero_vacantes, 
                    descripcion, requisitos, beneficios, email_contacto, 
                    telefono_contacto
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    id_usuario, empresa_id, titulo, ubicacion_id, tipo_trabajo_map[tipo_trabajo],
                    modalidad_map[modalidad], salario_min, salario_max,
                    experiencia_map[experiencia], fecha_limite, num_vacantes,
                    descripcion, requisitos, beneficios, email_contacto,
                    telefono_contacto
                )
            )
            vacante_id = cursor.lastrowid
            conexion.connection.commit()

            # 4. Procesar habilidades requeridas
            for habilidad in habilidades_req:
                # Verificar si la habilidad existe
                cursor.execute("SELECT id FROM habilidades WHERE nombre = %s", (habilidad,))
                habilidad_db = cursor.fetchone()
                if not habilidad_db:
                    cursor.execute("INSERT INTO habilidades (nombre) VALUES (%s)", (habilidad,))
                    habilidad_id = cursor.lastrowid
                    conexion.connection.commit()
                else:
                    habilidad_id = habilidad_db['id']
                
                # Relacionar habilidad con vacante
                cursor.execute(
                    "INSERT INTO vacantes_habilidades_requeridas (id_vacante, id_habilidad) VALUES (%s, %s)",
                    (vacante_id, habilidad_id)
                )
                conexion.connection.commit()

            # 5. Procesar habilidades deseadas
            for habilidad in habilidades_des:
                # Verificar si la habilidad existe
                cursor.execute("SELECT id FROM habilidades WHERE nombre = %s", (habilidad,))
                habilidad_db = cursor.fetchone()
                if not habilidad_db:
                    cursor.execute("INSERT INTO habilidades (nombre) VALUES (%s)", (habilidad,))
                    habilidad_id = cursor.lastrowid
                    conexion.connection.commit()
                else:
                    habilidad_id = habilidad_db['id']
                
                # Relacionar habilidad con vacante
                cursor.execute(
                    "INSERT INTO vacantes_habilidades_deseadas (id_vacante, id_habilidad) VALUES (%s, %s)",
                    (vacante_id, habilidad_id)
                )
                conexion.connection.commit()

            flash('Vacante creada exitosamente!', 'success')
            return redirect(url_for('reclutador_vacantes'))

        except mysql.connector.Error as err:
            if conexion and conexion.connection:
                conexion.connection.rollback()
            flash(f'Error al crear la vacante: {err}', 'danger')
        except Exception as ex:
            flash(f'Error inesperado: {ex}', 'danger')
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.connection:
                conexion.connection.close()

    # Para el método GET, simplemente renderizar el template
    return render_template('reclutador/crear_vacante.html')   


@app.route('/reclutador/vacantes/crear', methods=['POST'])
def crear_vacante_ajax():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Validar datos requeridos
        if not data.get('titulo') or not data.get('empresa') or not data.get('ubicacion'):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Procesar ubicación
        ubicacion_parts = [part.strip() for part in data['ubicacion'].split(',')]
        ciudad = ubicacion_parts[0] if len(ubicacion_parts) > 0 else ''
        estado = ubicacion_parts[1] if len(ubicacion_parts) > 1 else ''
        pais = ubicacion_parts[2] if len(ubicacion_parts) > 2 else 'México'
        
        # Mapear valores según los catálogos de la DB
        tipo_trabajo_map = {
            'full-time': 1,      # Tiempo Completo
            'part-time': 2,      # Medio Tiempo
            'contract': 3,       # Por Contrato
            'internship': 4      # Prácticas
        }
        
        modalidad_map = {
            'presencial': 1,     # Presencial
            'remote': 2,         # Remoto
            'hybrid': 3          # Híbrido
        }
        
        nivel_experiencia_map = {
            'entry': 1,          # Sin experiencia
            'junior': 2,         # Junior (1-3 años)
            'mid': 3,            # Mid-level (3-5 años)
            'senior': 4,         # Senior (5+ años)
            'lead': 5            # Lead/Manager
        }
        
        # 1. Insertar empresa si no existe
        empresa_query = f"SELECT id FROM empresas WHERE nombre = '{data['empresa']}'"
        empresa = conexion.get_datos(empresa_query)
        if not empresa:
            conexion.insert_datos(f"INSERT INTO empresas (nombre) VALUES ('{data['empresa']}')")
            empresa_id = conexion.cursor.lastrowid
        else:
            empresa_id = empresa[0][0]
        
        # 2. Insertar ubicación si no existe
        ubicacion_query = f"SELECT id FROM ubicaciones WHERE ciudad = '{ciudad}' AND estado = '{estado}' AND pais = '{pais}'"
        ubicacion = conexion.get_datos(ubicacion_query)
        if not ubicacion:
            conexion.insert_datos(f"INSERT INTO ubicaciones (ciudad, estado, pais) VALUES ('{ciudad}', '{estado}', '{pais}')")
            ubicacion_id = conexion.cursor.lastrowid
        else:
            ubicacion_id = ubicacion[0][0]
        
        # 3. Insertar vacante con todos los campos de la DB
        tipo_trabajo_id = tipo_trabajo_map.get(data.get('job_type', 'full-time'), 1)
        modalidad_id = modalidad_map.get(data.get('work_mode', 'presencial'), 1)
        nivel_experiencia_id = nivel_experiencia_map.get(data.get('experience_level', 'entry'), 1)
        
        # Procesar salario
        salario_minimo = data.get('salary_min') if data.get('salary_min') else None
        salario_maximo = data.get('salary_max') if data.get('salary_max') else None
        
        # Procesar fecha límite
        fecha_limite = data.get('deadline') if data.get('deadline') else None
        
        vacante_query = f"""
            INSERT INTO vacantes (
                id_usuario, id_empresa, titulo, id_ubicacion, id_tipo_trabajo, 
                id_modalidad_trabajo, salario_minimo, salario_maximo, id_nivel_experiencia,
                fecha_limite, numero_vacantes, descripcion, requisitos, beneficios,
                email_contacto, telefono_contacto
            ) VALUES (
                {user_id}, {empresa_id}, '{data['titulo']}', {ubicacion_id}, {tipo_trabajo_id}, 
                {modalidad_id}, {salario_minimo or 'NULL'}, {salario_maximo or 'NULL'}, {nivel_experiencia_id},
                {f"'{fecha_limite}'" if fecha_limite else 'NULL'}, {data.get('vacancies_count', 1)},
                '{data.get('job_description', '')}', '{data.get('requirements', '')}', '{data.get('benefits', '')}',
                '{data.get('contact_email', '')}', '{data.get('contact_phone', '')}'
            )
        """
        conexion.insert_datos(vacante_query)
        vacante_id = conexion.cursor.lastrowid
        
        # 4. Procesar habilidades requeridas
        if data.get('skills'):
            habilidades_req = [h.strip() for h in data['skills'].split(',') if h.strip()]
            for habilidad in habilidades_req:
                # Verificar si la habilidad existe
                habilidad_query = f"SELECT id FROM habilidades WHERE nombre = '{habilidad}'"
                habilidad_db = conexion.get_datos(habilidad_query)
                if not habilidad_db:
                    conexion.insert_datos(f"INSERT INTO habilidades (nombre) VALUES ('{habilidad}')")
                    habilidad_id = conexion.cursor.lastrowid
                else:
                    habilidad_id = habilidad_db[0][0]
                
                # Relacionar habilidad con vacante
                conexion.insert_datos(f"INSERT INTO vacantes_habilidades_requeridas (id_vacante, id_habilidad) VALUES ({vacante_id}, {habilidad_id})")
        
        # 5. Procesar habilidades deseadas
        if data.get('nice_to_have'):
            habilidades_des = [h.strip() for h in data['nice_to_have'].split(',') if h.strip()]
            for habilidad in habilidades_des:
                # Verificar si la habilidad existe
                habilidad_query = f"SELECT id FROM habilidades WHERE nombre = '{habilidad}'"
                habilidad_db = conexion.get_datos(habilidad_query)
                if not habilidad_db:
                    conexion.insert_datos(f"INSERT INTO habilidades (nombre) VALUES ('{habilidad}')")
                    habilidad_id = conexion.cursor.lastrowid
                else:
                    habilidad_id = habilidad_db[0][0]
                
                # Relacionar habilidad con vacante
                conexion.insert_datos(f"INSERT INTO vacantes_habilidades_deseadas (id_vacante, id_habilidad) VALUES ({vacante_id}, {habilidad_id})")
        
        # 6. Insertar estado inicial (Activa = 1)
        conexion.insert_datos(f"INSERT INTO estado_vacantes (id_vacante, id_estatus) VALUES ({vacante_id}, 1)")
        
        return jsonify({'success': True, 'vacante_id': vacante_id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reclutador/vacantes/<int:vacante_id>/datos')
def obtener_datos_vacante(vacante_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        user_id = session['user_id']
        query = f"""
            SELECT v.titulo, e.nombre as empresa, 
                   CONCAT(u.ciudad, ', ', u.estado, ', ', u.pais) as ubicacion,
                   tt.nombre as tipo_trabajo, mt.nombre as modalidad,
                   v.salario_minimo, v.salario_maximo, v.descripcion,
                   es.estatus as estado, v.email_contacto, v.telefono_contacto,
                   v.requisitos, v.beneficios, ne.nombre as nivel_experiencia
            FROM vacantes v
            INNER JOIN empresas e ON v.id_empresa = e.id
            INNER JOIN ubicaciones u ON v.id_ubicacion = u.id
            INNER JOIN tipos_trabajo tt ON v.id_tipo_trabajo = tt.id
            INNER JOIN modalidades_trabajo mt ON v.id_modalidad_trabajo = mt.id
            INNER JOIN niveles_experiencia ne ON v.id_nivel_experiencia = ne.id
            LEFT JOIN estado_vacantes ev ON v.id = ev.id_vacante
            LEFT JOIN estatus es ON ev.id_estatus = es.id
            WHERE v.id = {vacante_id} AND v.id_usuario = {user_id}
        """
        resultado = conexion.get_datos(query)
        
        if not resultado:
            return jsonify({'error': 'Vacante no encontrada'}), 404
        
        vacante = resultado[0]
        return jsonify({
            'titulo': vacante[0],
            'empresa': vacante[1],
            'ubicacion': vacante[2],
            'tipo_trabajo': vacante[3],
            'modalidad': vacante[4],
            'salario_minimo': vacante[5],
            'salario_maximo': vacante[6],
            'descripcion': vacante[7],
            'estado': vacante[8],
            'email_contacto': vacante[9],
            'telefono_contacto': vacante[10],
            'requisitos': vacante[11],
            'beneficios': vacante[12],
            'nivel_experiencia': vacante[13]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reclutador/vacantes/<int:vacante_id>/detalles')
def obtener_detalles_vacante(vacante_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        user_id = session['user_id']
        query = f"""
            SELECT v.titulo, e.nombre as empresa, 
                   CONCAT(u.ciudad, ', ', u.estado, ', ', u.pais) as ubicacion,
                   tt.nombre as tipo_trabajo, mt.nombre as modalidad,
                   v.salario_minimo, v.salario_maximo, v.descripcion,
                   es.estatus as estado, v.fecha_publicacion,
                   (SELECT COUNT(*) FROM postulaciones p WHERE p.id_vacante = v.id) as postulaciones,
                   v.requisitos, v.beneficios, ne.nombre as nivel_experiencia,
                   v.fecha_limite, v.numero_vacantes
            FROM vacantes v
            INNER JOIN empresas e ON v.id_empresa = e.id
            INNER JOIN ubicaciones u ON v.id_ubicacion = u.id
            INNER JOIN tipos_trabajo tt ON v.id_tipo_trabajo = tt.id
            INNER JOIN modalidades_trabajo mt ON v.id_modalidad_trabajo = mt.id
            INNER JOIN niveles_experiencia ne ON v.id_nivel_experiencia = ne.id
            LEFT JOIN estado_vacantes ev ON v.id = ev.id_vacante
            LEFT JOIN estatus es ON ev.id_estatus = es.id
            WHERE v.id = {vacante_id} AND v.id_usuario = {user_id}
        """
        resultado = conexion.get_datos(query)
        
        if not resultado:
            return jsonify({'error': 'Vacante no encontrada'}), 404
        
        vacante = resultado[0]
        # Obtener habilidades requeridas
        habilidades_req = conexion.get_datos(f"""
            SELECT h.nombre FROM vacantes_habilidades_requeridas vhr
            INNER JOIN habilidades h ON vhr.id_habilidad = h.id
            WHERE vhr.id_vacante = {vacante_id}
        """)
        habilidades_req = [h[0] for h in habilidades_req] if habilidades_req else []
        # Obtener habilidades deseadas
        habilidades_des = conexion.get_datos(f"""
            SELECT h.nombre FROM vacantes_habilidades_deseadas vhd
            INNER JOIN habilidades h ON vhd.id_habilidad = h.id
            WHERE vhd.id_vacante = {vacante_id}
        """)
        habilidades_des = [h[0] for h in habilidades_des] if habilidades_des else []
        return jsonify({
            'titulo': vacante[0],
            'empresa': vacante[1],
            'ubicacion': vacante[2],
            'tipo_trabajo': vacante[3],
            'modalidad': vacante[4],
            'salario_minimo': vacante[5],
            'salario_maximo': vacante[6],
            'descripcion': vacante[7],
            'estado': vacante[8],
            'fecha_creacion': vacante[9].strftime('%d/%m/%Y') if vacante[9] else '',
            'postulaciones': vacante[10],
            'requisitos': vacante[11],
            'beneficios': vacante[12],
            'nivel_experiencia': vacante[13],
            'fecha_limite': vacante[14].strftime('%d/%m/%Y') if vacante[14] else None,
            'numero_vacantes': vacante[15],
            'habilidades_requeridas': habilidades_req,
            'habilidades_deseadas': habilidades_des
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reclutador/vacantes/<int:vacante_id>/editar', methods=['POST'])
def editar_vacante_ajax(vacante_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Verificar que la vacante pertenece al usuario
        vacante_check = conexion.get_datos(f"SELECT id FROM vacantes WHERE id = {vacante_id} AND id_usuario = {user_id}")
        if not vacante_check:
            return jsonify({'error': 'Vacante no encontrada o sin permisos'}), 404
        
        # Validar datos requeridos
        if not data.get('titulo') or not data.get('empresa') or not data.get('ubicacion'):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Procesar ubicación
        ubicacion_parts = [part.strip() for part in data['ubicacion'].split(',')]
        ciudad = ubicacion_parts[0] if len(ubicacion_parts) > 0 else ''
        estado = ubicacion_parts[1] if len(ubicacion_parts) > 1 else ''
        pais = ubicacion_parts[2] if len(ubicacion_parts) > 2 else 'México'
        
        # Mapear valores según los catálogos de la DB
        tipo_trabajo_map = {
            'full-time': 1,      # Tiempo Completo
            'part-time': 2,      # Medio Tiempo
            'contract': 3,       # Por Contrato
            'internship': 4      # Prácticas
        }
        
        modalidad_map = {
            'presencial': 1,     # Presencial
            'remote': 2,         # Remoto
            'hybrid': 3          # Híbrido
        }
        
        nivel_experiencia_map = {
            'entry': 1,          # Sin experiencia
            'junior': 2,         # Junior (1-3 años)
            'mid': 3,            # Mid-level (3-5 años)
            'senior': 4,         # Senior (5+ años)
            'lead': 5            # Lead/Manager
        }
        
        # 1. Actualizar empresa
        empresa_query = f"SELECT id FROM empresas WHERE nombre = '{data['empresa']}'"
        empresa = conexion.get_datos(empresa_query)
        if not empresa:
            conexion.insert_datos(f"INSERT INTO empresas (nombre) VALUES ('{data['empresa']}')")
            empresa_id = conexion.cursor.lastrowid
        else:
            empresa_id = empresa[0][0]
        
        # 2. Actualizar ubicación
        ubicacion_query = f"SELECT id FROM ubicaciones WHERE ciudad = '{ciudad}' AND estado = '{estado}' AND pais = '{pais}'"
        ubicacion = conexion.get_datos(ubicacion_query)
        if not ubicacion:
            conexion.insert_datos(f"INSERT INTO ubicaciones (ciudad, estado, pais) VALUES ('{ciudad}', '{estado}', '{pais}')")
            ubicacion_id = conexion.cursor.lastrowid
        else:
            ubicacion_id = ubicacion[0][0]
        
        # 3. Actualizar vacante con todos los campos
        tipo_trabajo_id = tipo_trabajo_map.get(data.get('job_type', 'full-time'), 1)
        modalidad_id = modalidad_map.get(data.get('work_mode', 'presencial'), 1)
        nivel_experiencia_id = nivel_experiencia_map.get(data.get('experience_level', 'entry'), 1)
        
        # Procesar salario
        salario_minimo = data.get('salary_min') if data.get('salary_min') else None
        salario_maximo = data.get('salary_max') if data.get('salary_max') else None
        
        # Procesar fecha límite
        fecha_limite = data.get('deadline') if data.get('deadline') else None
        
        update_query = f"""
            UPDATE vacantes SET 
                id_empresa = {empresa_id},
                titulo = '{data['titulo']}',
                id_ubicacion = {ubicacion_id},
                id_tipo_trabajo = {tipo_trabajo_id},
                id_modalidad_trabajo = {modalidad_id},
                id_nivel_experiencia = {nivel_experiencia_id},
                salario_minimo = {salario_minimo or 'NULL'},
                salario_maximo = {salario_maximo or 'NULL'},
                fecha_limite = {f"'{fecha_limite}'" if fecha_limite else 'NULL'},
                numero_vacantes = {data.get('vacancies_count', 1)},
                descripcion = '{data.get('job_description', '')}',
                requisitos = '{data.get('requirements', '')}',
                beneficios = '{data.get('benefits', '')}',
                email_contacto = '{data.get('contact_email', '')}',
                telefono_contacto = '{data.get('contact_phone', '')}'
            WHERE id = {vacante_id} AND id_usuario = {user_id}
        """
        conexion.update_datos(update_query)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reclutador/vacantes/<int:vacante_id>/eliminar', methods=['POST'])
def eliminar_vacante_ajax(vacante_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        user_id = session['user_id']
        
        # Verificar que la vacante pertenece al usuario
        vacante_check = conexion.get_datos(f"SELECT id FROM vacantes WHERE id = {vacante_id} AND id_usuario = {user_id}")
        if not vacante_check:
            return jsonify({'error': 'Vacante no encontrada o sin permisos'}), 404
        
        # Primero eliminar las relaciones dependientes
        # Eliminar habilidades requeridas
        conexion.delete_datos(f"DELETE FROM vacantes_habilidades_requeridas WHERE id_vacante = {vacante_id}")
        
        # Eliminar habilidades deseadas
        conexion.delete_datos(f"DELETE FROM vacantes_habilidades_deseadas WHERE id_vacante = {vacante_id}")
        
        # Eliminar estado de vacante
        conexion.delete_datos(f"DELETE FROM estado_vacantes WHERE id_vacante = {vacante_id}")
        
        # Eliminar postulaciones si existen
        conexion.delete_datos(f"DELETE FROM postulaciones WHERE id_vacante = {vacante_id}")
        
        # Finalmente eliminar la vacante
        resultado = conexion.delete_datos(f"DELETE FROM vacantes WHERE id = {vacante_id} AND id_usuario = {user_id}")
        
        if "Error" in resultado:
            return jsonify({'error': resultado}), 500
        
        return jsonify({'success': True, 'message': 'Vacante eliminada exitosamente'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reclutador/vacantes/<int:vacante_id>/cambiar-estado', methods=['POST'])
def cambiar_estado_vacante_ajax(vacante_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        data = request.get_json()
        nuevo_estado = data.get('estado')
        user_id = session['user_id']
        
        if not nuevo_estado:
            return jsonify({'error': 'Estado no especificado'}), 400
        
        # Verificar que la vacante pertenece al usuario
        vacante_check = conexion.get_datos(f"SELECT id FROM vacantes WHERE id = {vacante_id} AND id_usuario = {user_id}")
        if not vacante_check:
            return jsonify({'error': 'Vacante no encontrada o sin permisos'}), 404
        
        # Verificar si ya existe un registro de estado
        existe = conexion.get_datos(f"SELECT id FROM estado_vacantes WHERE id_vacante = {vacante_id}")
        if existe:
            conexion.update_datos(f"UPDATE estado_vacantes SET id_estatus = {nuevo_estado} WHERE id_vacante = {vacante_id}")
        else:
            conexion.insert_datos(f"INSERT INTO estado_vacantes (id_vacante, id_estatus) VALUES ({vacante_id}, {nuevo_estado})")
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reclutador/vacantes/<int:vacante_id>/estado', methods=['POST'])
def cambiar_estado_vacante(vacante_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))
    nuevo_estado = request.form.get('estado')
    existe = conexion.get_datos(f"SELECT id FROM estado_vacantes WHERE id_vacante={vacante_id}")
    if existe:
        conexion.update_datos(f"UPDATE estado_vacantes SET id_estatus={nuevo_estado} WHERE id_vacante={vacante_id}")
    else:
        conexion.insert_datos(f"INSERT INTO estado_vacantes (id_vacante, id_estatus) VALUES ({vacante_id}, {nuevo_estado})")
    flash('Estado de la vacante actualizado.', 'success')
    return redirect(url_for('reclutador_vacantes'))

@app.route('/reclutador/vacantes/<int:vacante_id>/editar', methods=['GET', 'POST'])
def editar_vacante(vacante_id):
    return "Edición de vacante (pendiente de implementar)"



@app.route('/reclutador/vacantes/buscar', methods=['POST'])
def buscar_vacantes_ajax():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Obtener parámetros de búsqueda
        search_term = data.get('search', '').strip()
        status_filter = data.get('status', '')
        type_filter = data.get('type', '')
        
        # Construir la consulta base
        base_query = '''
            SELECT v.id, v.titulo, e.nombre as empresa, 
                   CONCAT(u.ciudad, ', ', u.estado, ', ', u.pais) as ubicacion,
                   DATE_FORMAT(v.fecha_publicacion, '%d %b %Y') as fecha_publicacion,
                   (SELECT COUNT(*) FROM postulaciones p WHERE p.id_vacante = v.id) as postulaciones,
                   es.estatus as estado
            FROM vacantes v
            INNER JOIN empresas e ON v.id_empresa = e.id
            INNER JOIN ubicaciones u ON v.id_ubicacion = u.id
            LEFT JOIN estado_vacantes ev ON v.id = ev.id_vacante
            LEFT JOIN estatus es ON ev.id_estatus = es.id
            WHERE v.id_usuario = {user_id}
        '''.format(user_id=user_id)
        
        # Agregar filtros
        conditions = []
        params = []
        
        if search_term:
            conditions.append("""
                (v.titulo LIKE %s OR e.nombre LIKE %s OR 
                 CONCAT(u.ciudad, ', ', u.estado, ', ', u.pais) LIKE %s)
            """)
            search_pattern = f'%{search_term}%'
            params.extend([search_pattern, search_pattern, search_pattern])
        
        if status_filter:
            conditions.append("es.estatus = %s")
            params.append(status_filter)
        
        if type_filter:
            # Mapear tipo de trabajo a ID
            tipo_map = {
                'Tiempo Completo': 1,
                'Medio Tiempo': 2,
                'Por Contrato': 3,
                'Prácticas': 4
            }
            tipo_id = tipo_map.get(type_filter)
            if tipo_id:
                conditions.append("v.id_tipo_trabajo = %s")
                params.append(tipo_id)
        
        # Agregar condiciones a la consulta
        if conditions:
            base_query += " AND " + " AND ".join(conditions)
        
        base_query += " ORDER BY v.fecha_publicacion DESC"
        
        # Ejecutar consulta
        conexion.cursor.execute(base_query, params)
        vacantes = conexion.cursor.fetchall()
        
        # Calcular estadísticas actualizadas
        total_vacantes = len(vacantes)
        vacantes_activas = len([v for v in vacantes if v[6] == 'Activa'])
        total_postulaciones = sum([v[5] for v in vacantes])
        
        # Obtener catálogo de estatus (solo los primeros 3 estados)
        estatus_catalogo = conexion.get_datos('SELECT id, estatus FROM estatus WHERE id IN (1,2,3) ORDER BY id')
        
        return jsonify({
            'vacantes': vacantes,
            'estatus_catalogo': estatus_catalogo,
            'total_vacantes': total_vacantes,
            'vacantes_activas': vacantes_activas,
            'total_postulaciones': total_postulaciones
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#---------- END RECLUTADOR DASHBOARD ---------

#---------- RUTA DE CIERRE DE SESIÓN ----------
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('inicio'))
#----------------------------------------------

#---------- RUTA DE EDITAR PERFIL ----------
@app.route('/user/editar_perfil', methods=['GET', 'POST'])
def editar_perfil_usuario():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))

    user_id = session['user_id']

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        empleo = request.form.get('empleos_deseados')
        experiencia = request.form.get('experiencia_previa')
        grado = request.form.get('grado_estudio')
        ciudad = request.form.get('ciudad')
        cp = request.form.get('codigo_postal')

        try:
            # Buscar IDs relacionados igual que en info()
            id_empleo = conexion.get_datos(f"SELECT id FROM empleos WHERE empleo LIKE BINARY '{empleo}' LIMIT 1")[0][0]
            id_exp = conexion.get_datos(f"SELECT id FROM experiencia WHERE experiencia LIKE BINARY '{experiencia}' LIMIT 1")[0][0]
            id_grado = conexion.get_datos(f"SELECT id FROM grado_estudios WHERE grado LIKE BINARY '{grado}' LIMIT 1")[0][0]
            id_ciudad = conexion.get_datos(f"SELECT id FROM ciudad_referencia WHERE ciudad LIKE BINARY '{ciudad}' LIMIT 1")[0][0]

            # Insertar CP si no existe
            id_cp_data = conexion.get_datos(f"SELECT id FROM cp WHERE cp = '{cp}' LIMIT 1")
            if not id_cp_data:
                conexion.insert_datos(f"INSERT INTO cp (cp) VALUES ('{cp}')")
                id_cp_data = conexion.get_datos(f"SELECT id FROM cp WHERE cp = '{cp}' ORDER BY id DESC LIMIT 1")
            id_cp = id_cp_data[0][0]

            # Actualizar datos
            update_query = f"""
                UPDATE informacion
                SET nombre = '{nombre}', apellidos = '{apellidos}',
                    id_empleos = {id_empleo}, id_experiencia = {id_exp},
                    id_grado_estudios = {id_grado}, id_ciudad = {id_ciudad},
                    id_cp = {id_cp}
                WHERE id_usuario = {user_id}
            """
            conexion.insert_datos(update_query)

            flash('Perfil actualizado correctamente.', 'success')
            return redirect(url_for('perfil_usuario'))

        except Exception as e:
            flash(f'Error al actualizar: {e}', 'error')

    # Si es GET, traer datos actuales para mostrarlos en el formulario
    query = f"""
        SELECT nombre, apellidos, empleos.empleo, experiencia.experiencia, 
               grado_estudios.grado, ciudad_referencia.ciudad, cp.cp
        FROM informacion
        INNER JOIN empleos ON informacion.id_empleos = empleos.id
        INNER JOIN experiencia ON informacion.id_experiencia = experiencia.id
        INNER JOIN grado_estudios ON informacion.id_grado_estudios = grado_estudios.id
        INNER JOIN ciudad_referencia ON informacion.id_ciudad = ciudad_referencia.id
        INNER JOIN cp ON informacion.id_cp = cp.id
        WHERE informacion.id_usuario = {user_id}
    """
    datos = conexion.get_datos(query)
    if not datos:
        flash("No tienes información registrada. Por favor complétala primero.", "info")
        return redirect(url_for('info'))

    usuario = {
        'nombre': datos[0][0],
        'apellidos': datos[0][1],
        'empleo': datos[0][2],
        'experiencia': datos[0][3],
        'grado': datos[0][4],
        'ciudad': datos[0][5],
        'codigo_postal': datos[0][6]
    }

    return render_template('editar_perfil.html', usuario=usuario)
#----------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)