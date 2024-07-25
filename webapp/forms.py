from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextAreaField, SelectField, FormField, RadioField
from datetime import datetime
from wtforms.fields.simple import SubmitField
from wtforms.form import Form
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms.fields.html5 import TelField, DateField
from webapp.models import *
from webapp.utils import *


class Login(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Log in')

    def validate_username(self,username):
        user = Laboratorista.query.filter_by(username=username.data).first()
        if user:
            if user.active == False:
                raise ValidationError("El usuario se encuentra inactivo")


class Buscar(FlaskForm):
    value = StringField('value')
    search = SubmitField('Buscar')


class RegisterFarinografo(Form):
    absorcion_agua = StringField('Absorcion de Agua')
    tolerancia_ub = StringField('Tolerancia')
    elasticidad = StringField('Elasticidad')
    viscodidad = StringField('Viscodidad')
    act_enzimatica = StringField('Enzimatica')
    trigo_germinado = StringField('Trigo Germinado')
    tiempo_amasado = StringField('Tiempo de Amasado')
    cantidad_gluten = StringField('Cantidad del Gluten')
    calidad_gluten = StringField('Calidad del Gluten')
    indoneidad = StringField('Indoneidad')
    dureza = StringField('Dureza')
    reblandecimiento = StringField('Reblancedimiento') 
    estabilidad = StringField('Estabilidad')
    tiempo_desarrollo = StringField('Tiempo de desarrollo') 
    qnumber = StringField('Qnumber')

class RegisterAlveografo(Form):
    tenacidad = StringField('Tenacidad')
    extensibilidad = StringField('Extensibilidad')
    fuerza_panadera = StringField('Fuerza Panadera')
    indice_elasticidad = StringField('Índice de Elasticidad')
    configuracion_curva = StringField('Configuración de la Curva')

class RegiseterLab(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', validators=[DataRequired()])
    active = BooleanField('Usuario activo') #! Boolean
    submit = SubmitField('Registrar')

    def validate_username(self,username):
        user = Laboratorista.query.filter_by(username=username.data).first()
        active_url = getFirstUrl()
        if user and active_url != "editar":
            raise ValidationError("Ese Usuario ya existe. Por Favor Selecciona otro")

    def __init__(self, * args, ** kwargs):
        super(RegiseterLab, self).__init__( * args, ** kwargs)
        self.role.choices = [('user', 'Usuario'),('admin', 'Administrador')]



class RegisterEquipo(FlaskForm):
    marca = StringField('Marca', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    serie = StringField('Serie', validators=[DataRequired()])
    proveedor = StringField('Proveedor', validators=[DataRequired()])
    fecha_adquisicion = DateField("Fecha de Adquisición", validators=[DataRequired()], default=datetime.now())
    garantia = DateField("Garantia", validators=[DataRequired()], default=datetime.today(), format='%Y-%m-%d')
    ubicacion = StringField('Ubicación', validators=[DataRequired()])
    mantenimiento = DateField("Mantenimiento", validators=[DataRequired()], default=datetime.now())
    descripcionc = StringField('Descripcion Corta', validators=[DataRequired()])
    descripcionl = TextAreaField('Descripcion Larga', validators=[DataRequired(),Length(max=100)])
    tipo = RadioField('Label', choices=[('alv','Alvegrafo'),('far','Farinografo')], validators=[DataRequired()])

    alveografo = FormField(RegisterAlveografo)
    farinografo = FormField(RegisterFarinografo)

    submit = SubmitField('Registrar')


    
class RegisterCliente(FlaskForm):
    rfc = StringField('RFC', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    domicilio = StringField('Domicilio', validators=[DataRequired()])
    ncontacto = TelField('Número de contacto', validators=[DataRequired()])
    personalizado_far = BooleanField('Farinografo Personalizado') #! Boolean
    personalizado_alv = BooleanField('Alveografo Personalizado') #! Booleanls

    alveografo = FormField(RegisterAlveografo)
    farinografo = FormField(RegisterFarinografo)

    submit = SubmitField('Registrar')


class RegisterOrden(FlaskForm):

    cantidad_solicitada = StringField('Cantidad Solicitada', validators=[DataRequired()])
    fecha_creada = DateField("Fecha Creada", validators=[DataRequired()], default=datetime.now())
    precio = StringField(' Precio', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class RegisterLote(Form):
    cantidad = StringField('Cantidad', validators=[DataRequired()])

class RegisterInspeccionNo(FlaskForm):
    loteSelect = SelectField("Lote")
    id_inspeccion = StringField("ID de Inspeccion", validators=[DataRequired()])
    equipo_alv = SelectField("Equipo Utilizado", validators=[DataRequired()])
    equipo_far = SelectField("Equipo Utilizado", validators=[DataRequired()])
    alveografo = FormField(RegisterAlveografo)
    farinografo = FormField(RegisterFarinografo)
    submit = SubmitField('Registrar')

    def __init__(self, * args, ** kwargs):
        super(RegisterInspeccionNo, self).__init__( * args, ** kwargs)
        self.equipo_alv.choices=[(table1.clave, table1.modelo) for table1 in EquipoLab.query.filter(EquipoLab.id_alv!="Null").all()]
        self.equipo_far.choices=[(table2.clave, table2.modelo) for table2 in EquipoLab.query.filter(EquipoLab.id_far!= "Null").all()]
        self.loteSelect.choices=[(table.idlote) for table in Lote.query.all()]



class RegisterInspeccionSi(FlaskForm):
    id_inspeccion = StringField("ID de Inspeccion", validators=[DataRequired()])
    loteForm = FormField(RegisterLote)
    equipo_alv = SelectField("Equipo Utilizado", choices=[(table1.clave, table1.modelo) for table1 in EquipoLab.query.filter(EquipoLab.id_alv!="Null").all()])
    equipo_far = SelectField("Equipo Utilizado", choices=[(table2.clave, table2.modelo) for table2 in EquipoLab.query.filter(EquipoLab.id_far!= "Null").all()])
    alveografo = FormField(RegisterAlveografo)
    farinografo = FormField(RegisterFarinografo)
    submit = SubmitField('Registrar')

    def __init__(self, * args, ** kwargs):
        super(RegisterInspeccionSi, self).__init__( * args, ** kwargs)
        self.equipo_alv.choices=[(table1.clave, table1.modelo) for table1 in EquipoLab.query.filter(EquipoLab.id_alv!="Null").all()]
        self.equipo_far.choices=[(table2.clave, table2.modelo) for table2 in EquipoLab.query.filter(EquipoLab.id_far!= "Null").all()]

class RegisterCertificado(FlaskForm):
    factura = IntegerField('Factura', validators=[DataRequired()])
    fecha_envio = DateField("Fecha de Envío", validators=[DataRequired()], default=datetime.now())
    fecha_caducidad = DateField("Fecha de Caducidad", validators=[DataRequired()], default=datetime.now())
    inspeccion = SelectField("Inspección")
    orden = SelectField("Numero de Orden")
    submit = SubmitField('Registrar')

    def __init__(self, * args, ** kwargs):
        super(RegisterCertificado, self).__init__( * args, ** kwargs)
        self.inspeccion.choices=[(table.idi, table.id_inspeccion) for table in Inspeccion.query.all()]
        self.orden.choices=[(table.norden, table.norden) for table in Orden.query.all()]

