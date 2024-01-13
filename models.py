from mongoengine import Document, StringField, DictField, ListField, EmbeddedDocumentField, EmbeddedDocument

class Template(Document):
    template_id = StringField(required=True, unique=True)
    template_body = StringField(required=True)

class Message(Document):   
    template_id = StringField(required=True)   
    replacement_dict = DictField(required=True)
    sender_list = ListField(required=True)       

class Notify(Document):
    template_id = StringField(required=True)
    template_body = StringField(required=True)
    sender_list = ListField(required=True)
    # end_status = StringField(required=True)