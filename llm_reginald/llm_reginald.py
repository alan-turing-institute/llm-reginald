import llm

@llm.hookimpl
def register_models(register):
    register(Reginald())


class Reginald(llm.Model):
    model_id = "reginald"

    def execute(self, prompt, stream, response, conversation):
        return ["hello"]
