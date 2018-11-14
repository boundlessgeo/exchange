Manage Layer History
====================

Version controlled layers
^^^^^^^^^^^^^^^^^^^^^^^^^

Layers with Version Control enabled in Boundless Exchange will have a GeoGig tab, in addition to the other tabs on the layer information page. The history lists all of the commits that have been made to the layer.

**Note:** Version Control is enabled during :ref:`layer upload <uploadlayers>`.

In the layer information page, click on the GeoGig tab to see the chronological list of commits. The number of commits, and the total number of contributors will display.

   .. figure:: img/geogig-tab.png

Notifications
^^^^^^^^^^^^^

Because Exchange is a real time collaboration tool, it is important for users to be able to see what changes other team members are making to a project. When users upload layers, they are given the option to import the layer(s) into GeoGig, which will show who has made what changes (for more on GeoGig, please reference the Working with Layers Management section). If another user has made modifications to a layer currently on the map, a number will appear next to the Notifications indicating how many unread notifications you have. The more notifications, the more changes that have been made to your map layers.

1. Click on the number of unread notifications to open the Notifications list in the layers menu. This will show you all of the changes that have been made to your layer. If there have been multiple changes, they may be grouped into sections based on when the changes occurred. Click on the grouping you would like to view.

  .. figure:: img/notification-list.png

    *Multiple changes were made to this layer, and have been grouped by time.*

2. From here you can either select :guilabel:`View on Map` or :guilabel:`Show Changes` to see what has been modified. View on Map will show you where the changes have been made on the map.

  .. figure:: img/view-on-map.png

  .. figure:: img/show-changes-bttn.png

3. Click the :guilabel:`Show Changes` button. Select :guilabel:`Yes` to acknowledge changes have been made to a feature, and compare the two versions.

  .. figure:: img/compare-changes.png

You will see a detailed side-by-side comparison of the features that have been edited.

  .. figure:: img/side-by-side.png

4. Changes made to the feature attributes will be highlighted in red, green or yellow, depending on whether the change was a deletion, addition or edit. Click the :guilabel:`Show Authors` button, and hover your mouse over the highlighted area to open a detailed description of the individual edit.

  .. figure:: img/show-author.png

5. If you do not approve of the changes, or feel they were made in error, you are able to select the :guilabel:`Undo Changes` button at the bottom of the details window to revert to the original feature.

  .. figure:: img/undo-changes.png

View layer history
^^^^^^^^^^^^^^^^^^

You can view all of the changes made to an entire layer from the map.

1. Select the name of the layer you want to view. The menu will expand to show additional layer options.

2. Click on the :guilabel:`Show History` button. The history will expand.

   .. figure:: img/show-history-bttn.png

3. Hover your mouse over a commit to view details about the changes. The color bar next to the commit indicates the type of edits that were made. Green indicates a new feature was added. Yellow indicates a feature was modified. Red indicates a feature was deleted. A commit can have multiple types of edits. In such cases, the bar will have colors representative of the types of edits that were made.

   .. figure:: img/show-history.png

      *History detail for a commit*

4. Click on a commit, and its history will update to show the individual edits within that commit. MapLoom will make one commit per edit.

   .. figure:: img/summary-changes.png

5. Click the :guilabel:`Show Changes` button to bring up a new window, displaying the specific changes that were made. The changes will be highlighted with the same color coding as the commits. Green means a feature was added. Yellow indicates the feature was changed. Redindicates the feature was deleted. In the image below, the feature was added, and so the feature on the map is highlighted in green.

   .. figure:: img/feature-history-changes.png

View feature history
^^^^^^^^^^^^^^^^^^^^

In addition to viewing the history of edits on a GeoGig layer, you can also view the history of a feature.

1. Select a feature on the map. The feature details will appear.

2. Click the :guilabel:`Show History` button. The history list will expand with the commits that contain changes for that feature.

   .. figure:: img/show-feature-history.png

3. Click the specific commit whose history you’d like to view. The history will update to show the edits made to the feature for that commit. Information about the feature will display as you hover your mouse over the changes.

   .. figure:: img/feature-history.png

4. Click the :guilabel:`Show Changes` button to bring up a new window, displaying the specific changes that were made.

   .. figure:: img/summary-of-changes.png

The changes will be highlighted with the same color coding as the commits. Green means something was added. Yellow means the feature was changed. Red means the feature was deleted. In the image below, the feature was added, and so the feature on the map and its attributes are highlighted in green.

  .. figure:: img/feature-history-diffs.png

5. Click the :guilabel:`Show Authors` button to see the names and dates for every attribute in the feature. Note that through the lifetime of a feature, there can be several authors. This is a good way to see who has contributed to a feature’s current state.

   .. figure:: img/show-authors.png

Summarize history
^^^^^^^^^^^^^^^^^

You can visualize a summary of all of the edits within a date range for a layer.

1. Click the :guilabel:`Show History` button for layer you want to summarize.

   .. figure:: img/show-history-bttn.png

2. Click the :guilabel:`History Summary` button.

   .. figure:: img/history-summary.png

3. Enter the date range for the history to summarize.

   .. figure:: img/date-summary.png

4. Click the :guilabel:`Summarize` button. The edited features will be highlighted, and will be listed under the Summary of Changes field.

   .. figure:: img/summary.png

5. Click the :guilabel:`Show Changes` button for one of the edits in the list to see a detailed view.

Export history
^^^^^^^^^^^^^^

You can export a summary of all of the edits within a date range for a layer.

1. Click the :guilabel:`Show History` button for layer you want to summarize.

   .. figure:: img/show-history-bttn.png

2. Click on the :guilabel:`History Summary` button

   .. figure:: img/history-summary.png

3. Enter the date range for the history to summarize.

   .. figure:: img/export-history.png

4. Click the :guilabel:`Export CSV` button.

5. When prompted to save the file, browse to the location where you want to save it, and click Ok.

All of the feature change history will be added to the spreadsheet.

  .. figure:: img/export-csv.png