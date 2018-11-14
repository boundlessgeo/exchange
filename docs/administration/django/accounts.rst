Accounts
========

This section covers how to add, modify and delete Exchange user accounts. All of the options in this section are available through the Account menu on the Django Site administration page.

  .. figure:: img/account-menu.png

Account creation
^^^^^^^^^^^^^^^^

1. To create an Exchange user account, select the Add link next to Accounts.

2. Click the green plus (+) button next to the User list to add another user.

  .. figure:: img/add-account.png

3. Create a username and password that will be remembered by the user. Confirm the password and select the Save button.

4. Select the timezone and primary language for the user from the drop down menus.

5. Click the :guilabel:`Save` button to save the account.

Modify an existing account
^^^^^^^^^^^^^^^^^^^^^^^^^^

Changing a user’s password, setting permissions, and editing their email address can all be completed in the Account section.

Edit user information
*********************

1. Select Accounts in the Account menu, and click on the username whose information you’d like to modify.

2. Click the pencil icon next to the username, and make the changes to the account. When you are finished, click the :guilabel:`Save` button to save your changes.

Within the Change User screen, you can update the following user information:

  * Personal info - The basics
  * User permissions - Designates what type of account the user has, groups the user belongs to
  * Important dates
  * Extended profile information - Organization, location, biography

Edit an email address
*********************

1. Select Email addresses in the Account menu, and click on the user name whose email you’d like to modify.

2. Update the email address, and check the box to display if the email has been verified, and if this is the user’s primary email address.

  .. figure:: img/edit-email.png

3. Click the save button when you are finished, or continue modifying any additional accounts.

Delete a user account
*********************

1. Select Accounts in the Account menu, and check the box next to the user account(s) you want to delete.

2. Select Delete selected accounts in the Action menu, and click the Go button.

  .. figure:: img/delete-account.png

3. Click the Yes, I’m sure button to verify your selection. You will be notified that the account was successfully deleted.

Signup codes
^^^^^^^^^^^^

As an administrator, you are able to invite individuals to try Exchange. When you do this, a signup code is generated. This signup code is used to track trial users in Exchange. From this site, you can modify when the signup code expires, the number of times it can be used, or delete the code itself.

Invite users
************

1. Select Profile in your profile drop down menu, and click Invite User in the lower right corner.

**Note:** While this is not done in Django, you must have the required privileges to invite users.

  .. figure:: img/invite-user.png

2. Type the email address of the person you’d like to invite, and provide an easy to remember username.

3. Click the :guilabel:`Invite User` button when you are finished.

The guest will receive an email notifying them that they have been invited to sign up for an Exchange account.

Signup codes
************

You will need to return to the Django administration site to modify signup codes.

1. Select Signup Codes in the Account menu, and click on the code you’d like to view.

2. Make all necessary changes, and click the Save button. From this screen, you are able to:

  * Modify the number of times the code can be used
  * Set an expiration date for the invitation
  * Add the individual who sent the invitation
  * Add any notes relevant to the invitation or its recipient

  .. figure:: img/change-code.png

To delete the signup code, click the :guilabel:`Delete` button, and select **Yes, I’m sure** to verify your choice.