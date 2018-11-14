Add or Edit Metadata
====================

1. From the search results page, click the **View Details** link for the map, document or layer that you’d like to edit. The details page for that resource will open.

2. Click the :guilabel:`Edit <resource> button`, and select the :guilabel:`Edit` button under Metadata. The Edit Metadata page will display.

  .. figure:: img/edit-map.png

  .. figure:: img/edit-doc.png

  .. figure:: img/edit-layer.png

  .. figure:: img/edit-metadata.png

3. Edit the information fields to include anything pertinent to the resource. **Note:** Once you begin to edit the metadata, the Category field becomes mandatory.

  .. figure:: img/owner-date-type.png

**Owner** - The Exchange user who uploaded the document or layer, or created the map.

**Title** - This should be the original title of the resource, and will not have the unique identifier assigned by Exchange.

**Date** - This is the date the resource was created in Exchange.

**Date type** - The identification of when a given event occurred.

  Click on the **Date type** menu, and select whether this is the creation date (of the original data), publication date (into Exchange) or the revision date for the resource.

  .. figure:: img/date-type.png

**Edition** - The version of the cited resource.

  .. figure:: img/edition-frequency.png

**Abstract** - A brief narrative summary of the content of the resource.

**Purpose** - A summary of why the resource was created.

**Maintenance Frequency** - Frequency with which modifications and deletions are made to the data after it is first produced.

  .. figure:: img/frequency.png

**Regions** - Select a region/country from the list which best fits the data. Hold down Ctrl, or Command on a Mac, to select more than one.

  .. figure:: img/regions-license.png

**Restrictions** - Select from a list of limitations which can be placed on the access or use of the data. Provide a description of other restrictions and prerequisites for accessing and using the resource or metadata in the “Other Restrictions” textbox.

**License** - Select data licensing requirements from the list. Not all data has licensing requirements.

  .. figure:: img/license.png

**Language** - Select the language used within the dataset.

**Spatial representation type** - This explains the method used to represent geographic information in the dataset.

  .. figure:: img/spatial-representation.png

**Temporal extent start / end** - Set the time period covered by the content of the dataset.

  Select the start and end date of the temporal data by clicking on the calendar icon, and choosing a date.

  .. figure:: img/temporal-extent.png

**Supplemental information** - Include any other descriptive information about the dataset.

  .. figure: img/supplemental.png

**Data quality statement** - Provide a general description of the validity and legitimacy of the dataset. Explain any changes in the data over time.

  .. figure:: img/data-quality.png

**Group** - From the drop-down menu, select which group has permission to access this data.

  .. figure:: img/group.png

Select the checkboxes for the options you’d like to turn on/off.

  .. figure:: img/checkboxes.png

Ensure the box is checked if:
  * You’d like to ensure no one is able to edit the metadata
  * The dataset is featured on the Exchange homepage
  * The resource is published, and made available through search for other users

**Note:** If you have added a resource to Exchange, and you’re unable to find it through a search, verify it has been published.

  * The raster data is part of a mosaic
  * The vector has a time attribute that you’d like to enable for temporal viewing
  * The raster has associated elevation information

**Link to (documents only)** - Select a map or layer in the drop down list. This will associate the document to that resource.

  .. figure:: img/link-to.png

**Regex (layers only)** - Select the regular expression for the time and/or elevation of raster data.

  .. figure:: img/regex.png
  
**Service** - To link the layer to an existing remote service, select it from the drop-down menu.

  .. figure:: img/service.png

**Site URL and Featured Map URL (maps only)** -

  .. figure:: img/site-map-url.png

**Keywords** - Provide terms to associate to your dataset. This will allow other users find the resource based on terms related to its content. Multiple keywords can be added, separated by a comma.

**Point of Contact** - This is the individual to contact, should you have questions regarding the metadata.

**Metadata Author** - The individual who originally added the metadata content. This will most likely be the same as the Point of Contact.

**Note:** You are not able to edit the Owner, Point of Contact or Metadata Author.

  .. figure:: img/poc.png

  
**Category** - Data is divided into categories, which assists in the grouping and search of available geographic datasets. These categories correspond to those on the Exchange homepage.

  .. figure:: img/category.png

**Attributes (layers only)** - All of the attributes for a layer will be listed. Edits can be made to the Label, Description, and Display Order fields.

  .. figure:: img/attributes.png

Click your mouse in the field you’d like to edit, and make your changes. You can select the up or down buttons in the Display Order field to change the order of where the attribute will display in the attribute list.

**Note:** If you change the order of one attribute, make sure you have changed the corresponding attribute to prevent duplicates.

Select the checkbox beneath the Visible column to turn off/on the visibility of an attribute. This will affect the attribute visibility on the map.

Select the checkbox beneath the Required column to require users to input a value for that attribute.

Select the checkbox beneath the Readonly column to ensure no one else can modify the attribute or its values.

**Constraints** - Attribute values can be edited to establish minimums and maximums for the data. This helps prevent data inconsistency, as well as ensures the values fall within the expected ranges. 

For our example, we are using the surface attribute to clarify whether a bike path is paved or unpaved. We want to ensure the attribute value added is limited to those two options. This provides continuity, and reduces ambiguity among answers (*e.g.* gravel, cement, dirt).

Click the orange carrot next to the field to implement constraints.

  .. figure:: img/constraints.png
  
Select the Control Type drop-down menu, and choose the option which best represents the way you’d like to represent the options.

  .. figure:: img/control-type.png
  
Select the blue Options :guilabel:`( + )`  button to add the values and labels for the data. In the example, we use **1** to represent a paved path, and **2** to represent an unpaved path.

When a user edits that value from the map, the are only presented with two values, and cannot add one that is unexpected. Note: Please see the Edit attributes section in Editing and Version Management for more information.

  .. figure:: img/map-edit.png

4. When you’re finished, click the :guilabel:`Update` button to save your changes.