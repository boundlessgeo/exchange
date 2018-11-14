Documents
=========

The Documents section is designed to help manage documents that have been added to Exchange. This section will explain how to add new documents through Django, and how to edit and delete existing documents. All of the options in this section are available through the Documents menu on the Django Site administration page.

Add a document
^^^^^^^^^^^^^^

1. Click the **Add** link next to Documents on the Django Administration site Documents menu.

  .. figure:: img/documents.png

2. Complete as much of the Add document form as possible; all of the fields on the form in **bold** are required.

You will see this form throughout the Django admin site. Additional fields are used in the Maps and Layers section.

  .. figure:: img/add-document.png

**Uuid -**  This field is required, and is only auto-generated through the Exchange User Interface. You can find UUID generators online to help you create one for use here.

**Owner -** Type or select your user name from the list.

**Title -** Provide a title for your document.

**Date/Time -** The date and time will automatically populate with the document upload date. It is the reference date for the document, and does not need to correlate to the time period of the data (which will be configured later).

**Date type -** This will indicate whether the date/time from above is related to the document’s creation, publication or revision.

**Edition -** If there have been revisions to your document, you can let users know by adding a version number here.

**Abstract -** Let others know what the document is about with a brief narrative summary.

**Purpose -** Provide a short description of why the document was created.

**Maintenance frequency -** From the pull down, select how often modifications and deletions are made to the data after it is first published.

  .. figure:: img/maintenance-freq.png

**Keywords region -** Select a region/country from the list which best fits the data. Hold down Control, or Command on a Mac, to select more than one.

**Restrictions -** Select from a list of limitations which can be placed on the access or use of the data. Provide a description of “Other Restrictions” in the textbox.

  .. figure:: img/restrictions.png

**License -** Select data licensing requirements from the list. Not all data has licensing requirements.

  .. figure:: img/licenses.png

**Language -** Select the language used within the dataset.

**Category -** Data is divided into categories, which assists in the grouping and search of available geographic datasets. These categories correspond to those on the Exchange homepage.

**Spatial representation type -** This explains the method used to represent geographic information in the dataset.

  .. figure:: img/represent.png

**Temporal extent start / end -** Set the time period covered by the content of the dataset.

**Supplemental information -** Include any other descriptive information about the dataset.

**Data quality statement -** Provide a general description of the validity and legitimacy of the dataset. Explain any changes in the data over time.

**Bounding boxes -** There are four boxes to enter the coordinates for your bounding boxes. Enter the points for all of the X,Y coordinates.

  .. Important:: **The following fields are automatically populated by Exchange, and should not be changed. Making edits to these fields could result in data loss.**

-  Srid
-  CSW typename
-  CSW schema
-  CSW source
-  CSW type
-  CSW anytext
-  CSW WKT geometry
-  Metadata xml
-  Object ID

  .. figure:: img/csw-document.png

**Metadata -** Click the checkboxes to ensure the metadata is uploaded and preserved. The Metadata XML will automatically generate once the document is saved.

**Counts -** Popular count and Share count will update as the document is viewed and shared.

**Featured -** Click the checkbox to feature this document on the homepage under the Featured Content section.

**Is Published -** This allows others to find your document when it is completed. It will make it searchable through the Exchange search.

**Thumbnail URL -** Enter the URL for the thumbnail for your document. This will be what users see when searching for your document in Exchange.

**Detail URL -** This is the number assigned to your document, and is added to the end of the Exchange URL. This can make accessing your document easier in the future; just enter the Exchange URL, followed by /document/<document number>. The detail URL is created after saving your document.

**Rating -** Once your document is published, others can provide a rating to let you know what they think of it.

**Content type -**  This does not necessarily correspond to the file’s extension type, but rather the type of data in the file.

**File -** Click the Choose File button to browse to and change the file.

**Extension -** The following file types can be uploaded: **.doc, .docx, .gif, .jpg, .jpeg, .ods, .odt, .pdf, .png, .ppt, .pptx, .rar, .sid, .tif, .tiff, .txt, .xls, .xlsx, .xml, .zip, .gz, .qml**.

**Doc type -** Is the file an image, document, presentation, etc.?

**URL -** The URL of the document if it is external.

**Keywords -** Enter words or phrases, separated by commas, used to describe the subject, and can be search by other users.

3. Once you have completed the form, click the :guilabel:`Save` button to add your document to Exchange.

Edit existing documents
^^^^^^^^^^^^^^^^^^^^^^^

1. To edit an existing document, click the Change link in the Documents menu.

2. Find the document you’d like to edit. You can do this multiple ways:

-  Type all or part of the document name in the search field at the top of the page.
-  Select a filter term on the right side of the page to minimize document results
-  Scroll through the list of results.

  .. figure:: img/document-list.png

3. Click on the ID number of the document you’d like to edit. The Change document page will open, and you can begin editing the metadata.

4. Click the :guilabel:`Save` button once you have made all of your edits.

Delete a document
^^^^^^^^^^^^^^^^^

If you no longer need a document, and would like to remove it from Exchange, it can be quickly and easily deleted from the system.

1. Click **Change** in the Documents menu to open the list of all documents.

2. Click the checkbox next to the document you’d like to delete.

3. Select **Delete selected documents** from the Action menu, and click the :guilabel:`Go` button.

  .. figure:: img/delete.png

4. Click the :guilabel:`Yes, I’m sure` button to verify your selection. You will be notified that the document was successfully deleted.

Your document will no longer be available in Exchange.