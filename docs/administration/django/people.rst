People
======

The primary use of the People section is to help Exchange admin users manage individual users, and modify their accounts, if necessary. The section allows administrators the ability to change the username, grant account permissions, or edit extended profile data. All new users are created by a system administrator through Auth0.

  .. figure:: img/people.png
  
Change user
-----------

User account information can be modified through the Django Administration site, as well. **Note:** Acccounts using a Boundless Connect login will not have the option to change passwords here. It would need to be done through Connect.

1. Click the **Change** link next to Users on the Django Administration site People menu to open the Change user page.

2. Click the Username for the account to be modified.

  .. figure:: img/people-list.png

3. Modify the user name.

  .. figure:: img/user-name.png

Personal info
-------------

Modifications can be made to the user’s first or last name, and their email address.

  .. figure:: img/personal-info.png

Permissions
-----------

Administrators can establish permissions by selecting the checkbox next to one or all of the available options. 

* Active - Designates whether the user account should be treated as active or inactive. Deselect this instead of deleting accounts.
* Staff Status - Designates whether the user can log into the Django admin site.
* Superuser Status - Designates that the user has all permissions without explicitly assigning them.

  .. figure:: img/user-permissions.png

Groups
------

Groups make it easy for organizations or individuals to share products and projects. Permissions are set by users to designate which groups have access to specific data. Assign users to groups by selecting on an available group, and clicking the right or left arrow to move it to the Chosen groups. 

**Important:** Users are assigned by default to the content_creator and service_manager groups. As a member of the content_creator group, the user is able to upload and create layers, upload documents, and save maps. As a member of the service_manager group, users can register new remote services. These features will be grayed out or unavailable if the user is removed from those groups.

  .. figure:: img/group-perms.png

Select a save option once all changes have been made.

  .. figure:: img/save-options.png