import os
from pathlib import Path
from opentelemetry import trace
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError
from config import ASSET_PATH, get_logger, enable_telemetry
from get_product_documents import get_product_documents
from azure.ai.inference.prompts import PromptTemplate
import tiktoken
import time

# initialize logging and tracing objects
logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)

# create a project client using environment variables loaded from the .env file
project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)

# create a chat client we can use for testing
chat = project.inference.get_chat_completions_client()

@tracer.start_as_current_span(name="chat_with_products")
def chat_with_products(messages: list, context: dict = None) -> dict:
    if context is None:
        context = {}

    logger.debug(f"Chat Model: {os.environ['CHAT_MODEL']}")
    documents = get_product_documents(messages, context)

    # do a grounded chat call using the search results
    grounded_chat_prompt = PromptTemplate.from_prompty(Path(ASSET_PATH) / "grounded_chat.prompty")

    system_message = grounded_chat_prompt.create_messages(documents=documents, context=context)

    logger.debug(f"System message parameters: {grounded_chat_prompt.parameters}")
    logger.debug(f"System message: {system_message}")
    logger.debug(f"User messages: {messages}")

    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = sum(len(encoding.encode(m["content"])) for m in messages)
    tokens += sum(len(encoding.encode(m["content"])) for m in system_message)

    logger.debug(f"Input tokens: {tokens}")

    for _ in range(3):  # try up to 3 times
        try:
            # get the chat response
            response = chat.complete(
                model=os.environ["CHAT_MODEL"],
                messages=system_message + messages,
                **grounded_chat_prompt.parameters,
            )
            break  # exit loop if successful
        except HttpResponseError as e:
            if e.status_code == 429:
                logger.warning("Rate limit error, retrying after 60 seconds...")
                time.sleep(60)
            else:
                raise
                    
    logger.info(f"💬 Response: {response.choices[0].message}")

    # Return a chat protocol compliant response
    return {"message": response.choices[0].message, "context": context}

if __name__ == "__main__":
    import logging
    import argparse

    # set logging level to debug when running this module directly
    logger.setLevel(logging.DEBUG)

    # load command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        type=str,
        help="Query to use to search product",
        default="I need a new tent for 4 people, what would you recommend?",
    )
    parser.add_argument(
        "--enable-telemetry",
        action="store_true",
        help="Enable sending telemetry back to the project",
    )

    args = parser.parse_args()
    if args.enable_telemetry:
        enable_telemetry(True)

    # run chat with products
    response = chat_with_products(messages=[{"role": "user", "content": args.query}])