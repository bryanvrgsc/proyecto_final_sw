from webapp.models import *

def TableValues(elemento):

    if elemento == "laboratorista":
        return {'uncalled': Laboratorista,'model' : Laboratorista(), 'search_item' : 'username', 'table_header' : Laboratorista.__table__.columns.keys(), 'breakpoint': None}
    elif elemento == "clientes":
        return {'uncalled': Cliente,'model' : Cliente(), 'search_item' : 'rfc', 'table_header' : Cliente.__table__.columns.keys() , 'breakpoint': 'personalizado_far'}
    elif elemento == "equipo":
        return {'uncalled': EquipoLab,'model' : EquipoLab(),'search_item' : 'clave', 'table_header' : EquipoLab.__table__.columns.keys() , 'breakpoint': 'descripcionl'}
    elif elemento == "certificados":
        return {'uncalled': Certificado,'model' : Certificado(), 'search_item' : 'ncertificado', 'table_header' : Certificado.__table__.columns.keys() , 'breakpoint': 'idl'}
    elif elemento == "inspeccion":
        return {'uncalled': Inspeccion,'model' : Inspeccion(),'search_item' : 'idi', 'table_header' : Inspeccion.__table__.columns.keys() , 'breakpoint': None}
    else:
        return {'error message' : 'Query Invalido', 'type':'alert'}


def universal(equipo):
    if equipo == "farinografo":
        class unidades():
            id_far = "Universal"
            absorcion_agua= '51.6–63.4 ml/100g'
            tolerancia_ub= '20 - 28 '
            elasticidad= '3.64 - 4.63 mm'
            viscodidad= '450-600 g/kg 80°C'
            act_enzimatica= 'Amilasas 30-35%'
            trigo_germinado= '60 - 75'
            tiempo_amasado= '4 - 7 min'
            cantidad_gluten= '12.5 - 13.5 %'
            calidad_gluten= '60- 90%'
            indoneidad= 'Levadura 20-25%'
            dureza= '54-145 FU'
            reblandecimiento= '0.651 - 0.9357 aw'
            estabilidad= '4.45–11.20 min'
            tiempo_desarrollo= '8.3 - 9.3 min'
            qnumber= '24 - 125'
                
    if equipo == "alveografo":
        class unidades():
            id_alv = "Universal"
            tenacidad= '45 mm'
            extensibilidad= '71.96 mm'
            fuerza_panadera= '60 mm'
            indice_elasticidad= '47 mm'
            configuracion_curva= '0.99 mm'
    
    return unidades