Introduction
============

`Apache Synapse <http://synapse.apache.org>`_ is a lightweight Enterprise Service Bus (ESB) that supports a wide range of communication protocols and messaging standards. It enables integrating heterogeneous systems in a simple and unified manner without requiring the system integrators to modify any of the existing applications or write custom adapters. Instead, the Synapse ESB is configured using a simple XML based metalanguage to define high-level APIs, services, endpoints and mediation flows to construct fully automated business processes and implement powerful Enterprise Integration Patterns (EIPs). 

Synapse provides comprehensive support for RESTful services as well as traditional SOAP/WS-* services. This allows developers to use Synapse as a gateway (proxy) for both SOAP and RESTful services. More specifically, Synapse can be used to provide a REST gateway for a collection of SOAP services. This is a particularly useful feature by which an existing SOAP service can be made available to a completely different group of consumers (e.g. RESTful mobile clients) without having to change any code related to the backend web service. In this tutorial we will look at how to use Apache Synapse as a REST gateway for a set of given SOAP services. We will look at how to define RESTful APIs in Synapse using its metalanguage and then map RESTful API calls into SOAP web service requests without compromising any features or semantics of the backend SOAP services.

This demonstration consists of 3 parts (available in 3 separate directories).
  * Backend SOAP service
  * Synapse ESB configuration
  * Sample client scripts

Read on to learn more about each of these components. 

Backend SOAP Service
--------------------
We are going to use a simple order management demo service as our backend SOAP service. It supports the following basic operations.
  * addOrder - Place a new order for a drink
  * getOrder - Get the details regarding an existing order
  * updateOrder - Update an existing order
  * deleteOrder - Delete/Cancel an existing order
  * getAllOrders - Get a list of all existing orders

The service has been implemented in Java using the `Apache Axis2 <http://axis.apache.org>`_ framework. Therefore it can be deployed in Axis2 or any Axis2 compatible service container. To build the deployable service artifact, go into the ``service/OrderManagementService`` directory and run the following `Maven <http://maven.apache.org>`_ command. ::

  mvn clean install

This will create a binary file named ``OrderManagementService.aar`` in the ``target`` directory which can be directory deployed.

Synapse ESB Configuration
-------------------------
As mentioned earlier, Apache Synapse is configured using a simple XML based metalanguage to receive, process and mediate service requests. In order to use Synapse as a gateway between REST clients and SOAP services, we need a set of Synapse configuration files that can process RESTful service requests by converting them into standard SOAP requests. In this demo application we configure Synapse to receive RESTful service requests and convert them into SOAP requests that can be sent to our backend order management service. SOAP responses from the backend service are converted back to the original REST style and sent back to the client. This way a RESTful client can interact with our SOAP based order management service using pure REST calls, without ever knowing that the backend is actually based on SOAP. Therefore the Synapse ESB acts as a transparent proxy between the REST client and the SOAP service in this case.

The set of Synapse configuration files for this demo can be found in the ``esb/synapse-config`` directory. These files can be directly deployed in Apache Synapse by copying them to the ``repository/conf/synapse-config`` directory of the Synapse installation. For the tutorial we will be using `WSO2 ESB <http://wso2.com/products/enterprise-service-bus/>`_, an open source ESB product that uses Synapse as its mediation engine. In that case these configuration files should be copied to the ``repository/deployment/server/synapse-configs/default`` directory of the ESB installation.

Sample Client Scripts
---------------------
In order to interact with this demo application, some RESTful client tool is necessary. A simple command line tool such as ``curl`` can be used for this purpose. In order to simplyfy the testing procedure, a set of sample Python scripts (based on httplib) are provided in the ``client`` directory. 

You may use any other REST client application to interact with this demo and try it out. If you are looking for a more UI oriented client tool, please check out the `Chrome Advanced REST Client <https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo?hl=en-US>`_.