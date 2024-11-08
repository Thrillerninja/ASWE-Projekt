import ollama


class LLMApi:
    """This class acts as API to chat with API-models. It uses ollama's REST-API.
    To use this class, a local instance of ollama needs to be running.
    The easiest way to get a local instance is to run ollama in a docker container.
    You can use this command to quickly get ollama up and running:

    docker run -d --name ollama -p 11434:11434 -v ollama_storage:/root/.ollama ollama/ollama:latest

    This command also attaches a volume to the container so your downloaded models are not lost on shutdown.
    """

    def add_model(self, model: str):
        """Adds a model to the list of available models in ollama.
        The model will be downloaded (be wary of long downloads!).
        This function can have unexpected results.
        Using the terminal inside the container is generally better.

        Args:
            model (str): name of the model as string (check ollama website for correct nomenclature)
        """
        ollama.pull(model)

    def remove_model(self, model: str):
        """Removes a model from the list of available models in ollama.
        The model will be deleted.
        This function can have unexpected results.
        Using the terminal inside the container is generally better.

        Args:
            model (str): name of the model as string (check ollama website for correct nomenclature)
        """
        ollama.delete(model)

    def list_available_models(self):
        """Returns a list of all available models in your ollama container.

        Returns:
            dict: A dictionary with a single key, 'models', which maps to a list of dictionaries.
            Each dictionary in the list represents a model and contains the following fields:
                - 'name' (str): The model's name and version, e.g., 'llama3.2:1b'.
                - 'model' (str): The model identifier, typically the same as 'name'.
                - 'modified_at' (str): ISO 8601 timestamp indicating the last modification date.
                - 'size' (int): Size of the model in bytes.
                - 'digest' (str): A unique hash representing the model's contents.
                - 'details' (dict): Additional model information with the following keys:
                    - 'parent_model' (str): Parent model identifier, if applicable.
                    - 'format' (str): The format of the model file, e.g., 'gguf'.
                    - 'family' (str): The family this model belongs to, e.g., 'llama'.
                    - 'families' (list[str]): List of family names associated with the model.
                    - 'parameter_size' (str): Number of parameters, e.g., '1.2B'.
                    - 'quantization_level' (str): Quantization level applied to the model, e.g., 'Q8_0'.
        """
        return ollama.list()

    def get_response(self, model: str, message_content: str):
        """Send a message to ollama and get the response.

        Args:
            model (str): name of the model as string (check ollama website for correct nomenclature)
            message_content (str): message to send to ollama as string

        Returns:
            str: only the parsed answer gets returned as a string
        """
        response = ollama.chat(
            model=model, messages=[{"role": "user", "content": message_content}]
        )
        return response["message"]["content"]
