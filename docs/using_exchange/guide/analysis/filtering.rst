Filter Features for Deeper Analysis
===================================


Spatial filters
----------------

Spatial filters are used to select features from one layer based on their location in relation to features from another layer. The overlapping, or intersecting, data will be filtered in the attribute table, and can be used for additional analysis.

#. Click a feature on the map to select it. This will set the boundaries for the filter, and all of the returned data will be within this feature.

#. Click the filter button to **Use this feature in a spatial filter**. The selected feature will change colors.

#. Click a feature from the layer you want to filter, and click the :guilabel:`Show Table` button in the information window. This will open the attribute table for the entire layer. All of the features in this layer will display in the attribute table.

#. Click the :guilabel:`Spatial Filter` button in the Table View. This filters the data to display only the features intersecting the original feature.

   .. figure:: img/spatial-filter.gif

    *Filter intersecting feature attributes*

You can expand your spatial filter by selecting additional features from your layer. The results will be displayed in your attributes table.

   .. figure:: img/multi-spatial.gif

    *In the first example, there were 15 results using the spatial filter. By selecting additional features, there are now 42 results that intersect the layer.*

A spatial filter can also be created using an individual point with a given radius, allowing you to see how many features from a second layer fall within that radius.

#. Click a point on the map from the desired layer. This will be the base point. A blue circle will highlight the point.

#. Click the filter button to :guilabel:`Use this feature in a spatial filter`. The selected feature will change colors. Enter the desired radius in meters when prompted. Click the :guilabel:`Add Spatial Filter` button.

#. Click a feature from the layer you want to filter, and click the :guilabel:`Show Table` button in the information window. This will open the attribute table, which will include all layer features.

#. Click the :guilabel:`Spatial Filter` button in the Table View. This filters the data to display only the features within the radius on the original point.

   .. figure:: img/point-spatial.gif

  *This example shows how many Department of Health facilities are within a 4000 meter radius of central Lake Charles, LA. The spatial filter narrows the results down to 17 facilities out of 1458.*

You can edit the geometry of an existing spatial filter to adjust the size of the filter area.

#. Select a spatial filter feature on the map, and click the :guilabel:`Edit Geometry` button. The selected feature will change colors and the Editing Geometry window will open.

#. A blue dot will appear over the point on the feature to be moved.

#. Click and drag the point to its new location. Repeat this process until all of the points have been moved to their new location.

#. Select the :guilabel:`Accept Feature` button to finish your edits, and apply the new shape to your spatial filter.

   .. figure:: img/edit-spatial.gif

Delete a spatial filter
-----------------------

Once you are finished with your spatial filter, you may want to clear the results, and remove the filter from your map.

#. From the Table View of your filtered results, select the :guilabel:`Spatial Filter` button. This will clear the filter, and  show all features within the layer. Close the Table View window.

#. Click on the feature you used in your spatial filter, and select the :guilabel:`Delete Feature` button. Confirm that you want to delete the feature.

Combine filters
---------------

Combining a filter by attribute and a spatial filter allows you to dig even deeper into your data to provide better analysis. Once you have completed your spatial filter, you can use an **Advanced Filter** to drill down even further.

1. With an existing spatial filter on the map, open the table view of the layer you want to further filter. Your table will display all of the features in the layer.

2. Click the Advanced Filters button, and select the attribute you’d like to add to the spatial filter. Click the drop down menu to select the appropriate criteria.

3. Add your search term to the text box, and click the Apply Filters button. This will filter your layer to those features containing the attribute you want to apply to the spatial filter.

4. Click the Spatial Filter button to apply the spatial filter.

Not only will all of your results fall completely within the area you selected for your spatial filter, but they will also meet your advanced filter criteria.

  .. figure:: img/complex-filter.gif

  *Using the Department of Health layer from the previous example, we want to find out how many of the facilities within our 4000 meter radius are hospitals. We filtered all facility types (in the FacilityTO attribute) to those containing the word hospital. There were 254 results. Next, we applied the spatial filter. Our search helped us determine that out of 1458 features, four are hospitals within a 4000 meter radius of Lake Charles, LA.*

Filter features by timeline
---------------------------

Features will often have a time attribute detailing the specific time an event has occurred, or when a feature has changed. This information can be displayed in two ways. Continuous time focuses on the changes of a singular feature, such as the path of a tornado, or the spread of disease. Temporal data also tracks multiple features in single locations over time, such as store openings, lightning strikes, or cell phones pinging cell towers. Temporal data can be displayed in Exchange either as a whole (the entire layer at once), or it can be played back, with the features populating the map as the time bar progresses.

  **Note:** For this feature, the layer must have a date/time attribute. The time attribute is configured when the layer is uploaded. Please see the section on Configuring Time Attributes under Working with layers for more information.

  .. figure:: img/playback-options.png

    *A layer with temporal data will have a toolbar with playback options at the bottom of the map.*

1. Add a layer with the temporal data to the map. The playback options will display at the bottom of your map.

2. Click the :guilabel:`Play` button to begin the playback for the layer. The features will populate, and display the date/time along the timeline.

  .. figure:: img/timeline-feature.gif

3. Select additional playback options. Playback options include:

  **Play / Pause** - Begins and stops the playback feature.

You can click and drag the time slider to display features at a specific time, or click on the red lines along the timeline. The spacing of the lines indicates the times on the layer.

  **Repeat** - Loops the playback so it automatically begins once all of the temporal features have displayed.

  **Step Back / Step Forward** - Displays the previous feature again or skips forward to the next feature.

4. Select the :guilabel:`Filter Features by Timeline` button to display all of the features at once, essentially turning off the playback.

  .. figure:: img/time-filter-off.gif

    *Filter features by timeline turns off the timeline feature for a layer.*
    
Create a heat map
-----------------

A heat map is a visual representation of your data, and allows you to see where your data is concentrated.

1. Select a point feature layer from your layers list.

2. Click the :guilabel:`Show heatmap` button to create a heat map layer.

  .. figure:: img/show-heatmap.png

On the heat map, red indicates a high area of data concentration.

    .. figure:: img/heatmap.png

Remove a heatmap
----------------

Quickly remove a heatmap from the display by selecting the heatmap layer, and clicking the :guilabel:`Remove Layer` button.

  .. figure:: img/remove-heatmap.png

