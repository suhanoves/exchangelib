from .common import EWSAccountService, create_folder_ids_element
from ..properties import FolderId
from ..util import create_element, set_xml_value, MNS


class MoveFolder(EWSAccountService):
    """MSDN: https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/movefolder-operation"""

    SERVICE_NAME = "MoveFolder"
    element_container_name = f'{{{MNS}}}Folders'

    def call(self, folders, to_folder):
        from ..folders import BaseFolder
        if not isinstance(to_folder, (BaseFolder, FolderId)):
            raise ValueError(f"'to_folder' {to_folder!r} must be a Folder or FolderId instance")
        return self._elems_to_objs(self._chunked_get_elements(self.get_payload, items=folders, to_folder=to_folder))

    def _elems_to_objs(self, elems):
        for elem in elems:
            if isinstance(elem, (Exception, type(None))):
                yield elem
                continue
            yield FolderId.from_xml(elem=elem.find(FolderId.response_tag()), account=self.account)

    def get_payload(self, folders, to_folder):
        # Takes a list of folders and returns their new folder IDs
        movefolder = create_element(f'm:{self.SERVICE_NAME}')
        tofolderid = create_element('m:ToFolderId')
        set_xml_value(tofolderid, to_folder, version=self.account.version)
        movefolder.append(tofolderid)
        folder_ids = create_folder_ids_element(tag='m:FolderIds', folders=folders, version=self.account.version)
        movefolder.append(folder_ids)
        return movefolder
