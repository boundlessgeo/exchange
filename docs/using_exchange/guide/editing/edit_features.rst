.. _edit:

Edit Layer Features
===================

Edit attributes
^^^^^^^^^^^^^^^

If a layer is able to be edited, Exchange allows you to make attribute changes directly from the map.

1. Select a feature on the map. The feature info box will appear.

2. Click the :guilabel:`Edit Attributes` button to open the Edit Attributes window.

3. Add attribute information as necessary.

4. Click the :guilabel:`Save` button to save your changes.

.. figure:: img/edit-attributes.gif

Edit point geometries on the map
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Point layers can be either simple point or multi-points layers. For simple point layer, there is one point per feature. Multi-point layers will have more than one point per feature.

1. Select a point feature on the map to open the feature info box.

2. Click the :guilabel:`Edit Geometry` button. This will open the Drawing Geometry dialog at the top of the screen. Your selected feature will be highlighted in blue.

3. Click and drag the feature to a new location.

4. Click the :guilabel:`Accept Feature` button to save the new feature location. Click the :guilabel:`Cancel` button to cancel your edit.

.. figure:: img/edit-point-geometry.gif

Edit point geometry manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coordinates for point geometries can also be edited manually. This is useful when you have the coordinates from another source (such as a report or agency).

1. Select a point feature on the map to open the feature info box.

2. Click the :guilabel:`Edit Attributes` button. The Edit Attributes window will open.

3. Click the Location field to edit the point's coordinates. Add the new location.

4. Click the :guilabel:`Save` button to save your changes.

  .. figure:: img/edit-points-manually.gif

Edit line or polygon geometries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any existing feature in a layer can be modified, if you have permission to edit the layer. A layer that has been saved to GeoGig will maintain a history of all of the edits to ensure the provenance of the data.

1. Select a feature on the map to be edited. This will open the feature info box.

2. Click the :guilabel:`Edit Geometry` button. The Editing Geometry dialog will open.

3. Mouse over the geometry to highlight the vertex to edit. Click and drag the vertex to a new location. Repeat to edit any additional vertices.

  .. figure:: img/edit-poly.gif