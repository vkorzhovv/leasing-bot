import dicttoxml
from import_export.formats.base_formats import TextFormat


class XML(TextFormat):
    def get_title(self):
        return 'xml'

    def is_binary(self):
        """
        Returns if this format is binary.
        """
        return False

    def get_extension(self):
        """
        Returns extension for this format files.
        """
        return ".xml"

    def get_content_type(self):
        return 'application/xml'

    def can_import(self):
        return False

    def can_export(self):
        return True

    def export_data(self, dataset, **kwargs):
        """
        Returns format representation for given dataset.
        """
        kwargs.setdefault('attr_type', False)
        return dicttoxml.dicttoxml(dataset.dict)
