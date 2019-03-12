from psdi.server import MXServer
from java.util import Date
from psdi.mbo import MboSetRemote
from psdi.mbo import MboRemote
from ute.utils import Security
from psdi.app.location import LocationMeterRemote
from psdi.app.meter import DeployedMeterRemote
from psdi.app.meter import MeterInGroupRemote

try:
  userInfo = Security.getIntegrationUser()
  idLoc = mbo.getString("location")
  #logger.debug(mbo.getString("location"))

  metersInGroup = mbo.getMboSet("METERINGROUP")
  setToGrow = mbo.getMboSet("LOCATIONMETER")
  setToGrow.reset()
  meter = metersInGroup.getMbo(0)
  m=1
  while meter:
     newDM = setToGrow.add()
     newDM.setCurrentlyBeingAddedOnMeterGroupChange(True)
     newDM.meterInGroupToDeployedMeter(meter, True)
     newDM .save()
     setToGrow.save()
     meter = metersInGroup.getMbo(m)
     m+=1
except (MXException, MXApplicationException, RemoteException, Exception), e:
   logger.debug("UTD_UPDMETERLOC ERROR Ubicacion idLoc")
   logger.debug(e)