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

"""Script para actualizar el tipo de Asset segun el tipo guardado en la variable tipo
 @Autor F286635
 @Version 1.0"""

logger = MXLoggerFactory.getLogger("maximo.gemalog")


try:
  userInfo = mbo.getUserInfo()
  tipo = "ACT-GRUPO-GENERADOR";
  classid = MXServer.getMXServer().getMboSet("classstructure", userInfo)
  classid.setWhere("classificationid = '" + tipo + "'")
  classid.reset()
  if not classid.isEmpty():
      idClass = classid.getMbo(0).getString("classstructureid")
  classid.close()
  
  idAsset= mbo.getString("ASSETNUM")
  mbo.setValue("UTD_TIPO_ASSET", tipo)
  mbo.setValue("classstructureid", idClass)
  logger.error(idAsset)
  
except (MXException, MXApplicationException, RemoteException, Exception), e:
    logger.error("Error: Scrip actualizar el tipo de Asset")
    logger.error(e)
    params=["Ocurrio un error a la hora de procesar el Script actualizar el tipo de Asset \n" + str(e.getMessage())]
    errorkey = "UTD_GENERICException"
    errorgroup = "UTD_GENERICException"
    error = True