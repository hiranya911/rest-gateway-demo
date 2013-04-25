REST Gateway Implementation
===========================
In this section we will look at how our REST-to-SOAP gateway is implemented. We will delve into the specifics of the Synapse configuration which makes the transformation of REST to SOAP and back possible.

Our gateway demo consists of 2 REST API configurations.
 * StarbucksOrderAPI - Handles placement, retrieval, updating and cancellation of individual orders
 * StarbucksOrderListAPI - Handles the retrieval of all pending orders

Order API (StarbucksOrderAPI)
-----------------------------
This API is anchored at the ``/order`` context. It consists of 2 resources, one to handle POST requests and another to handle GET, PUT and DELETE requests. ::

  <api context="/order" name="StarbucksOrderAPI">
    <resource methods="POST" url-mapping="/">
      ...
    </resource>
    <resource methods="GET PUT DELETE" uri-template="/{orderId}">
      ...
    </resource>
  </api>

According to this configuration, a POST request on the ``/order`` URL path would be handled by the first resource. Any GET, PUT or DELETE requests on the ``/order/{orderId}`` path would be handled by the second resource. The ``/{orderId}`` segment in the URL path is called a template variable, and the client should fill that part in when invoking this API. That is the actual URL path of the second resource should be something like ``/order/my-order-id`` where the string ``my-order-id`` fills in the ``orderId`` variable. Synapse makes it possible to access URI template variables through the Synapse configuration language. We will shortly see how we can use the ``orderId`` value sent by the client in our request processing logic. (Refer `RFC6570 <http://tools.ietf.org/html/rfc6570>`_ to learn more about URI templates)

The first resoruce accepts a simple XML document as its POST payload and transforms it into a SOAP placeOrder request which we can send to our backend order management service. This transformation is done using a ``payloadFactory`` mediator. ::

  <payloadFactory>
    <format>
	<ucsb:addOrder>
	  <ucsb:order>
	    <xsd:name>$1</xsd:name>
	    <xsd:additions>$2</xsd:additions>        
	  </ucsb:order>
	</ucsb:addOrder>
    </format>
    <args>
      <arg expression="//sb:drink" />
      <arg expression="//sb:additions" />
    </args>
  </payloadFactory>

The ``format`` section defines the structure of the the placeOrder SOAP request. It defines two variables ``$1`` and ``$2`` which needs to be filled by the values extracted from the original RESTful service request. The ``args`` section defines how to extract these values from the REST request using simple XPath expressions.

We do a similar back transformation from SOAP to REST in the out-sequence of the resource configuration. Also since the SOAP service always responds to the ESB with ``200 OK`` responses, we use a ``proeprty`` mediator to change it to ``201 Created``. ::

  <property name="HTTP_SC" scope="axis2" value="201" />

The second resource that handles GET, PUT and DELETE requests is conceptually similar to the first one but there is more mediation logic. We use a ``switch`` mediator to differentiate between HTTP methods and handle them using separate sequences. GET requests are transformed into SOAP getOrder requests, PUT requests are transformed into SOAP updateOrder requests and DELETE requests are transformed into SOAP deleteOrder requests. These SOAP requests require the order ID to be passed in, therefore we extract the order ID from the URI template defined in our resource. This is done by executing a built-in Synapse XPath extension named ``$ctx:uri.var.*``. ::

  <payloadFactory>
    <format>
      <ucsb:getOrder>
	<ucsb:orderId>$1</ucsb:orderId>
      </ucsb:getOrder>
    </format>
    <args>
      <arg expression="$ctx:uri.var.orderId" />
    </args>
  </payloadFactory>

In this case we use the XPath expression ``$ctx:uri.var.orderId`` to extract the value of the ``orderId`` template variable and put it in a getOrder SOAP request.

Order List API (StarbucksOrderListAPI)
--------------------------------------
This API is anchored at the ``/orders`` context and consists of a single resource that handles HTTP GET requests. ::

  <api name="StarbucksOrderListAPI" context="/orders">
    <resource methods="GET" faultSequence="StarbucksFault">
      ...
    </resource>
  </api>

One of the first things this resource does is extracting the value of the HTTP ``Accept`` header and storing it in a Synapse property variable. ::

  <property name="STARBUCKS_ACCEPT" expression="$trp:Accept" />

We use this value later in the out-sequence to serialize the output into a format preferred by the client (content negotiation). Once the required values have been extracted from the request, Synapse transforms the RESTful GET request into a SOAP getAllOrders request. ::

  <payloadFactory>
    <format>
      <ucsb:getAllOrders />
    </format>
  </payloadFactory>

In the out-sequence we run a ``switch`` mediator on the value we extracted from the ``Accept`` header of the request, and formats the message into the client preferred output format. ::

  <switch source="$ctx:STARBUCKS_ACCEPT">
    <case regex=".*atom.*">
      ...
    </case>
    <case regex=".*text/html.*">
      ...
    </case>
    <case regex=".*json.*">
      ...
    </case>
    <case regex=".*application/xml.*">
      ...
    </case>
    <default>
      ...
    </default>
  </switch>

Note that based on the value of the ``Accept`` header we can serialize the output in one of XML, JSON, HTML or Atom formats. If the ``Accept`` header is not specified or the client requests for a format that we don't support, we fall back to Atom. The exact transformations from SOAP to HTML and SOAP to Atom are performed using the ``xslt`` mediator. SOAP to JSON and SOAP to POX (XML) transformation are naturally supported by Synapse without any additional mediators.

Error Handling
--------------
Synapse supports a concept of fault sequences which provides try-catch semantics in the mediation engine. A special fault sequence can be registered with each message flow, service or API which gets triggered when an unexpected error condition occurs. One such error condition that may occur in our demo application is that the client invoking the StarbucksOrderAPI with an invalid order ID value. When this value is sent to the backend SOAP service it sends an error response. A special fault sequence has been defined in Synapse to handle this situation and respond to the user with a ``404 Not Found`` response. Another fault sequence catches all other unexpected runtime errors and responds to the user with a ``500 Internal Server Error`` response.