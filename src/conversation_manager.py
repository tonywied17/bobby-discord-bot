from src.utils import get_random_max_responses
from src.personality import get_combined_personality, ai_model

class ConversationManager:
    """Manage ongoing conversations in channels."""
    def __init__(self):
        self.active_conversations = {}
        self.triggered_recently = {}

    def start_conversation(self, channel_id, starter_message):
        """Start a new conversation in the channel with the given starter message."""
        max_responses = get_random_max_responses()

        conversation = {
            "messages": [{"role": "user", "content": starter_message}],
            "response_count": 0,
            "max_responses": max_responses,
        }
        self.active_conversations[channel_id] = conversation
        self.triggered_recently[channel_id] = True
        print(f"Starting new conversation in channel {channel_id}. Message: {starter_message}, Max Responses: {max_responses}")

    def append_message(self, channel_id, role, message):
        """Append a new message to the ongoing conversation in the channel."""
        if channel_id in self.active_conversations:
            self.active_conversations[channel_id]["messages"].append({"role": role, "content": message})
            if role == "assistant":
                self.active_conversations[channel_id]["response_count"] += 1
                response_count = self.active_conversations[channel_id]["response_count"]
                max_responses = self.active_conversations[channel_id]["max_responses"]
                print(f"Assistant response {response_count} out of {max_responses}")

    def is_conversation_active(self, channel_id):
        """Check if the conversation in the channel is still active."""
        conversation = self.get_conversation(channel_id)
        if conversation:
            return conversation["response_count"] < conversation["max_responses"]
        return False

    def get_conversation(self, channel_id):
        """Get the ongoing conversation in the channel."""
        return self.active_conversations.get(channel_id)

    def end_conversation(self, channel_id):
        """End the ongoing conversation in the channel."""
        if channel_id in self.active_conversations:
            print(f"Ending conversation in channel {channel_id}.")
            del self.active_conversations[channel_id]
            self.triggered_recently[channel_id] = False

    def can_trigger_conversation(self, channel_id):
        """Check if a new conversation can be triggered in the channel."""
        if channel_id in self.triggered_recently and self.triggered_recently[channel_id]:
            return False
        return True

    async def handle_conversation(self, channel, starter_message):
        """Handle the logic for starting and continuing conversations."""
        channel_id = channel.id

        #* Start a new conversation if one doesn't exist
        if channel_id not in self.active_conversations:
            self.start_conversation(channel_id, starter_message)
            response = await self.generate_ai_response([{"role": "user", "content": starter_message}])
            if response:
                await channel.send(response)
                self.append_message(channel_id, "assistant", response)
            return

        #* Continue the ongoing conversation
        conversation = self.get_conversation(channel_id)
        if self.is_conversation_active(channel_id):
            self.append_message(channel_id, "user", starter_message)
            response = await self.generate_ai_response(conversation["messages"])
            if response:
                await channel.send(response)
                self.append_message(channel_id, "assistant", response)
        else:
            #* End the current conversation and start a new one
            self.end_conversation(channel_id)
            self.start_conversation(channel_id, starter_message)
            response = await self.generate_ai_response([{"role": "user", "content": starter_message}])
            if response:
                await channel.send(response)
                self.append_message(channel_id, "assistant", response)

    async def generate_ai_response(self, messages):
        """Generate an AI response using the combined personality and the given messages."""
        try:
            combined_personality = get_combined_personality()
            formatted_messages = [{"role": "system", "content": combined_personality}] + messages
            response = ai_model.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=formatted_messages,
                max_tokens=250,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return None
        
    async def handle_message_edit(self, channel, edited_message):
        """Handle the logic for edited messages in ongoing conversations."""
        channel_id = channel.id
        if channel_id in self.active_conversations:
            conversation = self.get_conversation(channel_id)
            if self.is_conversation_active(channel_id):
                response = await self.generate_ai_response(conversation["messages"])
                if response:
                    await channel.send(response)
                    self.append_message(channel_id, "assistant", response)