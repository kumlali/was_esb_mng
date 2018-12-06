
def modifySCAImportHttpBinding(module, component, method, endpointURL):
  """
  Modifies endpointURL of either import HTTP binding or one of its 
  methods.

  HTTP binding is only changed if method parameter is None.
  """
  if method is None:
    method = component

  command = '[-moduleName %(module)s -import %(component)s -endpointURL <%(method)s>%(endpointURL)s</%(method)s>]' % locals()
  print 'Executing AdminTask.modifySCAImportHttpBinding(' + command + ')';
  AdminTask.modifySCAImportHttpBinding(command)


def modifySCAImportHttpBinding(binding):
  """
  Executes given import HTTP binding
  """
  print 'Executing AdminTask.modifySCAImportHttpBinding(' + binding + ')';
  AdminTask.modifySCAImportHttpBinding(binding)


def modifySCAImportWSBinding(module, component, endpointURL):
  """
  Modifies endpointURL of WS import binding
  """
  command = '[-moduleName %(module)s -import %(component)s -endpoint %(endpointURL)s]' % locals()
  print 'Executing AdminTask.modifySCAImportWSBinding(' + command + ')';
  AdminTask.modifySCAImportWSBinding(command)


def modifySCAImportWSBinding(binding):
  """
  Executes given import WS binding
  """
  print 'Executing AdminTask.modifySCAImportWSBinding(' + binding + ')';
  AdminTask.modifySCAImportWSBinding(binding)


def updateApp(appName, appPack):
  """
  Updates an application. appPack must include absolute path to ear
  file
  """
  print "Application [" + appName + "] is being reployed from [" + appPack + "]";
  print "Executing AdminApp.update(" + appName + ", \"app\", \"[-operation update -contents " + appPack + "]"
  AdminApp.update(appName, "app", "[-operation update -contents " + appPack + "]")


def stopApplication(appName, servers):
  """
  Stops an application on all the servers in given server list
  """
  for server in servers:
    appManager = AdminControl.queryNames("type=ApplicationManager,process=" + server + ",*")
    print "Application [" + appName + "] is being stopped on server [" + server + "]"
    print "Executing AdminControl.invoke(appManager, 'stopApplication', " + appName + ")"
    AdminControl.invoke(appManager, "stopApplication", appName)


def startApplication(appName, servers):
  """
  Starts an application on all the servers in given server list
  """
  for server in servers:
    appManager = AdminControl.queryNames("type=ApplicationManager,process=" + server + ",*")
    print "Application [" + appName + "] is being started on server [" + server + "]";
    print "Executing AdminControl.invoke(appManager, 'startApplication', " + appName + ")"
    AdminControl.invoke(appManager, "startApplication", appName)


def restartApplication(appName, servers):
   """
   Restarts an application on all the servers in given server list
   """
   # stop 
   for server in servers:
     appManager = AdminControl.queryNames("type=ApplicationManager,process=" + server + ",*")
     print "Application [" + appName + "] is being stopped on server [" + server + "]"
     print "Executing AdminControl.invoke(appManager, 'stopApplication', " + appName + ")"
     AdminControl.invoke(appManager, "stopApplication", appName)
   
   # start
   for server in servers:
     appManager = AdminControl.queryNames("type=ApplicationManager,process=" + server + ",*")
     print "Application [" + appName + "] is being started on server [" + server + "]";
     print "Executing AdminControl.invoke(appManager, 'startApplication', " + appName + ")"
     AdminControl.invoke(appManager, "startApplication", appName)


def modifySCAImportHttpBindings(httpBindings):
  for binding in httpBindings:
    modifySCAImportHttpBinding(binding)


def modifySCAImportWSBindings(wsBindings):
  for binding in wsBindings:
    modifySCAImportWSBinding(binding)


def saveConfig():
  print "Configuration is being saved"
  print "Executing AdminConfig.save()"
  AdminConfig.save()


def redeployApp(appName, appPack, httpBindings, wsBindings, servers):
  updateApp (appName, appPack)

  # Update HTTP bindings
  if httpBindings is not None:
    modifySCAImportHttpBindings(httpBindings)

  # Update WS bindings
  if wsBindings is not None:
    modifySCAImportWSBindings(wsBindings)

  # Save configuration and restart the application
  saveConfig()
  restartApplication(appName, servers)


def rippleStart(cluster):
  AdminConfig.save()
  cls = AdminControl.completeObjectName("type=Cluster,name=" + cluster + ",*")
  print "Cluster [" + cluster + "] is being ripple started"
  print "Executing AdminControl.invoke(cluster, 'rippleStart')"
  AdminControl.invoke(cluster, 'rippleStart')
