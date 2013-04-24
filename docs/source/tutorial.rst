REST Gateway Tutorial
=====================

Prerequisites
-------------
You will need following software tools to try out this tutorial. Simply download them from the specified URLs for now. The tutorial will guide you through the process of setting them up.

  * `WSO2 ESB 4.0.3 <http://wso2.com/products/enterprise-service-bus/>`_ or higher (You can also use Synapse 2.1.0 instead. But the tutorial only provides instructions for WSO2 ESB.)
  * `WSO2 Application Server 5.1.0 <http://wso2.com/products/application-server/>`_ or higher (You can use any Axis2 compatible application server here. But the tutorial only provides instructions for WSO2 Application Server.)

In addition to the above tools, your computer must be setup with the following infrastructure tools.

  * JDK 1.6 or higher (Oracle JDK recommended)
  * `Curl <http://curl.haxx.se>`_
  * `Apache Maven 3.0 <http://maven.apache.org>`_ or higher

The tutorial does not specify how to install these infrastructure software. Tutorial assumes that they are already installed and available for use.

Setting Up the Backend Server
-----------------------------

We are going to host our sample order management service in WSO2 Application Server. Therefore lets start by setting up the Application Server.

  * Simply extract the downloaded zip archive to install the WSO2 Application Server. ::

      unzip wso2as-5.1.0.zip

  * Go into the ``bin`` directory of the installation and execute the ``wso2server`` startup script to start the server.

      Unix/Linux: sh wso2server.sh
      Windows: wso2server.bat

  * Wait for the server to finish initialization. This could take a few seconds depending on how fast your machine is.

Now that the server is up and running, lets deploy the order management service in it.

  * Use Apache Maven to build the OrderManagementService.aar artifact. Simply go into to the ``server/OrderManagementService`` directory of this sample package and run the following command. This will create the required artifact in the ``server/OrderManagementService/target`` directory. ::

      mvn clean install

  * Launch your web browser and navigate to the WSO2 Application Server management console. This is available at ``https://localhost:9443/carbon``.

  * Sign in to the console using default administrator credentials. ::

      Username: admin
      Password: admin

  * You are now in the home page of the Application Server's management console.

      .. image:: as_home.png
         :width: 720
         :height: 450

  * Click on the ``Manage > Services > Add > AAR Service`` option in the main menu.

      .. image:: as_upload.png
         :width: 720
         :height: 450

  * Browse and select the OrderManagementService.aar file and click on ``Upload`` to upload the artifact. Service deployment will take a few seconds. Click/refresh the service listing page (under ``Manage > Services > List`` in the main menu) and you will see the OrderManagementService listed there. Feel free click on it and browse through the various options available. For instance you should be able to see the WSDLs of the service and even invoke it online using the `Try-It` tool built into the management console. The service endpoint will be ``http://localhost:9763/services/OrderManagementService``.

Setting Up the ESB
-------------------
Now we have our backend SOAP service up and running. So lets get started with the ESB (our REST gateway). 

* Extract the downloaded WSO2 ESB archive to install it. ::

    unzip wso2esb-4.0.3.zip

* Before we can start the server, we need to do some configuration changes. This is because by default WSO2 ESB is configured to use the same set of ports as WSO2 Application Server. Since we are starting both servers in the same machine, we need to change the ESB ports before we can actually start it. To do this go into the ``repository/conf`` directory of the ESB installation and open the ``carbon.xml`` file using a text editor. Scroll down to the ``Ports`` configuration section and change the ``Offset`` value to ``1``. This will increment all the port numbers used by the ESB by 1. ::

    <Ports>

        <!-- Ports offset. This entry will set the value of the ports defined below to
         the define value + Offset.
         e.g. Offset=2 and HTTPS port=9443 will set the effective HTTPS port to 9445
         -->
        <Offset>1</Offset>
        ...

* Now we need to deploy our REST gateway configuration into the ESB. Go the ``repository/deployment/server/synapse-configs/default`` directory of the ESB and delete everything already available in there (files as well as folders). Then copy the contents of the ``esb/synapse-config`` directory of this sample package into the ``default`` directory of the ESB. ::

    cd esb_home/repository/deployment/server/synapse-config/default
    rm -rf *
    cp -r /path/to/sample/esb/synapse-config/* .

* [Optional Step] It is also advisable to bind the ESB HTTP interface to a proper IP address, before starting the ESB. To do this open the ``repository/conf/axis2.xml`` file in a text editor and look for the HTTP ``transportReceiver`` configuration. Uncomment the ``bind-address`` parameter and set its value to the IP address of the machine. Or at least set it to the loop back address. ::

    <transportReceiver name="http" class="org.apache.synapse.transport.nhttp.HttpCoreNIOListener">
        <parameter name="port" locked="false">8280</parameter>
        <parameter name="non-blocking" locked="false">true</parameter>
        <parameter name="bind-address" locked="false">127.0.0.1</parameter>
        <!--parameter name="WSDLEPRPrefix" locked="false">https://apachehost:port/somepath</parameter-->
        <parameter name="httpGetProcessor" locked="false">org.wso2.carbon.transport.nhttp.api.NHttpGetProcessor</parameter>
        <!--<parameter name="priorityConfigFile" locked="false">location of priority configuration file</parameter>-->
    </transportReceiver>

* We are all set now. Head over to the ``bin`` directory of the ESB and start it up. ::

    Unix/Linux: sh wso2server.sh
    Windows: wso2server.bat

Running the REST Client
-----------------------
In this section we will look at how to run a REST client against our REST gateway and consume the backend SOAP service. For an explanation on how the gateway is configured please refer the REST Gateway Implementation section.