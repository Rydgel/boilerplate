from flask_admin.contrib.sqla import ModelView
from wtforms import validators, PasswordField
from ..models import User


class UserAdmin(ModelView):
    # Don't display the password on the list of Users
    column_exclude_list = list = ('password',)
    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password', [validators.DataRequired()])
        return form_class

    def get_edit_form(self):
        form = self.get_form()
        form.password2 = PasswordField('New Password')
        return form

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = User.hashed_password(model.password2)
