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

"""Script para actualizar la descripcion de ASSET 
 @Autor F286635
 @Version 1.0"""

logger = MXLoggerFactory.getLogger("maximo.gemalog")


try:
   userInfo = Security.getIntegrationUser()
   
   #Para probar uno.
   #mboSetAsset = MXServer.getMXServer().getMboSet("ASSET", userInfo)
   #mboSetAsset.setWhere("ASSETNUM = '265'")
   #mboSetAsset.reset()
   #mbo = mboSetAsset.getMbo(0)


   mboSetLocation = MXServer.getMXServer().getMboSet("LOCATIONS", userInfo)
   mboSetLocation.setWhere("location = '"+ mbo.getString("location")+"'")
   mboSetLocation.reset()
   mboLocation = mboSetLocation.getMbo(0)
   descripcion = mboLocation.getString("DESCRIPTION") +" / "+ mbo.getString("MANUFACTURER")
   if (mbo.getString("SERIALNUM")!=""):
      descripcion = descripcion +" / "+ mbo.getString("SERIALNUM")
   mbo.setValue("DESCRIPTION", descripcion)
   mbo.getThisMboSet().save()
   logger.error("Asset Modificado "+ mbo.getString("ASSETNUM")+"-"+mbo.getString("DESCRIPTION"))
  
except (MXException, MXApplicationException, RemoteException, Exception), e:
    logger.error("Error: Scrip actualizar la descripcion de Asset")
    logger.error(e)