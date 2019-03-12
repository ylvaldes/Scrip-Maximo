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

"""Script para ejecutar el WF Preparacion de Tareas Programadas
Crea una OT de Preparacion de tareas y un objeto de UTD_PREPTAREA
Valida que la OT de Mantenimiento o las OT hijas no tenga una OT de Preparacion de Tarea
 @Autor F286635
 @Version 1.0"""

logger = MXLoggerFactory.getLogger("maximo.gemalog")

def otConPrepTarea(mbo):
    """ OT con Preparacion de Tareas 
    Parametros 
    mbo: OT de la cual queremos saber si tiene OT de preparacion de Tareas

    Retorna
    True: si la OT que pasas por paramentros tiene una OT de Preparacion de Tarea
    False: si la OT que pasas por paramentros no tiene una OT de Preparacion de Tarea 
    """
    try:
        userInfo = mbo.getUserInfo()
        otPrepTarea = MXServer.getMXServer().getMboSet("WORKORDER", userInfo)
        otPrepTarea.setWhere("origrecordid='"+ mbo.getString("wonum")+ "' and classstructureid in ( select cle.classstructureid from classstructure cle where cle.classificationid in ('TARPROG','TARNPROG')) and status <> 'CANCELADA'")
        otPrepTarea.reset();
        if not otPrepTarea.isEmpty():
            return True
        else:
            return False
    except (Exception), e:
        logger.error("Error: Scrip Preparacion de tareas Programadas: otPrepTrea")
        logger.error(e)

def otHijaConPrepTarea(mbo):
    """ OT con OTs Hijas que tengan OT de Preparacion de Tareas 
    Parametros 
    mbo: OT de la cual queremos saber si tiene OTs hijas con la OT de preparacion de Tareas
    
    Retorna
    True: si la OT que pasas por paramentros tiene una OT hija con la OT de Preparacion de Tarea
    False: si la OT que pasas por paramentros no tiene una OT hija con la OT de Preparacion de Tarea 
    """
    try:
        userInfo = mbo.getUserInfo()
        otPrepTarea = MXServer.getMXServer().getMboSet("WORKORDER", userInfo)
        otPrepTarea.setWhere("parent='" + mbo.getString("wonum") + "'")
        otPrepTarea.reset();
        currentOT= otPrepTarea.moveFirst()
        while currentOT:
            if otConPrepTarea(currentOT):
                return True
            currentOT= otPrepTarea.moveNext()
        otPrepTarea.close()
        return False
    except (Exception), e:
        logger.error("Error: Scrip Preparacion de tareas Programadas: otHijaConPrepTarea")
        logger.error(e)
        

try:
  userInfo = mbo.getUserInfo()
  centro = mbo.getString("UTD_CENTRO")
  ubicacion = mbo.getString("LOCATION")
  classid = MXServer.getMXServer().getMboSet("classstructure", userInfo)
  classid.setWhere("classificationid = 'TARPROG'")
  classid.reset()
  if not classid.isEmpty():
      idClass = classid.getMbo(0).getString("classstructureid")
  classid.close()
  if not otConPrepTarea(mbo):
      if not otHijaConPrepTarea(mbo):
          setOT = MXServer.getMXServer().getMboSet("WORKORDER", userInfo)
          newWO =  mbo.createWorkorder()
          idNewOT =  newWO.getString("wonum")
          setId =newWO.getString("siteid")
          setOT.setWhere("WONUM = '" + idNewOT  + "'")
          setOT.reset()
          if not setOT.isEmpty():
              newWO = setOT.getMbo(0)
              newWO.setValue("classstructureid", idClass )
              newWO.setValue("DESCRIPTION", "Preparaci\xf3n de tareas programadas")
              newWO.setValue("UTD_CENTRO", centro,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
              lista=newWO.getMboSet("UTD_PREPTAREA")
              aux=lista.add()
              aux.setValue("WONUM" , idNewOT )
              aux.setValue("UBICACION" , ubicacion )
              aux.setValue("siteid" , setId)
              lista.save()
              setOT.save()
              wfs =  MXServer.getMXServer().lookup("WORKFLOW")
              wfs.initiateWorkflow("U_P_TAREA", newWO)
          setOT.close()
      else:
          params=["Existe una OT Hija con OT de Preparaci\xf3n de Tareas"]
          errorkey = "UTD_GENERICException"
          errorgroup = "UTD_GENERICException"
          error = True
  else:
      params=["La OT ya tiene una OT de Preparaci\xf3n de Tareas"]
      errorkey = "UTD_GENERICException"
      errorgroup = "UTD_GENERICException"
      error = True
except (MXException, MXApplicationException, RemoteException, Exception), e:
    logger.error("Error: Scrip Preparaci\xf3n de tareas Programadas")
    logger.error(e.getMessage())
    params=["Ocurrio un error a la hora de procesar el Script Preparaci\xf3n de Tareas \n" + str(e.getMessage())]
    errorkey = "UTD_GENERICException"
    errorgroup = "UTD_GENERICException"
    error = True