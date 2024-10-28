import unittest
from unittest.mock import patch
from api.llm_api import LLMApi  # Ensure the import is correct

class LLMApiTest(unittest.TestCase):
    """Test class for the LLMApi class, which tests functions to interact with the Ollama API model."""

    @patch('ollama.pull')  # Mock for the pull method
    def test_add_model(self, mock_pull):
        """Tests the add_model method of LLMApi.

        Ensures that the ollama.pull method is called with the correct model name.
        """
        api = LLMApi()
        model_name = "example_model"

        api.add_model(model_name)

        # Check that the pull method was called with the correct argument
        mock_pull.assert_called_once_with(model_name)

    @patch('ollama.delete')  # Mock for the delete method
    def test_remove_model(self, mock_delete):
        """Tests the remove_model method of LLMApi.

        Ensures that the ollama.delete method is called with the correct model name.
        """
        api = LLMApi()
        model_name = "example_model"

        api.remove_model(model_name)

        # Check that the delete method was called with the correct argument
        mock_delete.assert_called_once_with(model_name)

    @patch('ollama.list')  # Mock for the list method
    def test_list_available_models(self, mock_list):
        """Tests the list_available_models method of LLMApi.

        Ensures that the return value contains a list of models that matches the expected structure.
        """
        api = LLMApi()
        mock_list.return_value = {'models': [{'name': 'llama3.2:1b', 'model': 'llama3.2', 'modified_at': '2024-01-01T00:00:00Z', 'size': 123456789, 'digest': 'abcdefg', 'details': {}}]}

        models = api.list_available_models()

        # Check that the return value has the expected structure
        self.assertIn('models', models)
        self.assertIsInstance(models['models'], list)
        self.assertGreater(len(models['models']), 0)

    @patch('ollama.chat')  # Mock for the chat method
    def test_get_response(self, mock_chat):
        """Tests the get_response method of LLMApi.

        Ensures that the ollama.chat method is called with the correct arguments
        and that the returned response matches the expected answer.
        """
        api = LLMApi()
        model_name = "example_model"
        message_content = "Hello, how are you?"
        mock_chat.return_value = {"message": {"content": "I'm fine, thank you!"}}

        response = api.get_response(model_name, message_content)

        # Check that the chat method was called with the correct arguments
        mock_chat.assert_called_once_with(model=model_name, messages=[{"role": "user", "content": message_content}])
        
        # Check that the response is correct
        self.assertEqual(response, "I'm fine, thank you!")

if __name__ == '__main__':
    unittest.main()
