SSL and PKI Administration
==========================

When registering a new remote service, some sites may require you to register a PKI certificate. To obtain the certificate, contact the authorizing authority at the location to have it sent (this can be done by the user, or by the system administrator). Your system administrator will then need to add it to the PKI directory specified in the PKI_DIRECTORY variable in the .env file. Once the certificate is added, it can be configured for use within Exchange.

Add SSL Configuration
^^^^^^^^^^^^^^^^^^^^^

If a remote service requires authentication with PKI, and Exchange admin user will need to add an SSL configuration. This is to configure the PKI itself. Then, the user can register the remote service.

  .. figure:: img/ssl-pki.png
  
  
1. Click the **Add** link next to SSL Configs on the Django Administration site SSL/PKI menu to open the Add SSL Config page.

2. Provide a name for the configuration in the Name textbox. This  Add a brief description of the certificate or configuration for the user (optional).

Exchange accepts either a combined (concatenated) cert file, or a combination of a certificate file and a cert private key file. The type of PEM file you select from the options below, depends on the type of file sent by the site you’re trying to access. These files are added to the PKI directory, and will be available in the drop-down menus. 

3. For a concatenated certificate, use this option. From the Custom CA cert file drop-down menu, select the certificate to be configured.

  .. figure:: img/custom-ca.png

4. Check the box if you want to allow invalid CAs during the pre-validation of SSL components.

If a certificate is no longer valid, or has expired, the system administrator will receive a warning when trying to save the form. It is up to the discretion of the system administrator whether or not they will accept invalid certificates. When checked, the admin is warned about invalid certs. When unchecked, invalid certs cause the form to have an error.

  .. figure:: img/invalid-ca.png

5. Select the client certificate file and the private key file from the drop-down menu. Enter the client cert password, if required.

  .. figure:: img/client-cert.png
  
6. The default setting for the SSL peer verify mode is CERT REQUIRED. It is recommended that you do not change this setting.

  .. figure:: img/ssl-cert.png
  
7. Select the :guilabel:`Save` button when you are finished. Verify the SSL has been configured by clicking the **SSL Configs** link on the Django Administration site SSL/PKI menu. All SSL configurations will be listed.

Add a hostname
^^^^^^^^^^^^^^

Once the SSL had been configured, the hostname can be mapped to make all available services accessible by the remote service endpoints.

  .. figure:: img/ssl-pki.png
  
1. Click the **Add** link next to Hostname on the Django Administration site SSL/PKI menu to open the Add SSL Config page.

2. Select the checkbox to ensure mapping is **Enabled**.  

3. Provide the hostname, and port if required, for the service you are configuring.

  .. figure:: img/hostname-port.png
  
**Note:** The hostname must be in all lowercase. The * wildcard is acceptable, but should only be used when necessary. It will try to match anything before it, if included before the hostname, or after, if included at the end of it.

4. Select the SSL configuration for this hostname from the **Ssl config** drop-down menu.

5. Check the **Proxy** box if you want the client’s browser connections to be proxied through this application.

  .. figure:: img/proxy.png

6. Click the :guilabel:`Save` button to save the configuration. You will be directed to the list of mapped hostnames, and notified that the configuration was changed successfully.

  .. figure:: img/change-ssl-config.png

  Any new patterns are added to the bottom of the list, however they are matched from top to bottom. This matching applies for all enabled services only. This means that in a list of hostnames (and optionally ports) that looks like the following:

  1. my.first.domain - Enabled
  2. my.second.domain - Enabled
  3. \*.domain\ - Enabled

  Any requests for "my.first.domain" will map to the settings present in first entry, even though they also match the third entry in the list. However, in a list like this:

  1. my.first.domain - Disabled
  2. my.second.domain - Enabled
  3. \*.domain\ - Enabled

  Any requests for "my.first.domain" will map to the settings present in third entry. This means that a wildcard mapping like ( * ) should be used sparingly and as low down on the list as possible.

  Use the Move arrows to move the matchings to the preferred order of precedence. Once the hostnames are configured, and in the desired match order, the user should be able to register the remote services without issue.

