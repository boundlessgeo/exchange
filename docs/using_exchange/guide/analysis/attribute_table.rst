.. _attributes:

Working within the Attribute Table
==================================

In the **Edit Features** section, you learned how to :ref:`add data <add>` to the attribute table, and how to :ref:`edit <edit>` the attributes of a feature on the map. Here we will discuss how to manipulate the data from within the attribute table to find exactly what you need.

To open the **Table View**, click on a layer, and select the :guilabel:`Show Table` button.

   .. figure:: img/show-table.png

All of the data provided for this layer will display in the Table View, though you may need to scroll up and down, or left and right to view all of the columns on the page. Select the left or right arrow buttons to move to a different page.

  .. figure:: img/table.png

View attribute statistics
-------------------------

The View Statistics feature helps you visualize the data within an attribute by presenting it as either a bar graph or a pie chart. This information can be useful when you want to quickly see how data within a given attribute is distributed, or how many unique categories are represented within a single attribute.

1. Click the attribute title for the data you’d like to display.

  .. figure:: img/select-attribute.png

2. Click the :guilabel:`View Statistics` button to open the summary statistics chart.

  .. figure:: img/view-stats-bttn.png

The attribute categories will be broken out into a bar graph, where each unique value in the field is represented by a single bar (or slice, if you are using a pie chart). The graph will show each of the unique values on the bottom axis, and the number of times that value is represented in the attribute table on the left side of the graph.

The View Statistics feature will give you a count of all of the features within the layer, the number of features with data populated in the attribute you are examining, and the number of unique values of the attribute itself.

*Using the chart below as an example, you can see the layer has a total of 1,460 features. The FacilityTO attribute (used to create the graph) has data populating each of those features. There are eight unique values within the FacilityTO attribute field, and the bar represents the number of times that value was entered for the attribute.*

  .. figure:: img/bar-graph.png

3. Click the :guilabel:`Show Pie Chart` button to change the display to a pie chart.

  .. figure:: img/pie-chart-button.png

  .. figure:: img/pie-chart.png

Search all attributes
---------------------

The Search All Fields search examines all of the attributes in a layer, and returns all features that have your search term in *any* of its attribute fields. It is a simple search that will find results from any location.

  .. figure:: img/search-all-fields.png

#. Type a search term in the Search All Fields text box.

#. Click the magnifying glass button. Your results will display in the attribute table.

**NOTE:** You can use the ``*`` or the **?** as wildcards if you aren’t sure of the exact spelling of a search term. The * matches any number of characters. You can use the asterisk ``(*)`` anywhere in a character string. For example, **wh*** will find what, wheat, and whale, but not awhile or watch. The **?** will match a single character in a specific position. A search for **r?t** will return rat or rot, but not rest or retract. A search of a partial word, or an open ended search, will return results containing those characters. Typing **abr** will return abrams and candelabra. You may also use a combination of the two. To clear the search, click the magnifying glass or the **X** button.

Advanced filters
----------------

Advanced filters can help with your analysis by returning only the features you want to see. Whether you are looking for data matching a specific attribute, or events occurring within a certain time period, using an advanced filter will help you find what you need.

1. Select the :guilabel:`Advanced Filters` button in the Table View to open the Filter by Attribute options.

2. Select an attribute type, and click the drop down menu to select whether you would like to filter for an exact match, or a term that would be contained within the results.

3. Add your search term to the text box, and click the :guilabel:`Apply Filters` button. Repeat these steps to add additional filters, and refine your search even more.

   .. figure:: img/advanced-filter.png

You are also able to filter attributes with dates or numbers by using either an exact match, or setting a range.

#. Click the drop down menu to select either **Exact Match** or **Range**. Type the date or number in the text box for an exact match, or select the dates/times using the calendar to establish a range.

#. Select the :guilabel:`Apply Filters` button.

   .. figure:: img/date-range-filter.gif

Your results will display in the Table View. To clear your results, and return to the complete list of features, select the :guilabel:`Clear Filters` button. Click the :guilabel:`Advanced Filters` button again to return to **Search All Fields**.
