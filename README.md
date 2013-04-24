REST Gateway Demo
==================

Author: Hiranya Jayathilaka

This is a sample application that demonstrates using Apache Synapse (http://synapse.apache.org) as a
REST-to-SOAP gateway. This application relies on the REST API mediation support provided by Synapse
to receive RESTful service requests, transform them into SOAP web service requests and invoke a SOAP
backend service.

This application consists of 3 parts:
  1. Backend SOAP service (in service directory)
  2. Synapse ESB configurations (in esb directory)
  3. REST client scripts (in client directory)

Please refer the contents in the docs directory to learn more about each part and see how to assemble
the application into a single functional system.

