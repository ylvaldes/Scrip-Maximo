from psdi.server import MXServer
from psdi.security import UserInfo
from java.util import Date
from psdi.mbo import MboSetRemote
from psdi.mbo import MboRemote
from ute.utils import Security
from psdi.mbo import MboConstants
from java.lang import String
from psdi.workflow import  WorkFlowServiceRemote
from psdi.util import MXException
from psdi.util import MXApplicationException
from psdi.util.logging import MXLogger
from psdi.util.logging import MXLoggerFactory
from java.rmi import RemoteException
import sys

"""Script de validacion de datos en la Etapa 2 (Preparacion de tareas no Programadas) del WF Preparacion de Tareas No programadas  
 @Autor F286635
 @Version 1.0"""

logger = MXLoggerFactory.getLogger("maximo.gemalog")
sys.setdefaultencoding('utf-8')

def titulo_atributo(atributo, objeto):
    """ Retorna el titulo del atributo pasado por parametro 
    Parametros 
    objeto: objeto en el que se encuentra el atributo
    atributo: atributo al cual le queremos identificar el titulo

    Retorna
    El titulo del atributo
    """
    try:
        userInfo = mbo.getUserInfo()
        maxAtribute = MXServer.getMXServer().getMboSet("maxattribute", userInfo)
        maxAtribute.setWhere("attributename = '"+ atributo +"' and objectname = '"+ objeto +"'")
        maxAtribute.reset()
        l_MaxAtribute = maxAtribute.getMbo(0).getMboSet("ML_TITLE")
        l_MaxAtribute.setWhere("LANGCODE='ES'")
        l_MaxAtribute.reset()
        if not l_MaxAtribute.isEmpty():
            title = l_MaxAtribute.getMbo(0)
            titulo=title.getString("TITLE") + "\n"
            return titulo
        else:
            return atributo + "\n"
    except (Exception), e:
        logger.error("Error: Script de validación de datos en la Etapa 2 (Preparacion de tareas no Programadas): titulo_atributo")
        logger.error(e)
try:
    userInfo = mbo.getUserInfo()
    campos=""
    faltaDatos=False
    idOT = mbo.getString("wonum")
    lista = mbo.getMboSet("UTD_PREPTAREA")

    """Datos para pasar la OT a Ejecutada """
    fechaHoy = MXServer.getMXServer().getDate()
    originator = mbo.getString("ORIGRECORDID")
    setOT = MXServer.getMXServer().getMboSet("WORKORDER", userInfo)
    setOT.setWhere("WONUM = '" + originator  + "'")
    setOT.reset()

    if not lista.isEmpty():
        prepTarea = lista.getMbo(0)
        # Nombre de quien designa la tarea
        if prepTarea.getString("DESIGNATAR")=="":
            campos +=titulo_atributo("DESIGNATAR","UTD_PREPTAREA")
            faltaDatos= True
        # Ubicacion 
        if prepTarea.getString("UBICACION")=="":
            campos +=titulo_atributo("UBICACION","UTD_PREPTAREA")
            faltaDatos= True
        # FEC_PCTNP
        if prepTarea.getString("FEC_PCTNP")=="":
            campos +=titulo_atributo("FEC_PCTNP","UTD_PREPTAREA")
            faltaDatos= True
        # Nivel de tension 
        if prepTarea.getString("NIVELTENS_PCTNP")=="":
            campos +=titulo_atributo("NIVELTENS_PCTNP","UTD_PREPTAREA")
            faltaDatos= True
        # Descripcion de la Tarea
        if prepTarea.getString("DESCRIP_PCTNP")=="":
            campos +=titulo_atributo("DESCRIP_PCTNP","UTD_PREPTAREA")
            faltaDatos= True
        # Jefe de Trabajo
        if mbo.getString("SUPERVISOR")=="":
            campos +=titulo_atributo("SUPERVISOR","WORKORDER")
            faltaDatos= True
        if faltaDatos:
            params=["No puede avanzar. Falta completar los siguientes datos: \n"+ campos ]
            errorkey = "UTD_GENERICException"
            errorgroup = "UTD_GENERICException"
            error = True    
        else:
            if not setOT.isEmpty():
                newWO = setOT.getMbo(0)
                fechaHoy = MXServer.getMXServer().getDate()
                newWO.changeStatus("EJECUTADA", fechaHoy,"Ejecutada por el WF")
                setOT.save()
            setOT.close()

    else:
        logger.error("Error: Scrip WF_PTNP_E2 ")
        params=["No existe preparaci\xf3n de tareas"]
        errorkey = "UTD_GENERICException"
        errorgroup = "UTD_GENERICException"
        error = True 
            
except (MXException, MXApplicationException, RemoteException, Exception), e:
    logger.error("Error: Error: Scrip WF_PTNP_E2")
    logger.error(e)
    params=["Ocurrio un error a la hora de procesar el ScriptError: Scrip WF_PTNP_E2 \n" + str(e.getMessage())]
    errorkey = "UTD_GENERICException"
    errorgroup = "UTD_GENERICException"
    error = True