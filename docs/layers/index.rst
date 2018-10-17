Working with Layers
===================

Uploading layers into Exchange provides better visualization of your data, and helps you create a more detailed map.

Exchange supports the following Vector formats:

* ESRI Shapefile
* CSV (Comma Separated Value)
* Google Earth KML
* GeoJSON

The following are the supported Raster formats:

* GeoTIFF
* NITF (National Imagery Transmission Format)

All file types listed can be uploaded as a Zip Archive (.zip).

Once the layers are uploaded, they will be available to other users in Exchange.

Upload a layer
-----------------

1. Click the :guilabel:`Data` link on the Exchange toolbar, and select **Upload Layers** in the drop-down menu to open the Upload Layers page.

    .. figure:: img/upload-layer.png

2. Click the :guilabel:`Choose Files` button. This will open a local file dialog. Navigate to your data folder and select the file(s) for the geospatial layer.

**Note:** Some file types require multiple files to create a complete layer. If you are uploading an ESRI Shapefile, be sure to include the .dbf, .prj, .shp, and .shx files.

    .. figure:: img/add-layer.png

3. Click on your file under **Manage Your Data**. Verify the file information is correct, and select **Create Layer**.

    .. figure:: img/manage-data.png

4. Verify the title of your layer is correct. A unique identifier will be added to the end of your layer. Select a Category from the drop-down menu. The category field is mandatory, and should best fit the type of data you are importing.

  .. figure:: img/summary-info.png
  
  Select a Default Style from the drop-down menu.

  If the layer upload includes one or more sld files, you can select one from the list; otherwise, the layer will be given a default style, which can be edited within the map.

  .. figure:: img/default-style.png

  Provide a brief description of your data. Other users will be able to find your data based on this text.

  Click **Continue** when you are finished.

Configure time attributes
^^^^^^^^^^^^^^^^^^^^^^^^^

A feature can currently support one or two time attributes. If a single attribute is used, the feature is considered relevant at that single point in time (start date). If two attributes are used, the second attribute represents the end of a valid time period for the feature.

A time attribute can be:

        * A date - 02/15/2016 11:23 AM
        * Text that can be converted to a timestamp - Wednesday December 7, 2016 9:47 AM
        * A number representing a year - 2016, 1978

You will select the attribute you want to use from the drop down list. Exchange can handle the following formats:

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

5. Select a time attribute option for your layer.

    .. figure:: img/time.png

    **Yes -** If your layer has an attribute for time configuration, and you’d like to enable the playback feature, select Yes. Configure the time attribute by selecting which data field is the Start Date. Selecting an end date is optional.

    .. figure:: img/configure-time.png

    **No -** Select No if your data does not include temporal information.

    Click the :guilabel:`Next Step` button.

Enable version control
^^^^^^^^^^^^^^^^^^^^^^

Exchange uses GeoGig repositories to maintain version control of your vector data. By enabling version history, you can see the history of changes and who made them. Please reference the **Editing and Version Management** section for further information. Establishing permissions for your layers allows you to see edits made to the information through version history. Please see the below section on **Setting Permissions** for more information.

**Note:** Attempting to enable version history for a raster file will cause an error, notifying you to verify your configuration before you can proceed with the import.

6. Select **Yes** or  **No**, followed by the :guilabel:`Next Step` button.

    .. figure:: img/version-control.png

Enable layer viewing
^^^^^^^^^^^^^^^^^^^^

Determine who is able to view your layer. Selecting :guilabel:`Everyone` allows all users to view the data. This does not establish editing permissions, which can be created later.

7. Click either the :guilabel:`Everyone` button or :guilabel:`Just Me`.

  .. figure:: img/view-layer.png

8. Review the configuration, and click the :guilabel:`Start Import` button to begin the import.

    .. figure:: img/review-config.png

9. Click the :guilabel:`View Layer` button to make your layer visible to other users.

  .. figure:: img/import-complete.png

Selecting **View Layer** will take you to the layer’s information page, where you can create permissions for editing your data.

Layer information
-----------------

Each layer has an information page associated to it, which has several options for managing the layer’s data. Information is available for the following:

  * Info – Displays general information about the layer
  * Attributes - Lists the features in a layer, and the nonspatial information about the feature
  * Ratings – Based on the ratings of other users
  * Comments – Any comments on the layer from users
  * Legend – Maps using this layer – What other maps within Exchange are using the layer
  * Permissions – How others can see or modify this layer
  * Styles – What styles are associated to the layer
  * About – Provides information on the owner, Point of Contact and Metadata Author
  * Maps using this layer – Indicates which maps are using this layer

1. To access Layer Information, click the :guilabel:`Data` link on the Exchange toolbar, and select **Layers** from the drop-down menu. This will open the Explore Layers page. Here you will see a list of all of the available layers. Each layer has a thumbnail image, as well as the title, author, and any associated keywords. If a style was associated to the layer during import, it will display in the legend.

2. Click the **View Details** link below the layer you want to access.

  .. figure:: img/view-details.png

The information page for the layer will open.

  .. figure:: img/details-page.png


Using the map features
^^^^^^^^^^^^^^^^^^^^^^

Within the layer details page, there are some map features that will help you view the layer more in depth.

**Zoom -** Select the Zoom In or Zoom Out button to zoom to a specific location. Depending on the basemap, you may be able to zoom in as close as 1:10 meters.

  .. figure:: img/zoom-in.png

  .. figure:: img/zoom-out.png

**Zoom to the Initial Extent -** Return to the original extent of the map.

  .. figure:: img/initial-extent.png

**Print Map -** Select Print Map to print a copy of the layer.

  .. figure:: img/print-map.png

**Layers -** Select the Layers button to turn any of your layers off or on.

  .. figure:: img/layers-details.png

3. Click the :guilabel:`Basemap` button in the lower left corner to select a different basemap style.

  .. figure:: img/basemap-bttn.png

Exchange comes with the mapnik openstreetmap by default. Contact your Exchange administrator for additional basemaps.

  .. figure:: img/basemaps.png

Layer detail tabs
^^^^^^^^^^^^^^^^^

There are five tabs with information pertaining to the particular layer: Info, Attributes, Ratings, Comments, and GeoGig.

The Info tab is the default display, and contains basic information about the layer, such as the title, who created it, and when it was published.

  .. figure:: img/info-tab.png

The Attributes tab displays the layer attribute table. Layer attribute statistics will only display if the value is a numeric attribute, otherwise, no statistics will be calculated.

  .. figure:: img/details-attributes.png

The Ratings tab displays all ratings given to a layer by other users. Click on a star to rate the layer (one to five stars). Click the **Cancel this rating** icon to delete your rating.

  .. figure:: img/details-ratings.png

The Comments tab allows you to see what others are saying about this layer, as well as leave your own comment. Click the :guilabel:`Add Comment` button to leave a comment about the layer. When you’ve finished, click the :guilabel:`Submit Comment` button.

  .. figure:: img/comments.png

The GeoGig tab shows you the history of edits that have been made to the layer, when they were made, and by whom.

  .. figure:: img/geogig.png

Editing metadata and managing layers
------------------------------------

Each layer’s information page allows you to view the information that makes up the layer. Exchange allows you to edit metadata pertaining to a layer that you have uploaded, as well as any layers you are given permissions to access by other users.

Edit metadata
^^^^^^^^^^^^^

Metadata is information about the layer, such as the owner, title, purpose or restrictions on a layer. You can include as much information about the layer as you feel is important; the more you can tell other users about your layer, the better. If you have questions about what to put in a field, hover your mouse over the area. An information balloon will explain what is required.

1. Click the :guilabel:`Edit Layer` button, and select the :guilabel:`Edit` button under Metadata. The Edit Metadata page will display.

  .. figure:: img/metadata-edit.png

2. Edit the information fields to include anything pertinent to the layer. **Note:** Once you begin to edit the metadata, the Category field becomes mandatory, and you must select at least one.

3. Click the :guilabel:`Update` button at either the top or bottom of the page to save your changes.

Create a custom thumbnail
^^^^^^^^^^^^^^^^^^^^^^^^^
Custom images related to your map can be created, and will display next to the map on the Explore Maps page.

1. From the layer’s info page, click the :guilabel:`Edit Layer` button.

  .. figure:: img/edit-layer.png

2. Click the :guilabel:`Set from file` button to browse to the image.

  .. figure:: img/thumbnail.png

3. Browse to the image you’d like to use. Once added, the new image will display.

Set permissions
^^^^^^^^^^^^^^^^^^^

The social design of Exchange allows users to coordinate on projects by sharing access to the same layers and maps; however there may be instances when you want to limit who has what access to your layers. In Exchange, you can establish permissions for who can view, edit, and manage layers. Permissions can also be set for editing styles and metadata.

By default, when a layer is uploaded, the permissions are set so that only the person who uploaded the layer has permission to make changes. If you want other people to edit the layer, its styles or metadata, you must change the permissions to allow it.

1. Click the :guilabel:`Change Layer Permissions` button.

  .. figure:: img/permissions.png

2. Under the **Who can view it** and **Who can download it** sections, add the name(s) of registered users or groups. This will ensure anonymous view access is disabled, and only those users specified are able to see your layers. You can also leave the checkbox checked to allow all users access to the layer.

  .. figure:: img/set-permission.png

3. You can make the same changes for who can edit, change metadata, styles and who can manage the data. Add the names of users or groups who have permission to edit the layer. Click the :guilabel:`Apply Changes` button when you are finished.

Replace a layer
^^^^^^^^^^^^^^^

Replacing a layer allows you to upload a new layer, taking the place of the current layer.

1. Click the :guilabel:`Edit Layer` button, and select the :guilabel:`Replace` button.

  .. figure:: img/layer-remove-replace.png

2. Follow the instructions to upload a new layer.

Remove a layer
^^^^^^^^^^^^^^

Removing a layer will delete it completely from Boundless Exchange.

1. Click the :guilabel:`Edit Layer` button, and select **Remove**.

2. Verify your selection by clicking the :guilabel:`Yes, I am sure` button.

  .. figure:: img/verify-remove-layer.png

Downloading data from a layer
-----------------------------

Within Exchange, there are two ways to extract data and metadata, download a layer or download a layer’s metadata. This facilitates the flow of geospatial data in (import) and out (export) of Exchange.

Download data
^^^^^^^^^^^^^

1. Click the :guilabel:`Download Layer` button.

2. Select the format in which you’d like the data to be downloaded. Exchange currently offers the following formats for use in multiple geospatial platforms:

  .. figure:: img/download-data.png

Select either data or images.

  .. figure:: img/download-images.png

3. Save the file to your computer when the Save As dialog box opens.

Download metadata
^^^^^^^^^^^^^^^^^

1. Click the :guilabel:`Download Metadata` button.

2. Select the format in which you’d like to download the metadata.

  .. figure:: img/download-metadata.png

3. Save the file to your computer when prompted.

View layer on the map
^^^^^^^^^^^^^^^^^^^^^

If a layer has been saved to a map, the names of the map(s) using the layer will be listed.

Click the :guilabel:`Create a Map` button to open the layer in the map viewer.

  .. figure:: img/maps-layer.png

You can also simply click the :guilabel:`Open in Map Viewer` button. The map will open, and the layer will be available in the layers list.

  .. figure:: img/mapviewer.png
