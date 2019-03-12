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


"""Para crear SR a partir de la última medida de los Medidores
   MBO pasaso por Parametro es measurement
 @Autor F286635
 @Version 1.0"""

logger = MXLoggerFactory.getLogger("maximo.gemalog")

"""Obtener el centro dada la Gerencia de la Ubicacion"""
def obtenerCentro(location):
    try:
        d= {'MVDEO':631,'ESTE':302,'NORTE':202,'OESTE':402,'CENTRO':502}
        userInfo = mbo.getUserInfo()
        lochierarchy = MXServer.getMXServer().getMboSet("lochierarchy", userInfo)
        lochierarchy.setWhere("location='"+location+"' and systemid <> 'UTE'")
        lochierarchy.reset()
        gerencia=lochierarchy.getMbo(0).getString("systemid")
        return d.get(gerencia)
    except (Exception), e:
        logger.error("Error: Script crear ST: obtenerCentro")
        logger.error(e)

"""Obtener la Prioridad de la ST"""
def obtenerPrioridad(medidor,valor):
    try:
        prioridad=0
        logger.info("Medidor " + medidor+ " Valor "+valor)
        if medidor=="SIG_M":
            if float(valor) <= 7.0:
                prioridad=1
            elif float(valor) > 7.0 and float(valor) <= 18.30:
                prioridad=2
            elif float(valor)>18.30 and float(valor) <= 26.0:
                prioridad=3
        elif medidor=="CAV1" or medidor=="CAV2" :
            if float(valor)>= 75 and float(valor) <= 100:
                prioridad=1
            elif float(valor) >= 40 and float(valor) < 75:
                prioridad=2
            elif float(valor) >= 10 and float(valor) < 40:
                prioridad=3
        elif medidor=="PUD1" or medidor=="PUD2":
            if float(valor)>= 80 and float(valor) <= 100:
                prioridad=1
            elif float(valor) >= 50 and float(valor) < 80:
                prioridad=2
            elif float(valor) >= 25 and float(valor) < 50:
                prioridad=3
        return prioridad
    except (Exception), e:
        logger.error("Error: Script crear ST: Prioridad de la ST")
        logger.error(e)
"""Crear la ST"""
def crearSR(lisSR,idClas,centro,loca,prio):
    try:
        SR = lisSR.add()
        SR.setValue("UTD_ORIGEN", "MED")
        SR.setValue("CLASSSTRUCTUREID", idClas)
        SR.setValue("ORGID", "DISTRIB")
        SR.setValue("SITEID", "SITE_DIS")
        SR.setValue("REPORTEDPRIORITY", prio)
        SR.setValue("DESCRIPTION", "Poste analizado para reemplazar")
        SR.setValue("DESCRIPTION_LONGDESCRIPTION", "Poste analizado para reemplazar")
        SR.setValue("UTD_CENTRO", centro)
        SR.setValue("LOCATION", loca)
        SR.getThisMboSet().save()
        logger.info("Creo ST")

    except (Exception), e:
        logger.error("Error: Script crear ST: Craer la ST")
        logger.error(e)

try:
    logger.info("_____________________ Creando ST a partir de Medidores ___________________________________")
    localizacion= mbo.getString("location")
    medidor=mbo.getString("METERNAME")
    valor =mbo.getString("MEASUREMENTVALUE").replace(",",".")

    prioridad=str(obtenerPrioridad(medidor,valor))
    centroAux=str(obtenerCentro(localizacion))
    logger.info("Ubicacion " + localizacion +" Centro "+centroAux+" Prioridad nueva para la SR "+prioridad )
    userInfo = mbo.getUserInfo()
    listaClass = MXServer.getMXServer().getMboSet("CLASSSTRUCTURE", userInfo)
    listaClass.setWhere("CLASSIFICATIONID='GAMJ'")
    listaClass.reset()
    idClass = listaClass.getMbo(0).getString("CLASSSTRUCTUREID")

    listaSR = MXServer.getMXServer().getMboSet("SR", userInfo);
    listaSR.setWhere("UTD_ORIGEN='MED' and CLASSSTRUCTUREID='"+idClass+"' and LOCATION='"+localizacion+"'")
    listaSR.setOrderBy("REPORTEDPRIORITY desc")
    listaSR.reset()
    if not listaSR.isEmpty():
        SR= listaSR.getMbo(0)
        logger.info("Existe SR " + SR.getString("TICKETID")+ " con Prioridad "+SR.getString("REPORTEDPRIORITY"))
        if SR.getString("REPORTEDPRIORITY") < prioridad:
            crearSR(listaSR,idClass,centroAux,localizacion,prioridad)
        else:
            logger.info("Existe la SR con igual o menor prioridad ")
    else:
        if int(prioridad)!=0:
            logger.info("Crea SR por Primera vez")
            crearSR(listaSR,idClass,centroAux,localizacion,prioridad)
        else:
            logger.info("Valor de la prioridad nueva Incorrecto")
    logger.info("__________________________________________________________________________________________")

except (Exception), e:
        logger.error("Error: Script crear ST")
        logger.error(e)