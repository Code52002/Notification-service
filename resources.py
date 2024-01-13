from flask import request
from flask_restful import Resource
from models import Template, Message
import json

# sender_data = [""]    

class TemplateResource(Resource):

    def get(self, template_id=None):
     try:
        if template_id:
            temp_body = Template.objects(template_id=template_id).first()
            if temp_body:
                return {'status': 'success', 'template_id': temp_body.template_id,'template_body': temp_body.template_body}
            return {'status': 'error', 'message': 'Template not found'}, 404
        
        else:
                all_templates = Template.objects.all()
                result = []
                for temp_body in all_templates:
                    result.append({
                        'template_id': temp_body.template_id,
                        'template_body': temp_body.template_body,
                    })
                return {'status': 'success', 'messages': result}     #list of dictionaries is displayed in the result if no template id is entered
        
     except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500
    

    def post(self):
        data = request.get_json()
        template_id = data.get('template_id')
        template_body = data.get('template_body')

        if not template_body or not template_id:
            return {'status':'error','message': 'The template is not created'},400
        
        template = Template(template_id=template_id,template_body=template_body)
        template.save()
        return {'status':'success','message':'The template is created successfully'},201



class MessageResource(Resource):

    def get(self, template_id):         #list of dictionaries is displayed in the result
        try:
            messages = Message.objects(template_id=template_id)
            if messages:
                result = []
                for msg_body in messages:
                    result.append({
                        'template_id': msg_body.template_id,
                        'replacement_dict': msg_body.replacement_dict,
                        'sender_list': msg_body.sender_list
                    })
                return {'status': 'success', 'messages': result}

            return {'status': 'error', 'message': 'No templates found for the given template_id'}, 404

        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500


    def post(self):
        data = request.get_json()
        template_id = data.get('template_id')
        replacement_dict = data.get('replacement_dict')
        sender_list = data.get('sender_list')

        if not template_id or not replacement_dict or not sender_list:
            return {'status':'error','message':'Incomplete message data entry'},400

        message = Message(template_id=template_id,replacement_dict=replacement_dict,sender_list=sender_list)
        message.save()
        return {'status':'success','message':'Message sent'},201
    

class NotifyResource(Resource):

    def get(self,template_id):
        try:
            if template_id:
                messages = Message.objects(template_id=template_id)
                template = Template.objects(template_id=template_id).first()

            if messages and template_id:
                score = []

                if not template:
                      return {'status': 'error', 'message': 'Template not found for the given template_id'}, 404
                
                for msg_body in messages:
                    template_body = template.template_body.format(**msg_body.replacement_dict)
                    score.append({
                        "template_id":template["template_id"],
                        "template_body":template_body,
                        "sender_detail":msg_body["sender_list"],
                        "end_status":"pending"
                    })

                return {'status': 'success', 'messages': score},201

            return {'status': 'error', 'message': 'No templates found for the given template_id'}, 404
        

        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500



