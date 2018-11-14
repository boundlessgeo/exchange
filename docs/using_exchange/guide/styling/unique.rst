Unique
^^^^^^

The Unique style format requires you to have a relatively good understanding of your dataset. In this format, a different style will be applied to each unique value in an attribute field.

1. Click the title of the layer in the layer list to expand the layer options.

2. Click the :guilabel:`Style Layer` button to open the style options.

The style options will open, and default to the Simple format.

3. Click the arrow next to the right of the “Simple” header to go to  the Unique format options.

  .. figure:: img/unique.png

The Unique style format classifies the individual values for an attribute, and represents each of those values with a different color. It breaks the attribute data into qualitative groups, and makes each value its own color.

4. Under Classification, select the attribute from the pull down menu whose data will be divided into unique values.

5. Type the number of unique values for the attribute in the text box.

Understanding the dataset becomes increasingly important at this step, as you need to know how many unique values are represented for that attribute.

**Prot Tip:** For a fast count of how many unique values are available within a particular attribute, use the :ref:`View Statistics <attributes>` feature from the Analyzing Data section. It will give a quick count of unique values for the attribute.

6. Select a color palette option from the drop down menu to represent each unique value.

  .. figure:: img/color-palette.png

7. Select options from the Stroke pull down menus to change how the feature outline is displayed.  Select options to change the line from solid, dashed or dotted. Click the color block to select a new color.

  .. figure:: img/simple-stroke.png

8. If you would like to turn on an attribute label for your features, simply select the attribute in the pull down menu. You can also select the script, text size and color from the Label section.

  .. figure:: img/simple-label.png

Rules represent the breakdown of the individual values and their corresponding color from your attribute selections. You can click the **X** to remove a feature from this list, and it will not be represented on the map.

  .. figure:: img/unique-rules.png

9. Once you’ve finished making your changes, click the :guilabel:`Save Layer Changes` button for them to take effect.

This is what the layer looks like once the Unique style selections have been saved. Each feature is represented by a different color. The outline of the individual features is represented by the purple dashed line. Refresh the map to display the changes in the legend.

  .. figure:: img/unique-after.png