.. _uploadlayers:

Upload a Layer
==============

1. Click the :guilabel:`Data` link on the Exchange toolbar, and select **Upload Layers** in the drop-down menu to open the Upload Layers page.

  .. figure:: img/data-menu.png

2. Click the :guilabel:`Choose Files` button. This will open a local file dialog. Navigate to your data folder and select the file(s) for the geospatial layer.

**Note:** Some file types require multiple files to create a complete layer. If you are uploading an ESRI Shapefile, be sure to include the .dbf, .prj, .shp, and .shx files.

  .. figure:: img/choose-files.png

3. Click on your file under **Manage Your Data**. Verify the file information is correct, and select **Create Layer**.

  .. figure:: img/manage-data.png

4. Verify the title of your layer is correct. A unique identifier will be added to the end of your layer. Select a Category from the drop-down menu. The category field is mandatory, and should best fit the type of data you are importing.

  Provide a brief abstract for your data. Other users will be able to find your data based on this text.

  Click the :guilabel:`Next Step` button when you are finished.

  .. figure:: img/summary-info.png

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

  .. figure:: img/time-attributes.png

  **Yes -** If your layer has an attribute for time configuration, and you’d like to enable the playback feature, select Yes. Configure the time attribute by selecting which data field is the Start Date. Selecting an end date is optional.

  .. figure:: img/time-config.png

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

    .. figure:: img/start-import.png

9. Click the :guilabel:`View Layer` button to make your layer visible to other users.

  .. figure:: img/import-complete.png

Selecting **View Layer** will take you to the layer’s information page, where you can create permissions for editing your data.