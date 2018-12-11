import sys, ConfigParser

#This script must be executed within directory where base.py 
#is found. Otherwise sys.path.append("/path/to/base") must be 
#added before following line
from base import *


def loadConfig(filename):
  config = ConfigParser.ConfigParser()
  config.read(filename)

  # This is necessary to be able to set variables for use globally
  global cell, cluster, node1, node2, process1, process2, dataPowerUrl, coreUrl, portalUrl, ssoUrl, deployDir

  cell=config.get('WAS', 'cell')
  cluster=config.get('WAS', 'cluster')
  node1=config.get('WAS', 'node1')
  node2=config.get('WAS', 'node2')
  process1=config.get('WAS', 'process1')
  process2=config.get('WAS', 'process2')
  dataPowerUrl=config.get('Endpoints', 'dataPowerUrl')
  coreUrl=config.get('Endpoints', 'coreUrl')
  portalUrl=config.get('Endpoints', 'portalUrl')
  ssoUrl=config.get('Endpoints', 'ssoUrl')
  deployDir=config.get('Deployment', 'deployDir')

  print "Configuration file " + filename + " has been loaded."


def printConfigItems():
  print "cell: " + cell
  print "cluster: " + cluster
  print "node1: " + node1
  print "node2: " + node2
  print "process1: " + process1
  print "process2: " + process2
  print "dataPowerUrl: " + dataPowerUrl
  print "coreUrl: " + coreUrl
  print "portalUrl: " + portalUrl
  print "ssoUrl: " + ssoUrl
  print "deployDir: " + deployDir


def redeployCoreServiceModuleApp():
  # redeploy
  appName="CoreServiceModuleApp"
  appPack=deployDir + "/" + appName + ".ear"
  redeployApp(appName, appPack)

  # change endpoint urls
  module="CoreServiceModule"
  modifySCAImportHttpBinding(module, "Core", None, coreUrl + "/SoapHandler")
  modifySCAImportHttpBinding(module, "Core", "callCore", coreUrl + "/SoapHandler")
  modifySCAImportHttpBinding(module, "Dp", None, dataPowerUrl)
  modifySCAImportHttpBinding(module, "Dp", "callDpAmountDecreaseType", dataPowerUrl + "/AmountDecrease")
  modifySCAImportHttpBinding(module, "Dp", "callDpAmountIncreaseType", dataPowerUrl + "/AmountIncrease")
  modifySCAImportHttpBinding(module, "Dp", "callDpIssuerType", dataPowerUrl + "/Issuer")
  modifySCAImportWSBinding(module, "SsoWS", ssoUrl + "/ws/sso")

  saveConfig()

  restartApplication(appName, [process1, process2])


def redeployPortalServiceModuleApp():
  # redeploy
  appName="PortalServiceModuleApp"
  appPack=deployDir + "/" + appName + ".ear"
  redeployApp(appName, appPack)

  # change endpoint urls
  module="PortalServiceModule"
  modifySCAImportHttpBinding(module, "Core", None, coreUrl + "/SoapHandler")
  modifySCAImportHttpBinding(module, "Core", "callCore", coreUrl + "/SoapHandler")
  modifySCAImportWSBinding(module, "AnnouncementWS", portalUrl + "/ws/announcement")
  modifySCAImportWSBinding(module, "SecurityWS", portalUrl + "/ws/security")

  saveConfig()

  restartApplication(appName, [process1, process2])


def rippleStart():
  rippleStart(cluster)


# ---------------------------------------------------
# Script starts from here
# ---------------------------------------------------
cell=cluster=node1=node2=process1=process2=dataPowerUrl=coreUrl=portalUrl=ssoUrl=deployDir=""

usage = "\nUsage: jython manage.py --conf <config file> --cmd <command>\n\nAvailable commands: redeployCoreServiceModuleApp, redeployPortalServiceModuleApp, rippleStart, printConfigItems"

# if the script is ran by standalone jython installation, script name
# becomes argv[0] and len(sys.argv) becomes 5. On the other hand,
# when the script is ran by wsadmin console of IBM WebSphere, the script name
# is not passed and len(sys.argv) becomes 4.
if len(sys.argv) != 4:  # the program name and the four arguments
  # stop the program and print an error message
  sys.exit(usage)

option1=sys.argv[0]
arg=sys.argv[1]
option2=sys.argv[2]
cmd=sys.argv[3]
if option1 != "--conf" or option2 != "--cmd":
   print usage
   sys.exit(2)

loadConfig(arg) 
printConfigItems()

# do what cmd says
if cmd == "redeployCoreServiceModuleApp":
   redeployCoreServiceModuleApp()
elif cmd == "redeployPortalServiceModuleApp":
   redeployPortalServiceModuleApp()
elif cmd == "rippleStart":
   rippleStart()
elif cmd == "printConfigItems":
   printConfigItems()
else:
   print usage
   sys.exit(2)
