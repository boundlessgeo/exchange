Osgeo_Importer
==============

The primary use of the Osgeo_Importer section is to help Exchange admin users manage data, files and layers imported through the web user interface. This section will cover how to view and delete existing uploaded files. All of the options in this section are available through the Osgeo_Importer section on the Django Site administration page.

View Uploaded data
^^^^^^^^^^^^^^^^^^

1. Click the **Upload data** link under the Osgeo_Importer menu on the Django Administration site Osgeo-Importer menu.

  .. figure:: img/osgeo-menu.png

Data that has been uploaded into Exchange will be listed on the page. Information is listed for the name of the data file, the user who uploaded it, the state of the file (typically will display UPLOADED), and the size of the file. A green checkmark will display, indicating the data upload was completed successfully.

  .. figure:: img/osgeo-upload.png

Uploaded data can be filtered by selecting one of the filter options. Available options allow you to filter by user, by state and by complete. Select on one of the links to narrow the results displayed to fit your filter criteria.

  .. figure:: img/osgeo-filter.png

2. Click on a file name to view the individual file information.

**Note:** These fields were populated at the time the file was imported, and should not be changed. This section should be thought of as for informational purposes only to view the status, size or file type for a file.

3. Click the browser’s back arrow to return to the previous page.

View Uploaded files and Uploaded layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Click either the **Upload files** or **Upload layers** link under the Osgeo_Importer menu on the Django Administration site Osgeo-Importer menu.

The Upload files page will display the directory link for the file.

  .. figure:: img/uploaded-files.png

      *List of uploaded files*

Clicking on the file link will open the Change file upload page, where you can change the uploaded file or view the file type. It is not recommended that this information is changed, as it could lead to loss of data. This is intended for reference only.

Selecting **Upload layers** will display the list of layers by name and feature count. The task ID will be the unique ID assigned to the layer upon upload.

  .. figure:: img/uploaded-layers.png

      *List of uploaded layers*

Delete uploaded data/files/layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users with administrator privileges are able to delete uploaded content from within the Django Administration site quickly, and easily.

1. From the list of uploaded content, click the checkbox next to the name of the data/files/layers you’d like to delete.

2. Select the delete option from the Action drop down menu, and click the **Go** button.

  .. figure:: img/delete-uploads.png

3. Verify your selection by clicking the :guilabel:`Yes, I’m sure` button.