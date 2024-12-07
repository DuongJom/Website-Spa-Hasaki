import json
from datetime import datetime as dt
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Messenger, Customer, Employee

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.customer_id = self.scope['url_route']['kwargs']['id']
        self.roomGroupName = f"group_chat_1"
        await self.channel_layer.group_add(
                self.roomGroupName,
                self.channel_name
            )
        await self.accept()
        messages = await self.get_message_from_db(self.customer_id)
        # Send all messages to the WebSocket client
        await self.send(text_data=json.dumps({
            'messages': messages
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        time = text_data_json["time"]

        # Send message to the group
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "time": time
        })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        sender = await self.get_user_name(username)
        time = event["time"]
        is_customer,user = await self.get_user(username=username)
        if user:
            await self.save_message_to_db(user=user, message=message, time=time, is_customer=is_customer)
        await self.send(text_data=json.dumps({
            "message": message, 
            "username": username,
            "sender": sender,
            "time": time
            }
        ))

    # Helper function to save message to the database (Django ORM)
    @sync_to_async
    def save_message_to_db(self, user, message, time, is_customer):
        customer, employee = None, None
        if is_customer:
            customer = user
        elif not is_customer and user:
            employee = user
        message = Messenger(
            customer=Customer.objects.get(customer_id=self.customer_id), 
            employee=employee if employee else Employee.objects.filter(employee_id=1).first(),
            message_id=1,
            message=message,
            is_sent_from_customer=(0 if customer else 1),
            sent_time=dt.strptime(time, "%Y-%m-%d %H:%M"),
            is_resolved=0)
        message.save()

    @sync_to_async
    def get_user_name(self, username):
        customer = Customer.objects.filter(email=username).first()
        if customer:
            return customer.customer_name
        
        employee = Employee.objects.filter(email=username).first()
        if employee:
            return employee.employee_name
        return "Người dùng ẩn danh"
            
    @sync_to_async
    def get_message_from_db(self, customer_id):
        customer = Customer.objects.filter(customer_id=customer_id).first()
        messages = None
        if customer:
            messages = Messenger.objects.filter(customer_id=customer.customer_id)

        employee = Employee.objects.filter(email=self.user.username).first()
        message_list = [
            {
                "username": customer.email if message.is_sent_from_customer == 0 else self.user.username,
                "sender": customer.customer_name if message.is_sent_from_customer == 0 else (employee.employee_name if employee else ""), 
                "message": message.message, 
                "time": message.sent_time.strftime('%Y-%m-%d %H:%M'),
                "is_sent_customer": message.is_sent_from_customer
            } 
            for message in messages
        ]
        return message_list
    
    @sync_to_async
    def get_user(self, username):
        customer = Customer.objects.filter(email=username).first()
        if customer:
            return True,customer
        employee = Employee.objects.filter(email=username).first()
        if employee:
            return False,employee
        return False,None