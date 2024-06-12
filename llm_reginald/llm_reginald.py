import llm
import httpx

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
        user_id = ""

        with httpx.Client() as client:
            response = client.post(
                self._direct_message_endpoint(),
                json={"message": message, "user_id": user_id},
                timeout=None
            )
            response.raise_for_status()
            return response.json()['message']
