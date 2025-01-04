# import time
# import requests

# def get_response_on_device(prompt):
#     """
#     Sends a prompt to the deployed LLM and returns its response.

#     Args:
#         prompt (str): The input prompt to send to the LLM.

#     Returns:
#         str: The response from the LLM.

#     Raises:
#         Exception: If the request to the endpoint fails.
#     """
#     url = "http://34.95.247.215:8000/predict"

#     try:
#         # Send the prompt to the endpoint
#         response = requests.post(url, data=prompt)
        
#         # Raise an exception if the request was not successful
#         response.raise_for_status()
        
#         # Return the response text
#         return response.text

#     except requests.exceptions.RequestException as e:
#         raise Exception(f"Error while getting response from LLM: {e}")


# def test_llm():
#     """
#     Test function to verify LLM responses
#     """
#     test_prompts = [
#         "Tell me a short story about a cat",
#         "What is Python programming?",
#         "Write a haiku about summer"
#     ]
    
#     print("Starting LLM test...\n")
    
#     for i, prompt in enumerate(test_prompts, 1):
#         print(f"\nTest {i}: '{prompt}'\n")
#         print("=" * 50)
        
#         start_time = time.time()
#         response = get_response_on_device(prompt)
#         end_time = time.time()
        
#         if response:
#             print("\n" + "=" * 50)
#             print(f"\nResponse time: {end_time - start_time:.2f} seconds")
#         else:
#             print("\nFailed to get response")
        
#         print("\n" + "-" * 50)


# import unittest
# from unittest.mock import patch, Mock

# def test_get_response_on_device():
#     # Create a sample prompt
#     sample_prompt = "This is a sample prompt."

#     # Mock the requests.post function
#     with patch('requests.post') as mock_post:
#         # Create a mock response object
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_response.text = "This is a sample response."

#         # Set the return value of the mocked requests.post
#         mock_post.return_value = mock_response

#         # Call the function being tested
#         response = get_response_on_device(sample_prompt)

#         # Assert that the response is as expected
#         assert response == "This is a sample response."

#         # Assert that requests.post was called with the correct arguments
#         mock_post.assert_called_once_with(url="http://34.95.247.215:8000/predict", data=sample_prompt)

# if __name__ == '__main__':
#     test_get_response_on_device()



import time
import requests

def get_response_on_device(prompt):
    print("USING DEPLOYED MODEL")
    """
    Sends a prompt to the deployed LLM and returns its response.

    Args:
        prompt (str): The input prompt to send to the LLM.

    Returns:
        str: The response from the LLM.

    Raises:
        Exception: If the request to the endpoint fails.
    """
    url = "http://35.198.59.156:8000/predict"

    try:
        # Send the prompt to the endpoint
        response = requests.post(url, data=prompt)
        
        # Raise an exception if the request was not successful
        response.raise_for_status()
        
        # Return the response text
        return response.text

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error while getting response from LLM: {e}")


def test_llm():
    """
    Test function to verify LLM responses
    """
    test_prompts = [
        "Tell me a short story about a cat",
        "What is Python programming?",
        "Write a haiku about summer"
    ]
    
    print("Starting LLM test...\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest {i}: '{prompt}'\n")
        print("=" * 50)
        
        start_time = time.time()
        response = get_response_on_device(prompt)
        end_time = time.time()
        
        if response:
            print("\n" + "=" * 50)
            print(f"\nResponse time: {end_time - start_time:.2f} seconds")
        else:
            print("\nFailed to get response")
        
        print("\n" + "-" * 50)

# if __name__ == "__main__":
#     test_llm()