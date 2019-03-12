from psdi.server import MXServer
from java.util import Date
from psdi.mbo import MboSetRemote
from psdi.mbo import MboRemote
from ute.utils import Security


userInfo = Security.getIntegrationUser()
fechaHoy = MXServer.getMXServer().getDate()

originator = mbo.getString("ORIGRECORDID")
setOT = MXServer.getMXServer().getMboSet("WORKORDER", userInfo)
setOT.setWhere("WONUM = '" + originator  + "'")
setOT.reset()
if not setOT.isEmpty():
    newWO = setOT.getMbo(0)
    fechaHoy = MXServer.getMXServer().getDate()
    newWO.changeStatus("EN_PROG", fechaHoy,"En Progresos por el WF")
    setOT.save()
setOT.close()