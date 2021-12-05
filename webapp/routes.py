from flask import render_template, request, redirect, url_for, flash, Response
from webapp import app, db, bcrypt, Download_FOLDER
from webapp.forms import  *
from webapp.models import *
from flask_login import login_user, current_user, logout_user, login_required
import os
import pdfkit, os, uuid
from webapp.registros import *
from webapp.utils import *

@app.route("/", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
        
    form = Login()
    if form.validate_on_submit():
        user = Laboratorista.query.filter_by(username= form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('menu'))
            else:
                flash("Contraseña Incorrecta.","danger")
        else:
            flash("Login invalido, Revisa tus credenciales","danger")

    return render_template("login.html", form=form)


@app.route("/menu", methods=["GET","POST"])
@login_required
def menu():    
    user_type = current_user.role
    return render_template("menu.html", user_type=user_type, menu_items=menu)



@app.route("/buscador/<elemento>" ,methods=["GET", "POST"])
@login_required
def buscador(elemento):
    search_form = Buscar()

    # Largo de Table Header
    table = TableValues(elemento)

    table_header = table['table_header']
    if table['breakpoint']:
        index = table_header.index(table['breakpoint'])
        table_header = table_header[0:index]

    # Filtar con busqueda
   
    if search_form.validate_on_submit():
        kwargs = {table['search_item']: search_form.value.data}    
        table_items = table['model'].query.filter_by(**kwargs)
    else:
        table_items = table['model'].query.all()

    
    if 'error message' in table:
        flash(table['error message'], table['type'])
        return redirect(url_for('menu'))
    
    return render_template("buscador.html", 
    elemento=str(elemento).capitalize(), 
    table_items=table_items, 
    table_header=table_header, 
    search_item = table['search_item'].upper(),
    # Formularios a usar
    form=search_form)

@app.route("/register/<elemento>",methods=["GET", "POST"], defaults={'l_nuevo': None} )
@app.route("/register/<elemento>/<l_nuevo>",methods=["GET", "POST"])
@login_required
def formulario(elemento, l_nuevo):
    elemento = elemento.lower()
    modalForm = {
        'laboratorista' : RegiseterLab(),
        'clientes' : RegisterCliente(),
        'equipo': RegisterEquipo(),
        'certificados': RegisterCertificado(),
        'inspeccion': RegisterInspeccionNo()
    }
    if l_nuevo == "si":
        modalForm["inspeccion"] = RegisterInspeccionSi()

    if modalForm[elemento].validate_on_submit():
        table = TableValues(elemento)
        if l_nuevo == "si":
            message = table['registro'](modalForm[elemento], l_nuevo)
        else:    
            message = table['registro'](modalForm[elemento])

        flash(message['message'], message['type'])

        return redirect(url_for("buscador", elemento=elemento))

    return render_template(f"formularios/{elemento}.html", elemento=elemento, form=modalForm[elemento], l_nuevo=l_nuevo, object=None)


@app.route("/editar/<elemento>/<id>")
def editar(elemento, id):
    elemento = elemento.lower()
    table = TableValues(elemento)
    table_header = table['table_header']
    filter = {table_header[0] : id}
    object = table['model'].query.filter_by(**filter).first()

    role = object.role

    modalForm = {
        'laboratorista' : RegiseterLab(role=role),
        'clientes' : RegisterCliente(),
        'equipo': RegisterEquipo(),
        'certificados': RegisterCertificado(),
        'inspeccion': RegisterInspeccionNo()
    }


    return render_template(f"formularios/{elemento}.html", form=modalForm[elemento], object=object)



# Log Out
@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))


# Acciones de tabla

# ELIMINAR REGISTRO
@app.route("/eliminar/<elemento>/<value_id>")
@login_required
def eliminar(elemento,value_id):
    
    elemento = str(elemento).lower()
    table = TableValues(elemento)['model']
    result = table.query.get(value_id)
    db.session.delete(result)
    db.session.commit()
    flash(f"El concepto con ID: {value_id} fue eliminado ", 'warning')

    return redirect(url_for('buscador', elemento=elemento))

@app.route("/seleccionar/<elemento>/<value_id>")
@login_required 
def seleccionar(elemento,value_id):
    elemento = str(elemento).lower()
    tabla = TableValues(elemento)
    value = tabla['model'].query.get(value_id)
    print(value)
    return render_template(f"info_templates/{elemento}.html",
     value=value,
     table_header=tabla["table_header"])



''' -------------------------------------------------
wkhtmltopdf pdf creator
 -------------------------------------------------'''

@app.route("/api/createPDF/<elemento>/<value_id>")
@login_required
def creacion_certificado(elemento,value_id):
    table = TableValues(str(elemento).lower())
    kwargs = {table['table_header'][0]: value_id}
    value = table['model'].query.filter_by(**kwargs).one()
    template = render_template('pdf_templates/certificado.html', value=value)
    
    try:
        filename = str(uuid.uuid4()) + '.pdf'
        config = pdfkit.configuration(wkhtmltopdf=Download_FOLDER)
        pdfkit.from_string(template, filename, configuration=config)
        pdfDownload = open(filename, 'rb').read()
        os.remove(filename)
        return Response(
            pdfDownload,
            mimetype="application/pdf",
            headers={
                "Content-disposition": "attachment; filename=" + filename,
                "Content-type": "application/force-download"
            }
        )
    except ValueError:
        print("Oops! ")


# Ruta para editar el template de de los certificados para el pdf
# @app.route("/edicion-template/<value_id>")
# def edicion_template(value_id):
#     tabla = TableValues('certificados')

#     value = tabla['model'].query.get(value_id)

#     return render_template('pdf_templates/certificado.html', value=value)