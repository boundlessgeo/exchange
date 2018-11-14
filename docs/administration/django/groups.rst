Groups
======

The Groups section of the Django administration site allows users with admin credentials to manage groups within Exchange. This section will explain how to invite individuals to groups, create or delete groups, and modify group profiles.

  .. figure:: img/groups.png

Create a group
^^^^^^^^^^^^^^

1. Click the **Add** link next to Group profiles on the Django Administration site Groups menu to open the Add group profile page.

2. Provide a unique title for your group. This will also be what is used for the Slug field. The Slug is a unique identifier for your group. If your group title is comprised of multiple words, you will need to use a hyphen or an underscore to replace the spaces.

  .. figure:: img/slug.png

A slug is the URL friendly version of the title. For example, with the group We Love Maps, the slug would be either We-Love-Maps or We_Love_Maps. When the URL for the group is created, it becomes something like this:

  ``https://exchange.boundlessgeo.io/groups/group/We-Love-Maps``

3. Browse to an image you want to use as a logo for the group.

4. Provide a brief description of the group. Explain briefly why the group was created, who the members are, or what service the group provides.

5. Add an email address. This can be an email used to contact one or all of the group members, such as a mailing list, shared email, or an exchange group.

6. Select the type of access you’d like users to have to the group from the Access menu. The group can be Public, Public (invite-only), or Private.

  .. figure:: img/access.png

7. Add any keywords that may be helpful for users to find your group, or determine if the organization is relevant to their work.

8. Add members to the group by selecting Exchange users from the pull down list, and select either Manager or Member from the Role menu. If adding more than three members, to a group, select the **Add another Group member** link. This will add another row for an additional member.

  .. figure:: img/group-members.png

9. Once all of the group members have been added, click the :guilabel:`Save` button to create the group. This will direct you to the list of existing groups. A notice will display, indicating the group profile was added successfully.

Manage groups
^^^^^^^^^^^^^

Update existing group profiles and modify group members through the Django site.

1. Click **Group profiles** in the Groups menu on the Django administration site Groups menu to open the list of existing groups.

2. Open the Change group profile page for a specific group by selecting on the name of the group you’d like to modify.

From here, you are able to to change the group information, add or remove group members, and change member roles.

To delete a user from a group, click the checkbox under the delete column next to their name.

3. Click the :guilabel:`Save` button when you are finished to save your changes.

Delete  a group
^^^^^^^^^^^^^^^

1. Click **Group profiles** in the Groups menu on the Django administration site Groups menu to open the list of existing groups.

2. Click the checkbox next to the name of the group to be deleted, and select **Delete selected group profiles** in the Action menu, followed by the :guilabel:`Go` button.

  .. figure:: img/delete-group.png

3. Click the :guilabel:`Yes, I’m sure` button to verify your selection. You will be notified that you have **Successfully deleted 1 group profile**.