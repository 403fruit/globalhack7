from flask import current_app
from flask_babel import lazy_gettext


LABELS = {
    "username": lazy_gettext("Username"),
    "category": lazy_gettext("Category"),
    "quantity": lazy_gettext("Quantity"),
    "type": lazy_gettext("Type"),
    "password": lazy_gettext("Password"),
    "repeat_password": lazy_gettext("Repeat Password"),
    "remember_me": lazy_gettext("Remember Me"),
    "submit_sign_in": lazy_gettext("Sign In"),
    "submit": lazy_gettext("Submit"),
    "submit_register": lazy_gettext("Register"),
    "submit_create": lazy_gettext("Create"),
    "email": lazy_gettext("Email"),
    "register": lazy_gettext("Register"),
    "name": lazy_gettext("Name"),
    "phone": lazy_gettext("Phone Number"),
    "secondary_phone": lazy_gettext("Secondary Phone Number"),
    "bio": lazy_gettext("Bio"),
    "description": lazy_gettext("Item Description"),
    "primary_role": lazy_gettext("Primary Role"),
    "language": lazy_gettext("Language"),
    "country": lazy_gettext("Country"),
    "picture": lazy_gettext("Picture"),
    "association": lazy_gettext("Association"),
}
HELP = {
    "picture": lazy_gettext("Upload a picture of yourself to help others get to know you"),
}

# copied from config.json, replace names with native names
LANGUAGE_CHOICES = {
    "en": "English",
    "es": "Español",
    "zh": "汉语",
    "fr": "français",
    "ar": "العربية",
    "vi": "Tiếng Việt"
}


class SUPPORTEDLANGUAGES(object):
    def __iter__(self):
        for key, value in current_app.config.get("SUPPORTED_LANGUAGES", {}).items():
            yield (key, value)


ERROR_MESSAGES = {
    "different_username": lazy_gettext("Please select a different username."),
    "different_email": lazy_gettext("Please select a different email address"),
    "invalid_credentials": lazy_gettext("Invalid username or password."),
    "not_logged_in": lazy_gettext("Must be logged in.")
}

GENERAL_MESSAGES = {
    "registration_success": lazy_gettext("You have successfully registered."),
    "resource_requested": lazy_gettext("The Resource has been successfully requested."),
    "resource_not_requested": lazy_gettext("The Resource was not successfully requested."),
    "resource_save_success": lazy_gettext("You have successfully saved."),
    "resource_fulfilled": lazy_gettext("Your contact info was sent to Requester. Thank you!"),
    "resource_not_fulfilled": lazy_gettext("Your contact info was not sent to Requester"),
    "login_success": lazy_gettext("You have successfully logged in."),
    "logout_success": lazy_gettext("You have successfully logged out.")
}
