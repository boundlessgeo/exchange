Working with Maps
=================

Maps are comprised of various layers and their styles. Layers are available as local layers, or they can be remote layers, served from other web servers. Exchange maps can be manipulated via map zoom and extent, layer ordering, and style.

Create a map
------------

Maps can be created multiple ways within Exchange. If you’re starting a new project, you may want to start with a new, blank map. You can also create maps from existing layers and existing maps. The following steps will help you create the map environment you need.

Create a new blank map
^^^^^^^^^^^^^^^^^^^^^^

1. Select the :guilabel:`Maps` link on the Boundless Exchange toolbar.

2. Click **Create Map** in the drop-down menu.

  .. figure:: img/map-menu.png

A new map environment will open, and you can begin working.

Create a new map from layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Layers can be used to create maps, and added from either the Explore Layers or Explore Maps section.

1. Select the :guilabel:`Data` link on the Boundless Exchange toolbar, and click **Layers** in the drop-down menu.

  .. figure:: img/data-menu.png

2. Click the **Plus** icon next to the layer you’d like to add to your map. You can select multiple layers. They will display in your workspace until you are ready to build your map.

3. Click the :guilabel:`Open Workspace in map` button to add the layers in the workspace to a new map.

  .. figure:: img/workspace.png

    *Remove a layer from the workspace by clicking the X button next to its name.*

A new map will open with all of the layers displayed, and listed in the map menu.

Add layers to a map
-------------------

You can add layers to the map from within the map environment using the Add Layer feature. Layers can be added from either the local geoserver within Exchange, or from a remote service.

The local geoserver hosts layers that have been added to Exchange by other registered users. Local layers can be discovered through an advanced search from the Boundless Exchange homepage, from the Explore Layers page, and from within the map.

A remote service is a separately-hosted data service of varying type (OGC,  Esri, etc). Remote services appear within the map and in search as layers. Rather than having to re-upload the files found within a particular service to Exchange, an external service’s layers are indexed and allow the user to find them and add them to their map.

**Note:** Layers with time enabled features must be added via Explore Layers or the search function from the workspace. They will not function properly if they are added directly from the map.

#. Click the Add Layer :guilabel:`(+)` button in the Layers field.

   .. figure:: img/add-layer-bttn.png

The Add Layers window will open, and you can begin your search using the settings on the left side of the screen.

   .. figure:: img/add-layer.png

2. **Using the map -** Zoom in or out to your area of interest. The list of available layers will change to show you what is within the map extent (minus any layers currently on your map).

Zoom to limit the search to data that includes features in the displayed area. Hover your mouse over a layer in the results list. A bounding box will display over the layer’s coverage area. Each layer will tell you whether it is from the local geoserver, or a remote service.

  .. figure:: img/bounding-box.png

3. **Keywords -** Add keywords to find specific layers. Words associated in the metadata, and the title are used for results. Select the Clear link to remove the filter.

  .. figure:: img/keywords.png

4. **By owner -** Click the checkbox next to an individual’s name to return layers added by that user. If you are collaborating on a project, this is a fast way to find layers from your team members.

  .. figure:: img/by-owner.png

5. **Date Created -** Click and drag the time bar to filter layers by their creation date.

6. **Category -** Click the checkbox next to one or more categories to filter layers by their metadata category.

7. Once your results have been filtered, select the layers you’d like to add to your map from the results list, and click the :guilabel:`Add Layers` button. Your layer(s) will now display on your map, and in the layers list.

  .. figure:: img/added-layers.png

Change layer order
^^^^^^^^^^^^^^^^^^

Layers on a map are drawn from bottom to top. The top layer in your list will display on top of any layers below it. Each layer will appear in the order it is displayed in your list. Sometimes a layer may need to be reordered so it can be more clearly displayed.

#. Click on the name of the layer you want to reorder.

#. Drag the layer up or down to the desired position.

Toggle layer visibility
^^^^^^^^^^^^^^^^^^^^^^^

Toggle Visibility allows you to turn a layer’s display off and on without having to remove the layer form the map completely.

  .. figure:: img/toggle-layer.png

#. Click the Toggle Visibility button to turn a layer off.

#. Click the Toggle Visibility button again to turn a layer back on.

Zoom to data
^^^^^^^^^^^^

The Zoom to data button allows you to center the map quickly on a particular layer. It is particularly convenient when you need to quickly return to the extent of the data for that layer.

#. Click a layer in the layer list.

#. Click the :guilabel:`Zoom to data` button. The map will zoom in and center on that particular layer's extent.

  .. figure:: img/zoom-data.png

.. important:: If a layer’s visibility is dependent on scale, and the data extent is at a lower scale, you will need to zoom in to view the data.

Show layer info
^^^^^^^^^^^^^^^

Information about a layer is available in the map by clicking the Show Layer Info button. Show Layer Info will include server information, basic metadata, and the projection (SRS).

#. Click on a layer name in the layer list to expand the layer options.

#. Click the :guilabel:`Show Layer Info` button.

  .. figure:: img/show-info.png

The Layer Info window will display.

   .. figure:: img/layer-info.png

Remove a layer from the map
^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. To remove a layer from the map, click the name of the layer you’d like to remove, and click the :guilabel:`Remove layer` button in the layer tools.

   .. figure:: img/remove-layer.png

#. Click the :guilabel:`Yes` button to confirm.

   .. figure:: img/confirm-remove.png

Modify layer transparency
^^^^^^^^^^^^^^^^^^^^^^^^^

The transparency of a layer can be adjusted for viewing the map beneath the layer. Click and drag the slide button to adjust the transparency. As the transparency increases, you will see more of the map. As opacity increases, the layer features will be more prominent.

  .. figure:: img/transparency.png
  
  .. figure:: img/more-transparent.png
  
    *Example of increased transparency*
  
  .. figure:: img/more-opacity.png
  
    *Example of no transparency selected*

Get feature information
^^^^^^^^^^^^^^^^^^^^^^^

To get information for a feature, simply click the feature on the map. Once you select a feature, the information window will display. The point of the information window will touch the feature you clicked.

.. figure:: img/get-feature-info.png

**Note:** Get feature information is now available for a WMS remote service, but external services do not provide as much data as other layers and will have a more simplified display.

  .. figure:: img/wms-popup.png

    *This is an example of a feature from a WMS layer*

Change attribute visibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Individual attribute visibility can be turned off and on in a feature window. This can make managing large numbers of attribute fields in a layer easier.

#. In the layers list on the map, select on the layer whose attribute visibility you'd like to change.  The layer’s additional options will display.

2. Click the :guilabel:`Show Attribute Visibility` button to open the list of attributes for the layer.

  .. figure:: img/attribute-visibility.png

3. Click on the :guilabel:`Toggle Visibility` button for an attribute to turn it off and on.

  .. figure:: img/layer-attribute-visibility.png

4. Select a feature on the map from that layer. The attribute will no longer appear in the feature information window, as it has been toggled off. Repeat these steps to toggle it back on.

Search for locations
^^^^^^^^^^^^^^^^^^^^

FFind a specific location on the map simply by typing the name of a place, zip code, address or lat/long (DMS or DD) in the Search Locations textbox. Click the search button to return a list of possible matches. Scroll through the list, and select one of the matches. The map will recenter on that location. This is a simple search, and does not allow wildcards.

  .. figure:: img/search-locations.png

Using the legend
^^^^^^^^^^^^^^^^

A legend displayed the symbols used for vector layers in a map. It can be toggled off and on to maximize screen space when necessary.

.. figure:: img/legend.png

Click the Toggle Legend button to toggle the legend off and on.

Additional map features
^^^^^^^^^^^^^^^^^^^^^^^

There are additional features which allow you to change your coordinate display, your full screen extent, and your map scale.

1. Click the :guilabel:`Toggle Full Screen` button to maximize your map environment to the full screen.

  .. figure:: img/toggle-full-screen.png

2. Click the :guilabel:`Zoom In (+) / Zoom Out (-)` buttons, or click and drag the scroll bar to zoom in and out on the map. Click the :guilabel:`Zoom to World` button to return to the world view.

  .. figure:: img/zoom-buttons.png

3. Click the :guilabel:`Switch Coordinate Display` button, in the lower left corner of your map, to change the coordinate system. Your available options are DMS, DD (or XY) and MGRS. Click the button additional times to cycle through to your desired display. Your scale bar is located just above the coordinate display.

  .. figure:: img/coord-display.png

Measure distance or area
^^^^^^^^^^^^^^^^^^^^^^^^

You can measure distance or areas on your map using the Measure tool.

1. To measure an area or distance on the map, select the Measure field. The measure tools will open, and you can select whether you want to measure a line distance, or an area.

2. **Area** - Click the :guilabel:`Area` button in the Measure tools. Begin drawing by clicking your mouse on your map at your starting point. Click subsequent points around the area you want to measure.  To complete your measurement, you will need to ensure you close your polygon by clicking on your starting point.

  .. figure:: img/measure-area.gif

  **Line** - Click the Length button in the Measure tools. Begin drawing by clicking your mouse at your starting point. Click subsequent points along the route or feature you want to measure.

  .. figure:: img/measure-line.gif

3. To complete your measurement, click your mouse at the end distance. The line will turn from a bold blue to a thin blue line. The distance will display as meters/kilometers, miles or feet, depending which unit you have selected.

4. Click the :guilabel:`Stop Measuring` button to clear your map and measurements.

Save a map
^^^^^^^^^^

Saving a map allows you to maintain your preferences for the next use, as well as makes it available for other Exchange users.

1. Click the :guilabel:`Save this map` button.

  .. figure:: img/save-map.png

2. Add a title and an abstract for your map so it is searchable by others. Click the Save button to save your changes. The name will be reflected in the title, and replace “New Map.”

3. Select the Refresh Interval drop-down menu to choose a refresh rate for your map. This will help ensure your map is as current as possible.

  .. figure:: img/save-this-map.png

The Map is now saved in the list of maps on the Maps page.

For MapLoom version info, hover the mouse over the **i** info button in the lower left corner of the window.

Share a saved map
^^^^^^^^^^^^^^^^^

A link will be created for your saved map. Copy the link to share with other users. 

  .. figure:: img/share-map.png

Create a copy of a map
^^^^^^^^^^^^^^^^^^^^^^

You can use an existing map as a starting point for another map. This allows you to incorporate the work others have done without changing their maps.

1. Click **Maps** on the  Boundless Exchange toolbar, and select Explore Maps in the drop-down menu.

2. Select on the map you would like to copy. This will open the map details page.

3. Click the :guilabel:`Create a New Map` button under the Copy this map section.

   .. figure:: img/copy-map.png

A new map will open, populated with all of the layers of the map you copied.

4. Click the :guilabel:`Save this map` button on the toolbar.

5. Add a new title and an abstract, possibly indicating this is a copy of another map.

6. Click the :guilabel:`Save Copy` button.

Your new map is now saved, and can be accessed from the maps page.

.. important:: You are only copying the map. Any changes you make to the layer (data set) will affect any maps using that layer. Copying the map would primarily be used to make visual changes. To make changes to the data, it is recommended that you download the layer, and import your own copy.

Managing Maps
-------------

Every map has its own details page, which provides more information about the map, the metadata and who has what permissions for making edits.

Click the **View Details** link to open the details page.

  .. figure:: img/view-details2.png

The map details page provides a view of the map, and displays any associated comments or ratings.

  .. figure:: img/map-details.png

All associated layers and documents will be listed, with links to their respective details pages. Simply click the title of the associated file to open the page.

  .. figure:: img/associated.png

Edit map metadata
^^^^^^^^^^^^^^^^^

Metadata plays an important role for maps. It describes the map in a way that the legend does not; why it was created, the date it was published, and who created it, for example. When a map is updated, it is important to update the metadata, as well.

**Note:** You can only edit the metadata for the map if you have the proper permissions.

1. Click the :guilabel:`Edit Map` button.

2. Click the :guilabel:`Edit` button under Metadata on the Edit Map menu.

   .. figure:: img/edit-map.png

3. In the metadata page, fill in the fields with information about the map. The more information you provide, the better others will understand your map.

**Note:** The “Category” field is a mandatory field, and if it has not previously been selected, you will be required to select one at that time.

4. Click the :guilabel:`Update` button to save your changes.

Set map thumbnail
^^^^^^^^^^^^^^^^^

By default the thumbnail images for maps will only have the vector layers. In order to include the background map you will need to use the Set Map Thumbnail button.

1. Pan and/or zoom the inset map on the **Map Details** page so that it’s centered on the view you would like for the map thumbnail.

2. Click the :guilabel:`Edit Map` button.

3. Click the :guilabel:`Set` button under Thumbnail on the Edit Map menu.

   .. figure:: img/edit-map.png

This will set the map thumbnail with the base map and layers included.

.. figure:: img/view-details.png

  *Old Thumbnail*

.. figure:: img/new-thumbnail.png

   *New Thumbnail*

Create a custom thumbnail
^^^^^^^^^^^^^^^^^^^^^^^^^

Custom images related to your map can be created, and will display next to the map on the Explore Maps page.

1. From the map’s info page, click the :guilabel:`Edit Map` button.

  .. figure:: img/edit-map-bttn.png

2. Click the :guilabel:`Set from File` button to browse to the image. Select the image you want to use, and verify it displays in the thumbnail section.

  .. figure:: img/file-thumbnail.png

Edit map permissions
^^^^^^^^^^^^^^^^^^^^

The map permissions determine which users can view or edit a map. The permissions can be set to establish:

* Who can view it?
* Who can download it?
* Who can change metadata for it?
* Who can manage it (update, delete, change permissions, publish/edit)?

#. Click the :guilabel:`Change Permissions of this Map` button in the Permissions section.

    .. figure:: img/permissions.png

#. Establish the permissions for viewing, editing, and managing according to your needs.

    .. figure:: img/set-permissions.png

#. Click the **Apply Changes** button to save changes.

Remove a map
^^^^^^^^^^^^

You are able to remove a map from Exchange. It is important to note that this will remove the map for all users.

#. Click the :guilabel:`Edit Map` button.

   .. figure:: img/edit-map.png

#. Click the red :guilabel:`Remove` button under Map in the Edit Map menu.

#. Click the :guilabel:`Yes` button to confirm.

  .. figure:: img/remove-map.png
