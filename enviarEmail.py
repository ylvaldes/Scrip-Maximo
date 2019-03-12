from psdi.server import MXServer
from psdi.util import MXException
from ute.utils import Security
from psdi.util import MXException
from psdi.util import MXApplicationException
from java.rmi import RemoteException
from java.lang import System

nuevalinea = System.getProperty("line.separator")
emailDestino =  "mrodriguezf@ute.local"
emailOrigen = "soporteGEMA@ute.local"
asunto= "asunto"
mensaje = "<b>prueba&oacute;</b>"
MXServer.sendEMail(emailDestino , emailOrigen, asunto,mensaje )
print "fin"