from TyMessageSender import TyMessageSender


class MetaDataConverter:
    def __init__(self):
        self.metaData = {
            "titles": [],
            "identifiers": [],
            "experimental_identifier": "",
            "resource_type": "",
            "descriptions": [],
            "creators": [],
            "created_at": "",
            "updated_at": "",
            "filesets": [],
            "instrument": [],
            "experimental_methods": [],
            "specimens": [],
            "custom_properties": [],
        }

    def setTitle(self, title=""):
        titles = self.metaData["titles"]
        for i in range(len(titles)):
            if titles[i]["title"] == title:
                return 1
        dictTitle = {"title": title}
        self.metaData["titles"] = dictTitle

    def setIdentifiers(self, identifier="", experimentID=""):
        identifiers = []
        identifiers.append({"identifier": identifier})
        identifiers.append({"identifier": experimentID})
        self.metaData["identifiers"] = identifiers
        self.metaData["experiment_identifier"] = experimentID

    def resource_type(self, resourceType="dataset"):
        self.metaData["resource_type"] = resourceType

    def setDescriptions(self, description=""):
        descriptions = []
        descriptions.append({"description": description})
        self.metaData["descriptions"] = descriptions

    def setCreators(
        self, name="", affiliation="", email="", identifier="", identifierType=""
    ):
        creators = self.metaData["creators"]
        for i in range(len(creators)):
            if creators[i]["name"] == name:
                return 1
        creator = {}
        creator["name"] = name
        creator["affiliation"] = affiliation
        creator["email"] = email
        creator["identifier"] = identifier
        creator["identifier_type"] = identifierType
        creators.append(creator)
        self.metaData["creators"] = creators
        return 0

    def setCreated_at(self, date="", current=""):
        self.metaData["created_at"] = date
        if current == "":
            self.metaData["updated_at"] = date
        self.metaData["updated_at"] = current

    def setFilesets(self, filename="", description="", status_valid=False):
        filesets = self.metaData["filesets"]
        for i in range(len(filesets)):
            if filesets[i]["filename"] == filename:
                return 1
        fileset = {}
        fileset["filename"] = filename
        fileset["description"] = description
        fileset["status_valid"] = status_valid
        filesets.append(fileset)
        self.metaData["filesets"] = filesets
        return 0

    def setInstrument(self, name="", identifier="", description="", instrumentType=""):
        instruments = self.metaData["instrument"]
        for i in range(len(instruments)):
            if instruments[i]["name"] == name:
                return 1
        instrument = {}
        instrument["name"] = name
        instrument["identifier"] = identifier
        instrument["instrument_type"] = instrumentType
        instrument["description"] = description
        instruments.append(instrument)
        self.metaData["instrument"] = instruments
        return 0

    def setExperimentalMethods(self, category="", description=""):
        experimental_methods = self.metaData["experimental_methods"]
        experimental_method = {}
        experimental_method["category_description"] = category
        experimental_method["description"] = description
        experimental_methods.append(experimental_method)
        self.metaData["experimental_methods"] = experimental_methods
        return 0

    def setSpecimens(self, name="", identifier="", description=""):
        specimens = self.metaData["specimens"]
        for i in range(len(specimens)):
            if specimens[i]["name"] == name:
                return 1
        specimen = {}
        specimen["name"] = name
        specimen["identifier"] = identifier
        specimen["description"] = description
        specimens.append(specimen)
        self.metaData["specimens"] = specimens
        return 0

    def setCustomProperties(self, key="", value=""):
        custom_properties = self.metaData["custom_properties"]
        for i in range(len(custom_properties)):
            if custom_properties[i]["key"] == key:
                return 1
        custom_property = {}
        custom_property["key"] = key
        custom_property["value"] = value
        custom_properties.append(custom_property)
        self.metaData["custom_properties"] = custom_properties
        return 0

    def getMetaDataDictionary(self):
        return self.metaData

    def set_URL_To_Diamond(self, url):
        self.url_To_Diamond = url

    def get_Meta_Data_From_Diamond(self, usageID, url=""):
        if url != "":
            self.url_To_Diamond = url
        message_Sender = TyMessageSender(self.url_To_Diamond)
        metaData = message_Sender.sendRequestGetMetaData(usageID)
        return metaData
