from django import forms

from apps.upload.models import UploadFolder
from apps.upload.services.storage.base import upload_and_unzip_folder
from apps.upload.services.services import file_dir_by_created

from apps.core.system import get_dir_content
from apps.core.utils import get_media_url, get_file_from_nested_folder


class UploadFolderForm(forms.ModelForm):
    all_files = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 10, "cols": 100, "readonly": True})
    )

    class Meta:
        model = UploadFolder
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            instance_dir = file_dir_by_created(self.instance.created)
            self.initial["all_files"] = "\n".join([
                get_media_url(path, True) for path in get_file_from_nested_folder(instance_dir)
            ])

    def clean(self):
        cleaned_data = super().clean()
        try:
            upload_and_unzip_folder(cleaned_data.get("folder_path"))
        except Exception:
            raise forms.ValidationError(
                "File is not .zip file. "
                "This file may not be compressed using the standard algorithm of the Zip format."
            )
