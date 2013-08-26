Managing the site
=================

Managing the site is easy due to the use of Fabric for system administration tasks. We have written all
the code to deal with starting, editing, and stopping the server. The :file:`hosts_data.json` file must
be filled with all the data you set from the :doc:`../getting_started/installing` for the following commands
to work.

.. warning::
   These commands will only affect the gunicorn server and **not** the nginx server. You have to manually 
   start and stop the nginx, though that should not be necessary for this application as nginx only acts
   as a proxy.

Starting the site
-----------------

Run the following command on your local machine in the source code directory (the one with the 
:file:`hosts_data.json`) file in it::

   fab server_start

This will start off the gunicorn server remotely.

Stopping the site
-----------------

Run the following command to stop the site::
   
   fab server_stop

Restarting the site
-------------------

Run the following command to restart the site::

   fab server_restart

Updating the configuration
--------------------------

If you need to update any of the settings in the :file:`hosts_data.json` file, run the following two commands
to upload any changes and restart the server::

   fab create_local_settings
   fab server_restart

Updating the site
-----------------

To update the site to a newer version from github, run the command below. This will update the source code
and migrate your database with any changes. It will also stop the server while it is updating, so wait for the 
command to finish before attempting to visit the site::
   
   fab update_deploy

