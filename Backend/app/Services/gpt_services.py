import openai
import re
import random
import os
from dotenv import load_dotenv



 #Function to detect language
def detect_language(code):
    """
    Detects the programming language of the provided code using GPT.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code language detection assistant."},
                {"role": "user", "content": f"Identify the programming language of the following code:\n\n{code}\n\nJust provide the language name, nothing else."}
            ],
            max_tokens=10,
            temperature=0,
        )
        result = response.choices[0].message['content'].strip()
        print(f"Detected language: {result}")
        return result

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error detecting language"



def filter_dataset_by_language(dataset, language):
    """
    Filters a dataset by language.
    """
    return [entry for entry in dataset if entry['lang'].lower() == language.lower()]


def filter_dataset_by_tags(dataset, tags):
    """
    Filters the dataset to include entries that have matching tags in their 'Tags' field.
    """
    filtered_examples = []
    for entry in dataset['train']:
        entry_tags = entry.get('meta_data', {}).get('Tags', [])
        entry_tags_lower = [tag.lower() for tag in entry_tags]
        if any(tag in entry_tags_lower for tag in tags):
            filtered_examples.append(entry)
    return filtered_examples


def generate_tags(code):
    """
    Uses GPT to generate tags for the given code snippet.
    """
    prompt = f"Please generate relevant tags for the following code snippet:\n\n{code}\n\nProvide the tags as a comma-separated list. Make sure you detect the programming language as one of the tags."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.7,
    )
    tags_text = response.choices[0].message.content.strip()
    return [tag.strip() for tag in tags_text.split(',')]


def wrap_code_snippet(user_prompt):
    """
    Wraps the user prompt in `<pre><code>` tags if not already wrapped.
    """
    code_snippet = extract_code_snippet(user_prompt)
    if not code_snippet:
        return f"<pre><code>\n{user_prompt.strip()}\n</code></pre>"
    return user_prompt


def extract_code_snippet(user_prompt):
    """
    Extracts the code snippet from the user prompt.
    """
    match = re.search(r'<pre><code>(.*?)</code></pre>', user_prompt, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r'```.*?\n(.*?)```', user_prompt, re.DOTALL)
    if match:
        return match.group(1).strip()
    return user_prompt.strip()


# Few-shot Prompt Generation
def create_few_shot_prompt_with_custom_code_and_tags(dataset, user_prompt, num_examples=2):
    """
    Creates a few-shot prompt using examples filtered by tags and appends a custom user-provided prompt.
    """
    # response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a code language detection assistant."},
    #             {"role": "user", "content": f"Identify the programming language of the following code:\n\n{code}\n\nJust provide the language name, nothing else."}
    #         ],
    #         max_tokens=10,
    #         temperature=0,
    #     )
    user_prompt = wrap_code_snippet(user_prompt)

    # Generate tags from user prompt
    code_snippet = extract_code_snippet(user_prompt)
    tags = generate_tags(code_snippet)

    # Filter dataset based on tags
    filtered_examples = filter_dataset_by_tags(dataset, tags)

    # Use random examples if no matching tags
    if not filtered_examples:
        filtered_examples = random.sample(list(dataset['train']), num_examples)

    # Select examples from filtered dataset
    examples = []
    for i in range(min(num_examples, len(filtered_examples))):
        entry = filtered_examples[i]
        examples.append({'prompt': entry['prompt'], 'response': entry['response']})

    # Build the few-shot prompt
    prompt_text = "You are an expert in software engineering tasked with providing actionable code review. Below are some examples:\n\n"
    for example in examples:
        prompt_text += f"PROMPT:\n{example['prompt']}\nRESPONSE:\n{example['response']}\n\n"

    prompt_text += f"PROMPT:\n{user_prompt}\nRESPONSE:\n"
    return prompt_text


def construct_messages(example, user_code):
    """
    Constructs a set of messages for GPT to analyze security vulnerabilities in the provided code.
    """
    messages = [{"role": "system", "content": "You are an AI assistant that identifies and explains security vulnerabilities in code and suggests improvements."}]

    # Include example if available
    if example:
        example_user_code = example['rejected']
        example_response = f"The provided code has a vulnerability: {example['vulnerability']}\n\nTo fix this issue, you can modify your code as follows:\n{example['chosen']}"
        messages.append({"role": "user", "content": f"Please review the following code for security vulnerabilities:\n\n{example_user_code}"})
        messages.append({"role": "assistant", "content": example_response})

    # Add the user's code
    messages.append({"role": "user", "content": f"Please review the following code for security vulnerabilities:\n\n{user_code}"})

    return messages


# GPT Generation Functions
def generate_optimized_code(dataset, prompt: str, max_tokens: int, temperature: float, top_p: float, num_examples: int) -> str:
    """
    Generates optimized code using GPT after preprocessing the input.
    """
    print(prompt)
    # Create a few-shot prompt
    few_shot_prompt = create_few_shot_prompt_with_custom_code_and_tags(dataset, prompt, num_examples)

    # Call GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": few_shot_prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message['content'].strip()


def analyze_code_security(dataset, code: str, max_tokens: int, temperature: float, top_p: float) -> str:
    """
    Analyzes code for security vulnerabilities using GPT after preprocessing.
    """

    # Detect language

    detected_language = detect_language(code)
    
    # Filter dataset by language
    filtered_dataset = filter_dataset_by_language(dataset, detected_language)

    # Select example
    example = filtered_dataset[0] if filtered_dataset else None
    print(example)

    # Construct messages
    messages = construct_messages(example, code)

    # Call GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message['content'].strip()
