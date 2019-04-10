from psdi.server import MXServer
from java.util import Date
from psdi.mbo import MboSetRemote
from psdi.mbo import MboRemote
from ute.utils import Security
from psdi.app.location import LocationMeterRemote
from psdi.app.meter import DeployedMeterRemote
from psdi.app.meter import MeterInGroupRemote


userInfo = Security.getIntegrationUser()

mboL= MXServer.getMXServer().getMboSet("locations", userInfo)
mboL.setWhere("location = '104671491'")
mboL.reset()
mbo = mboL.getMbo(0)     

metersInGroup = mbo.getMboSet("METERINGROUP")
metersInGroup.setWhere("METERNAME = 'FE_RETRA' or METERNAME = 'FE_IMPRE' or METERNAME = 'SIG_M' ")
metersInGroup.reset()
setToGrow = mbo.getMboSet("LOCATIONMETER")
meter = metersInGroup.getMbo(0)
m=1
while meter:
   newDM = setToGrow.add()
   newDM.setCurrentlyBeingAddedOnMeterGroupChange(True)
   newDM.meterInGroupToDeployedMeter(meter, True)
   meter = metersInGroup.getMbo(m)
   m+=1
setToGrow.save()
setToGrow.close()
metersInGroup.close()