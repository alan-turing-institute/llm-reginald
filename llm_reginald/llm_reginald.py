import llm
import httpx
import uuid

@llm.hookimpl
def register_models(register):
    register(Reginald())


class Reginald(llm.Model):
    model_id = "reginald"
    can_stream = False

    default_host = "http://localhost:8000"

    def _direct_message_endpoint(self, hostname=None):
        if hostname is None:
            hostname = self.default_host

        return hostname + "/direct_message"

    def execute(self, prompt, stream, response, conversation):

        message = prompt.prompt

        # Reginald keeps a separate conversation history for each
        # "user_id".  If 'conversation' is None (or doesn't have the
        # user_id logged) start a new conversation by minting a new
        # user_id history.  Otherwise, extract the logged user_id to
        # continue that conversation.

        try:
            user_id = conversation.responses[0].response_json['user_id']
        except (TypeError, AttributeError, KeyError, IndexError) as e:
            user_id = str(uuid.uuid4().int)

        with httpx.Client() as client:
            reginald_reply = client.post(
                self._direct_message_endpoint(),
                json={"message": message, "user_id": user_id},
                timeout=None
            )

        reginald_reply.raise_for_status()
        yield reginald_reply.json()['message']

        response.response_json = {'user_id': user_id}
