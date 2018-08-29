.. _createlayers:

Create a New Layer
==================

Creating a new, blank layer allows users the freedom to build a layer with the attribute data they need, and still be able to tailor the style to what they want. Exchange users can create new, blank layers, rather than be limited to data that must be uploaded. From there, a user can add points, lines or polygons as necessary. The layer can be styled as explained in the Styling Layers section.

Creating a new layer in Exchange allows users of the `Boundless Anywhere™ <https://connect.boundlessgeo.com/docs/anywhere/1.3.0/>`_ app to create a framework for their data, and use it to add features while out in the field.

Please email contact@boundlessgeo.com for more information on how to get Boundless Anywhere for mobile field data collection.

1. Click the **Data** link on the Exchange toolbar, and select **Create Layer** in the drop-down menu to open the Create an empty layer page.

  .. figure:: img/data-menu.png
  
2. Provide a name and title for the layer in the appropriate fields. The name and title do not need to be the same, but it may be best to at least have similar names to prevent confusion.

  .. figure:: img/create-layer.png
  
3. Select the geometry type for the layer from the pull-down menu.

Exchange users can create point, line or polygon layers. 

4. Click the :guilabel:`Add Attribute` button to add feature attributes to the layer. 

This is where information such as feature name, location, or date can be added. 

Attributes should be entered as:
  * String - A text attribute, which allows 255 characters of any type.
  
  * Integer - Typically an integer from integer from -1,999,999,999 to 1,999,999,999 
  
  * Float - An integer which also allows decimal places
  
  * Date - A date - 02/15/2016 11:23 AM
  
    * Text that can be converted to a timestamp - Wednesday December 7, 2016 9:47 AM
  
    * A number representing a year - 2016, 1978
  
Exchange will handle the following date formats:

The most common formatting flags are:
  * y - year
  * M - month
  * d - day of month
  * h - hour of the day (0 - 23)
  * k - hour of the day (1-24)
  * m - minute in an hour
  * s - seconds in a minute

Exchange will also handle date and optional time variants of ISO-8601. In terms of the formatting flags noted above, these are:

    yyyy-MM-dd'T'HH:mm:ss.SSS'Z'

    yyyy-MM-dd'T'HH:mm:sss'Z'

    yyyy-MM-dd'T'HH:mm:ss'Z'

    yyyy-MM-dd'T'HH:mm'Z'

    yyyy-MM-dd'T'HH'Z'

    yyyy-MM-dd

    yyyy-MM

    yyyy

**Note:** Single quotes represent a literal character.

To remove ambiguity, repeat a code to represent the maximum number of digits. For example, yyyy or MM instead of yy or M.

  .. figure:: img/add-attributes.png
  
Set permissions
^^^^^^^^^^^^^^^  
  
The social design of Exchange allows users to coordinate on projects by sharing access to the same layers and maps; however there may be instances when you want to limit who has what access to your layers. In Exchange, you can establish permissions for who can view, edit, and manage layers. Permissions can also be set for editing styles and metadata. 

By default, when a layer is uploaded, the permissions are set so that only the person who uploaded the layer has permission to make changes. If you want other people to edit the layer, its styles or metadata, you must change the permissions to allow it. 

5. Under the **Who can view** and **Who can download** sections, add the name(s) of registered users or groups. This will ensure anonymous view access is disabled, and only those users specified are able to see your layers. You can also leave the checkbox checked to allow all users access to the layer.

  .. figure:: img/permissions.png
  
6. You can make the same changes for who can edit, change metadata, styles and who can manage the data. Add the names of users or groups who have permission to edit the layer. 

7. Once you have added all of your necessary attributes, and have created permissions for the layer, click the Create button.

The map will open, and the layer will be available in the layer list.

