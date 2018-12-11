# was_esb_mng
Sample IBM WebSphere ESB management scripts created on 2014 - not sure if it still works :)

Note that the most important part of all is `base.py` and it provides following functions: `startApplication`, `stopApplication`, `redeployApp`, `restartApplication`, `rippleStart` and  `updateApp`.

The project has sub projects having two different approaches.

## embedded_config
It can be used to _generate_ management scripts _for the given environment_ (TEST, PROD etc.):

    ant -Denv=test

then, the generated scripts can be used to redeploy the services on IBM WebSphere ESB: 

    jython ~/esb/bin/redeploy_CoreServiceModule.py
    
    ...

    jython ~/esb/bin/redeploy_PortalServiceModule.py
    ...

    jython ~/esb/bin/ripplestart.py


## externalized_config
It can be used to manage the services deployed to IBM WebSphere ESB. Each environment (TEST, PROD etc.) has its own configuration file under `conf` directory:

    jython manage.py --conf <config file> --cmd <command>

Available commands: `redeployCoreServiceModuleApp`, `redeployPortalServiceModuleApp`, `rippleStart`, `printConfigItems`.

    jython ~/esb/bin/manage.py --conf ~/esb/conf/test.cfg --cmd redeployCoreServiceModuleApp

P.S.: `manage.py` can be executed either by standalone jython installation(the script name becomes `argv[0]` and `len(sys.argv)` becomes `5`) or wsadmin console of IBM WebSphere(the script name is not passed and `len(sys.argv)` becomes `4`).