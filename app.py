from flask import Flask
from flask_restful import Api 
from flask_mongoengine import MongoEngine
from resources import TemplateResource, MessageResource, NotifyResource

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'notification_db',
    'host': 'mongodb://localhost:27017',
}
db = MongoEngine(app)
api = Api(app)

api.add_resource(TemplateResource, '/notificationservice/template','/notificationservice/template/<string:template_id>')
api.add_resource(MessageResource, '/notificationservice/message','/notificationservice/message/<string:template_id>')
api.add_resource(NotifyResource, '/notificationservice/notify','/notificationservice/notify/<string:template_id>')

if __name__ == '__main__':
    app.run(debug=True)