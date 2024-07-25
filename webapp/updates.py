from webapp.forms import *
from webapp import db, bcrypt
from flask_login import current_user
from webapp.utils import getObject
from flask import flash
from webapp.registros import regFarinografo, regAlveografo, regLote


def upOrden(form):
    # orden = Orden(cantidad_solicitada=form.cantidad_solicitada.data, fecha_creada=form.fecha_creada.data, precio=form.precio.data)
    # return orden
    pass

def upFarinografo(form, id, elemento):
    far = getObject(id, elemento)
    far.absorcion_agua=form.absorcion_agua.data
    far.tolerancia_ub=form.tolerancia_ub.data
    far.elasticidad=form.elasticidad.data
    far.viscodidad=form.viscodidad.data
    far.act_enzimatica=form.act_enzimatica.data
    far.trigo_germinado=form.trigo_germinado.data
    far.tiempo_amasado=form.tiempo_amasado.data
    far.cantidad_gluten=form.cantidad_gluten.data
    far.calidad_gluten=form.calidad_gluten.data
    far.indoneidad=form.indoneidad.data
    far.dureza=form.dureza.data
    far.reblandecimiento=form.reblandecimiento.data
    far.estabilidad=form.estabilidad.data
    far.tiempo_desarrollo=form.tiempo_desarrollo.data
    far.qnumber=form.qnumber.data
    return far


def upAlveografo(form, id, elemento):
    alv = getObject(id, elemento)
    
    alv.tenacidad=form.tenacidad.data
    alv.extensibilidad=form.extensibilidad.data
    alv.fuerza_panadera=form.fuerza_panadera.data
    alv.indice_elasticidad=form.indice_elasticidad.data
    alv.configuracion_curva=form.configuracion_curva.data
    return alv

def upLaboratorista(form, id, elemento):
    if form.password.name =="password":
        lab = getObject(id, elemento)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        lab.username=form.username.data
        lab.password=hashed_password
        lab.role=form.role.data
        lab.active=form.active.data

    try:
        db.session.add(lab)
        db.session.commit()
        return {"message": f"El usuario {lab.username} ha sido actualizado con exito" , "type": "success"}
    except:
        return {"message": f"Hubo un error con su peticion, intentelo mas tarde" , "type": "danger"}

def upEquipo(form, id, elemento):
    equipo = getObject(id, elemento)
    equipo.marca=form.marca.data
    equipo.modelo=form.modelo.data
    equipo.serie=form.serie.data
    equipo.proveedor=form.proveedor.data
    equipo.fecha_adquisicion=form.fecha_adquisicion.data
    equipo.garantia=form.garantia.data
    equipo.ubicacion=form.ubicacion.data
    equipo.mantenimiento=form.mantenimiento.data
    equipo.descripcionc=form.descripcionc.data
    equipo.descripcionl=form.descripcionl.data

    # revisar que tipo de equipo era antes del upadate
    if equipo.id_far == None:
        tipo = "alv"
    else:
        tipo = "far"

    if tipo == form.tipo.data:
        if tipo == "alv" :
            alveografo = regAlveografo(form.alveografo)
            db.session.add(alveografo)
            new_alv_id = str(getLastId(Alveografo).id_alv)
            equipo.id_alv = new_alv_id
        else:
            farinografo = regFarinografo(form.farinografo)
            db.session.add(farinografo)
            new_far_id =  str(getLastId(Farinografo).id_far)
            equipo.id_far = new_far_id
    else:
        if tipo == "alv" :
            print("crear far")
            farinografo = regFarinografo(form.farinografo)
            db.session.add(farinografo)
            new_far_id =  str(getLastId(Farinografo).id_far)
            equipo.id_far = new_far_id
            db.session.delete(equipo.alveografo)
        else:
            print("crear var")
            alveografo = regAlveografo(form.alveografo)
            db.session.add(alveografo)
            new_alv_id = str(getLastId(Alveografo).id_alv)
            equipo.id_alv = new_alv_id
            db.session.delete(equipo.farinografo)
            

    db.session.add(equipo)
    db.session.commit()
    return{"message": f"El equipo {equipo.marca} ha sido registrado con exito" , "type": "success"}


def upCliente(form, id, elemento):
    cliente = getObject(id, elemento)
    cliente.rfc=form.rfc.data
    cliente.nombre=form.nombre.data
    cliente.apellido=form.apellido.data
    cliente.domicilio=form.domicilio.data
    cliente.ncontacto=form.ncontacto.data
    if cliente.personalizado_alv == True and form.personalizado_alv.data == True:
        alveografo = regAlveografo(form.alveografo)
        db.session.add(alveografo)
        new_alv_id = str(getLastId(Alveografo).id_alv)
        cliente.id_alv = new_alv_id
    elif cliente.personalizado_alv == False and form.personalizado_alv.data == True:
        alveografo = regAlveografo(form.alveografo)
        db.session.add(alveografo)
        new_alv_id = str(getLastId(Alveografo).id_alv)
        cliente.id_alv = new_alv_id
    if cliente.personalizado_far == True and form.personalizado_far.data == True:
        farinografo = regFarinografo(form.farinografo)
        db.session.add(farinografo)
        new_far_id =  str(getLastId(Farinografo).id_far)
        cliente.id_far = new_far_id
    elif cliente.personalizado_far == False and form.personalizado_far.data == True:
        farinografo = regFarinografo(form.farinografo)
        db.session.add(farinografo)
        new_far_id =  str(getLastId(Farinografo).id_far)
        cliente.id_far = new_far_id
    cliente.personalizado_far=form.personalizado_far.data
    cliente.personalizado_alv=form.personalizado_alv.data
    db.session.add(cliente)
    db.session.commit()
    return{"message": f"{cliente.nombre} ha sido actualizado con exito" , "type": "success"}

def upLote(form, id, elemento):
    lote = getObject(id, elemento)
    lote.cantidad=form.cantidad.data
    return lote


def upInspeccion(form, id, elemento, l_nuevo):
    inspeccion = getObject(id,elemento)
    
    # # Registro de campos basicos en inspeccion
    inspeccion.id_inspeccion=form.id_inspeccion.data
    inspeccion.clave_alv=form.equipo_alv.data
    inspeccion.clave_far=form.equipo_far.data

    # creacion de alveofrafo y farinografo nuevo
    farinografo = regFarinografo(form.farinografo)
    db.session.add(farinografo)
    new_far_id =  str(getLastId(Farinografo).id_far)
    inspeccion.id_far = new_far_id

    alveografo = regAlveografo(form.alveografo)
    db.session.add(alveografo)
    new_alv_id = str(getLastId(Alveografo).id_alv)
    inspeccion.id_alv = new_alv_id

    if l_nuevo == "no":
        # Edicion de Lote
        inspeccion.idlote = form.loteSelect.data
    else:
        # Formulario: Se crea un nuevo lote y se adquire su id para agregarlo a la base
        lote = regLote(form.loteForm)
        new_lote_id = str(getLastId(Lote).idlote)
        inspeccion.idlote = new_lote_id
        

    db.session.add_all([alveografo,farinografo,inspeccion])
    print(db.session.dirty)
    db.session.commit()
    return{"message": f"{inspeccion.id_inspeccion} ha sido actualizada con exito" , "type": "success"}

def upCertificado(form, id, elemento):
    certificado = getObject(id, elemento)     
    certificado.factura=form.factura.data
    certificado.fecha_envio=form.fecha_envio.data
    certificado.fecha_caducidad=form.fecha_caducidad.data
    certificado.idi=form.inspeccion.data
    # certificado.idl=current_user.idl
    certificado.norden=form.orden.data
    db.session.add(certificado)
    db.session.commit()
    return {'message': f'El certificado con factura: {certificado.factura} ha sido actualizado', 'type': 'info'}



# Funcion que define que tabla se va a actualizar
def updateFunction(elemento):
    if elemento == "laboratorista":
        return {'update_function': upLaboratorista}
    elif elemento == "clientes":
        return {'update_function': upCliente}
    elif elemento == "equipo":
        return {'update_function': upEquipo}
    elif elemento == "certificados":
        return {'update_function': upCertificado}
    elif elemento == "inspeccion":
        return {'update_function': upInspeccion}
    else:
        return {'error message' : 'Query Invalido', 'type':'alert'}