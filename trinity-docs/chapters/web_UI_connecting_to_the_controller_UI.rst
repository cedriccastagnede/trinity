
.. vim: si:et:ts=4:sw=4:tw=100

.. This is an rST document. See Python Docutils for more details on the format and how to process:
.. http://docutils.sourceforge.net/

.. It may include Sphinx extensions. See the Sphinx website for more information:
.. http://www.sphinx-doc.org/

.. Text width is 100 characters with hard wraps, set your terminal / editor accordingly.


:Title:         Web UI: Connecting to the controller UI
:Author:        jf.lefillatre
:Last update:   2016/04/01


.. TODO
    Udate for HA controller pairs, which have different names (controller-1, -2)



Connecting to the controller UI
===============================

.. note::
    The exact setup of your system depends on how it was installed. The following instructions may
    need to be adapted to your specific hostnames, network ranges, etc.

Most of the configuration of a running Trinity system can be done through the integrated Web user
interface, or Web UI. This interface is available on the **controller** of the cluster, or on the
first controller of an HA controller pair.

There are multiple ways to connect to the Web UI. Most of the time you will reach it with `Direct
access`_ over the network, but it is also possible over a `Local console access`_.



Local console access
--------------------

The Web UI can be reached directly from the console of the controller node. The console can be
accessed in many ways, amongst which are:

- a keyboard, mouse and screen (directly or through a KVM);
- console redirection through the node's BMC;
- an SSH connection from a UNIX machine with X redirection (`ssh -X`).

Once logged in, a web browser pointing to `localhost` will display the Web UI: ::
    
    [controller]# firefox http://localhost



Direct access
-------------

.. versionadded:: R8
    Prior to R8, the only hostname allowed for accessing the Web UI was `localhost`, and by default
    the Web UI could only be reached through `Local console access`_. Starting with R8, the default
    hostnames of `controller` and `controller.cluster` were added to the list.
    See `Adding hostname aliases`_ for allowing access using alternative server names.

It is also possible to reach the Web UI over the network interfaces of the controller node. By
default the hostname of the controller is `controller`, and it is part of a domain called `cluster`.
With the hostname pointing to the correct IP address through the client's name resolution mechanism,
clicking on any of those links will connect to the Web UI:

`http://controller <http://controller>`_

`http://controller.cluster <http://controller.cluster>`_

If you would like to access the controller under a different hostname or domain name, please see
`Adding hostname aliases`_.



Adding hostname aliases
-----------------------

.. warning::
    The hostname of the controller is hardcoded in the configuration of Trinity. Although you may
    want to change the controller's public name, do not change the hostname itself. Instead, add
    whichever name you want for this machine in your DNS service, and follow the procedure below.

For security reasons the web framework used by Trinity limits the hostnames and domain names that
it serves (see `the original documentation of the Django project
<https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts>`_ for more details). Because of
that the framework will reject any connection attempt for which the hostname isn't in its whitelist.

To access the Web UI on the controller using a different hostname, follow those steps:

#. add the new hostname alias for the controller in your name resolution infrastructure (hostfile,
   DNS, NIS, LDAP, etc);

#. get `Local console access`_ to the controller node;

#. in the framework configuration file, add the new hostname alias, in that case `mynewname`: ::

    [controller]# grep ALLOWED_HOSTS /trinity/horizon/rootimg/etc/openstack-dashboard/local_settings 
    ALLOWED_HOSTS = ['localhost', 'controller', 'controller.cluster']
    
    [controller]# vim /trinity/horizon/rootimg/etc/openstack-dashboard/local_settings
    
    [controller]# grep ALLOWED_HOSTS /trinity/horizon/rootimg/etc/openstack-dashboard/local_settings 
    ALLOWED_HOSTS = ['localhost', 'controller', 'controller.cluster', 'mynewname']


#. restart the web framework to take the changes into account: ::
    
    [controller]# systemctl restart httpd

You should now be able to access the Web UI using the new hostname alias.

