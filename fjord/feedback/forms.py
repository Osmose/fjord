from django import forms

from fjord.base.forms import EnhancedURLField
from fjord.feedback.config import URL_LENGTH


class URLInput(forms.TextInput):
    """Text field with HTML5 URL Input type."""
    input_type = 'url'


class ResponseForm(forms.Form):
    """Basic response feedback form."""

    # NB: The class 'url' is hard-coded in the Testpilot extension to
    # accommodate pre-filling the field client-side.
    url = EnhancedURLField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'http://', 'class': 'url'}))

    description = forms.CharField(widget=forms.Textarea(), required=True)
    # required=False means this allowed to be False, not that it can
    # be blank.
    happy = forms.BooleanField(required=False, widget=forms.HiddenInput())

    email_ok = forms.BooleanField(required=False)
    email = forms.EmailField(required=False)

    browser_ok = forms.BooleanField(required=False)
    browser_data = forms.CharField(widget=forms.Textarea(), required=False)

    # These are hidden fields on the form which we have here so we can
    # abuse the fields for data validation.
    manufacturer = forms.CharField(required=False, widget=forms.HiddenInput(
        attrs={'class': 'manufacturer'}))
    device = forms.CharField(required=False, widget=forms.HiddenInput(
        attrs={'class': 'device'}))

    def clean_url(self):
        # Truncate the url if it's > URL_LENGTH characters. We truncate rather
        # than use it to validate because it probably doesn't matter if we keep
        # super long urls and we'd rather not error out on the user.
        data = self.cleaned_data['url']
        data = data[:URL_LENGTH]
        return data
