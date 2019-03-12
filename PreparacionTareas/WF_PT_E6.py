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

"""Script de validacion de datos en la Etapa 6 (Rev Preparacion Oficina) del WF Preparacion de Tareas
Cambia a estado EN PROGRESO la OT de Mantenimiento   
 @Autor F286635
 @Version 1.0"""

logger = MXLoggerFactory.getLogger("maximo.gemalog")
userInfo = Security.getIntegrationUser()
fechaHoy = MXServer.getMXServer().getDate()
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
        logger.error("Error:Script de validacion de datos en la Etapa 6 (Rev Preparacion Oficina) : titulo_atributo")
        logger.error(e)
try:
    userInfo = mbo.getUserInfo()
    campos=""
    faltaDatos=False
    idOT = mbo.getString("wonum")
    lista = mbo.getMboSet("UTD_PREPTAREA")

    if not lista.isEmpty():
        prepTarea = lista.getMbo(0)
        # Obtengo la OT de Mantenimiento
        originator = mbo.getString("ORIGRECORDID")
        setOT = MXServer.getMXServer().getMboSet("WORKORDER", userInfo)
        setOT.setWhere("WONUM = '" + originator  + "'")
        setOT.reset()
        if not setOT.isEmpty():
                newWO = setOT.getMbo(0)
        # Fecha de recibo validación de oficina
        if prepTarea.getString("FECRECIBO_VO")=="":
            campos +=titulo_atributo("FECRECIBO_VO","UTD_PREPTAREA")
            faltaDatos= True
        # Jefe de Trabajo
        #ot DE mANTENIMIENTO 
        if newWO.getString("SUPERVISOR")=="":
            campos +=titulo_atributo("SUPERVISOR","WORKORDER")
            faltaDatos= True
        if faltaDatos:
            params=["No puede avanzar. Falta completar los siguientes datos: "+ campos ]
            errorkey = "UTD_GENERICException"
            errorgroup = "UTD_GENERICException"
            error = True
        else:
            fechaHoy = MXServer.getMXServer().getDate()
            newWO.changeStatus("EN_PROG", fechaHoy,"Aprobada por el WF")
            setOT.save()
            setOT.close()

    else:
        logger.error("Error: Scrip WF_PT_E6 ")
        params=["No existe preparaci\xf3n de tareas"]
        errorkey = "UTD_GENERICException"
        errorgroup = "UTD_GENERICException"
        error = True 
            
except (MXException, MXApplicationException, RemoteException, Exception), e:
    logger.error("Error: Error: Scrip WF_PT_E6")
    logger.error(e)
    params=["Ocurrio un error a la hora de procesar el ScriptError: Scrip WF_PT_E6 \n" + str(e.getMessage())]
    errorkey = "UTD_GENERICException"
    errorgroup = "UTD_GENERICException"
    error = True