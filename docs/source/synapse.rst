Getting Familiar with Apache Synapse
====================================
Apache Synapse is a lightweight Enterprise Service Bus (ESB) that caters a wide range of service integration and messaging requirements. Some of the fundamental capabilities of Synapse are;
 * Message logging
 * Message filtering
 * Content based routing
 * URL rewriting
 * Message transformation
 * Protocol switching
 * Load balancing and fail-over routing
 * Persistent messaging support
 * Message enriching 

With these basic features, Synapse enables the developers and system integrators to connect multiple heterogeneous systems and implement a wide range of enterprise integration patterns (EIPs). This is particularly useful in large enterprise settings, where a number of disparate systems must co-exist and work together in perfect synchronism to support complex business processes and workflows. 

What makes Synapse even more attractive is the fact that Synapse facilitates a zero-code approach for connecting systems. This implies that multiple systems can be connected via Synapse without having to write any custom adaptation code. Instead, Synapse only needs to be configured using a very high-level, XML-based metalanguage. The language is simple, intuitive and abstracts out all the wire-level and other implementation details of the message flows and systems being integrated. Therefore the configurations are easy to develop, highly reusable and easy to maintain over time. The backend systems can undergo architecture or implementation level changes without inducing any changes to the Synapse configuration.

Since the ESB acts as a hub that sits between several systems, it's crucial that the ESB does not introduce any unnecessary latencies to the message flows that go through it. Synapse really stands out from other similar ESB products with regard to this aspect. Benchmarking results have shown that Synapse and the ESB products based on Synapse are the among the fastest in the world, can handle thousands of concurrent connections and can handle enormous volumes of traffic at sub millisecond latencies. Some recent benchmark results involving Synapse can be found at `<http://wso2.org/library/articles/2013/01/esb-performance-65>`_.

Simple Proxy Services
---------------------
This section provides a quick tutorial aimed at giving a little taste of what Synapse really is and how to use it in practice.

 * Start by downloading the Apache Synapse `binary distribution <http://synapse.apache.org/download.html>`_. The latest stable release as of now is v2.1.0
 * Simply extract the downloaded archive to install the ESB. ::

     unzip synapse-2.1.0-bin.zip
     tar xvf synapse-2.1.0-bin.tar.gz

 * Synapse ships with a set of prepackaged sample configurations. Each sample is identified by a unique numeric identifier. For this tutorial we will be using `sample 150 <http://synapse.apache.org/userguide/samples/sample150.html>`_. To start ESB with this sample configuration simply run the following command from the ``bin`` directory of the Synapse installation. ::

     Unix/Linux: sh synapse.sh -sample 150
     Windows: synapse.bat -sample 150

 * Sample 150 consists of a simple proxy service configuration. Proxy services are used to intercept web service requests before they reach their actual target destinations and perform some additional processing (can perform both pre-processing and post-processing). The exact configuration used in sample 150 looks like this. ::

     <proxy name="StockQuoteProxy">
        <target>
            <endpoint>
                <address uri="http://localhost:9000/services/SimpleStockQuoteService"/>
            </endpoint>
            <outSequence>
                <send/>
            </outSequence>
        </target>
        <publishWSDL uri="file:repository/conf/sample/resources/proxy/sample_proxy_1.wsdl"/>
     </proxy>

  * This tells Synapse to expose a proxy service named ``StockQuoteProxy``. Any requests received by this service will be forwarded to the backend endpoint ``http://localhost:9000/services/SimpleStockQuoteService``. The responses coming back from the service will be sent back to the client as they are. Therefore this proxy service does not really perform any additional processing on the messages. It simply acts as a transparent pass-through pipe between the client and the server.

  * To try this out we should first start a sample backend service at ``http://localhost:9000/services/SimpleStockQuoteService``. Synapse ships with all the artifacts needed for this. Simply head over to the ``samples/axis2Server/src/SimpleStockQuoteService`` directory and invoke ANT. ::

      ant

  * This would build a mock web service named ``SimpleStockQuoteService`` and deploy it into a sample Axis2 server that ships with Synapse. To start this sample backend server, head over to ``samples/axis2Server`` and run the appropriate startup script. ::

      Unix/Linux: sh axis2server.sh
      Windows: axis2server.bat

  * Now you have a backend server running. To invoke the proxy service, head over to ``samples/axis2Client`` directory and run the following ANT command. ::

      ant stockquote -Daddurl=http://localhost:8280/services/StockQuoteProxy

  * This would invoke your proxy service, which in turns invokes the backend Axis2 service and gets you the desired response. You can also use a tool such as SOAP-UI to try out the proxy service.

  * Finally, launch your web browser and navigate to the URL ``http://localhost:8280/services/StockQuoteProxy?wsdl`` to see the WSDL exposed by Synapse for the proxy service we configured.

Messaging Model
---------------
Previous section gave a breif outline of what it takes to install and run simple integration scenarios using Synapse. This section provides more detailed information about how Synapse works and what the underlying messaging model looks like.

The smallest configurable unit in Synapse is known as a mediator. A mediator can be viewed as a black box that takes an input message, performs some processing on it and produces an output message. Synapse ships with a large number of built-in mediators that are designed to handle various tasks such as logging, XSLT transformation, database lookups and URL rewriting. Using the Synapse configuration language we can combine multiple mediators to form complex message flows (sequences). Multiple sequences can be further combined to form high-level services.

Therefore the task of configuring Synapse boils down to defining the required sequences and services. In the previous section we configured a proxy service. A proxy service typically consists of an in-sequence and an out-sequence. The in-sequence mediates all the requests received by the proxy service and the out-sequence mediates all the responses sent by the backend service. In sample 150 however we only have an out-sequence configured. But it also have a target endpoint configured. From this Synapse infers that the requests must be directly forwarded to the target endpoint without performing any processing on it. The single ``send`` mediator configured in the out-sequence instructs Synapse to simply pass the response along to the client that started the invocation. If we need to perform some additional processing on the requests in this proxy service, all we need to do is to define an in-sequence in the proxy service and specify the required set of mediators. In the out-sequence it is possible to add more mediators and add more processing capabilities to the response flow. It is even possible to forward the response of the backend service to a different service and thereby chaining multiple services together to construct complex workflows.

Synapse mediators provide a high-level abstraction which allows the developers to configure services without considering the actual application layer protocol and the message format used to send/receive messages. All the messages are converted to the SOAP format before they are injected into the Synapse mediation engine. Therefore the message flow designer can simply assume that all messages are SOAP messages and invoke mediators on them. Therefore Synapse provides a uniform model for dealing with all types of messages and protocols.

REST API Support
----------------
Starting from version 2.1.0, Apache Synapse has comprehensive support for exposing REST APIs on the ESB and mediating RESTful service requests. Our demo application relies primarily on this REST mediation support of Synapse. A REST API configured in Synapse is somewhat similar to a webapp deployed in a servlet container. Each API has a unique name and it is anchored at a specific URL context. Within the API we can define one or more resources. Each resource is equivalent to a proxy service, with their own in-sequences and out-sequences. Each resource can be configured to handle a particular URI template and/or HTTP method combination. Lets consider the following example API. ::

  <api name="StockQuoteAPI" context="/stockquote">
    <resource uri-template="/view/{symbol}" methods="GET">
      <inSequence>
        ...
      </inSequence>
      <outSequence>
       ...
      </outSequence>
    </resource>
    <resource url-pattern="/order/*" methods="POST">
      <inSequence>
         ...
      </inSequence>
    </resource>
  </api>

This API is anchored at the ``/stockquote`` context. Therefore it will handle any HTTP request whose request URL path starts with ``/stockquote``. Then the API defines 2 resources. One resource will handle GET requests to the path ``/stockquote/view/{symbol}`` and the other will handle POST requests to the path ``/stockquote/order/*``. Within each resource we can define in-sequences and out-sequences with any suitable mediator configuration to process the RESTful service requests. 

More Documentation and Samples
------------------------------
To learn more about Apache Synapse, please refer to the `official Synapse documentation <http://synapse.apache.org/index.html>`_. This includes a complete `catalog of samples <http://synapse.apache.org/userguide/samples.html>`_ that Synapse ships with and detailed instructions on how to try them out. More specifically there are samples on Synapse message flows, mediators, proxy services, protocol switching and a number of other interesting scenarios.

Configuration Language
----------------------
The configuration language specification for Synapse can be found at official `Synapse documentation <http://synapse.apache.org/userguide/config.html>`_. The language is simple, intuitive and XML-based. Therefore most services and message flows can be constructed for Synapse by manually editing XML. If graphical tooling support is required, `WSO2 Developer Studio <http://wso2.com/products/developer-studio/>`_ which is based on `Eclipse <http://www.eclipse.org>`_ can be used.

WSO2 ESB
--------
For this demonstration we will not be using vanilla Apache Synapse. Rather we will be using `WSO2 ESB <http://wso2.com/products/enterprise-service-bus/>`_ which is an open source ESB based on Synapse. WSO2 ESB uses Synapse as its mediation engine and hence supports all the features (and more) that Synapse does. The same XML-based metalanguage used to configure Synapse is used to configure WSO2 ESB as well. This means any valid Synapse configuration is also a WSO2 ESB configuration and vice versa. In addition to the set of features provided by Synapse, WSO2 ESB provides excellent UI support, powerful management capabilities and flexible tooling support.

The set of samples that ship with Synapse are also being shipped with WSO2 ESB. Please refer the `ESB documentation <http://docs.wso2.org/wiki/display/ESB460/Enterprise+Service+Bus+Documentation>`_ and `samples guide <http://docs.wso2.org/wiki/display/ESB460/Samples>`_ to see how to try them out.