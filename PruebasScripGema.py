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

try:
        logger = MXLoggerFactory.getLogger("maximo.gemalog")
        medidor=mbo.getString("METERNAME")
        valor =mbo.getString("MEASUREMENTVALUE").replace(",",".")
        prioridad=0
        logger.info("Medidor " + medidor+ " Valor "+valor)
        if medidor=="SIG_M":
            logger.info("SIG_M")
            if float(valor) <= 7.0:
                prioridad=1
            elif float(valor) > 7.0 and float(valor) <= 18.30:
                prioridad=2
            elif float(valor)>18.30 and float(valor) <= 26.0:
                prioridad=3
        elif medidor=="CAV1" or medidor=="CAV2" :
            logger.info("CAV1 or CAV2")
            if float(valor)>= 75 and float(valor) <= 100:
                prioridad=1
            elif float(valor) >= 40 and float(valor) < 75:
                prioridad=2
            elif float(valor) >= 10 and float(valor) < 40:
                prioridad=3
        elif medidor=="PUD1" or medidor=="PUD2":
            logger.info("PUD1 or PUD2")
            if float(valor)>= 80 and float(valor) <= 100:
                prioridad=1
            elif float(valor) >= 50 and float(valor) < 80:
                prioridad=2
            elif float(valor) >= 25 and float(valor) < 50:
                prioridad=3
        logger.info("Prioridad "+ str(prioridad))

except (Exception), e:
        logger.error("Error: Script crear ST: Prioridad de la ST")
        logger.error(e)