import asyncio
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from app.core.config import DEFAULT_BACKBOARD_ASSISTANT_ID
from app.services.assistant_service import (
    create_document_assistant,
    create_thread_for_assistant,
    send_message_to_thread,
    upload_document_to_assistant,
    wait_for_document_indexing,
)

load_dotenv()

BACKBOARD_API_KEY = os.getenv("BACKBOARD_API_KEY")
BASE_URL = "https://app.backboard.io/api"
DOCUMENT_PATH = Path("data/documents/cognito-dg-pages.pdf")


def post_message_raw(thread_id: str, content: str, web_search=None, memory=None):
    if not BACKBOARD_API_KEY:
        raise ValueError("BACKBOARD_API_KEY is missing from .env")

    headers = {
        "X-API-Key": BACKBOARD_API_KEY,
    }

    payload = {
        "content": content,
    }

    if web_search is not None:
        payload["web_search"] = web_search

    if memory is not None:
        payload["memory"] = memory

    response = requests.post(
        f"{BASE_URL}/threads/{thread_id}/messages",
        headers=headers,
        json=payload,
        timeout=60,
    )

    print(f"\nHTTP {response.status_code}")
    print("Payload sent:", payload)

    response.raise_for_status()
    return response.json()


async def ensure_assistant():
    if DEFAULT_BACKBOARD_ASSISTANT_ID:
        print(f"Using existing assistant_id: {DEFAULT_BACKBOARD_ASSISTANT_ID}")
        return DEFAULT_BACKBOARD_ASSISTANT_ID

    assistant = await create_document_assistant(
        name="Challenge 4 Assistant",
        system_prompt=(
            "You are a helpful assistant. "
            "Use web search for current information when enabled. "
            "Remember useful user details when memory is enabled."
        ),
    )

    assistant_id = getattr(assistant, "assistant_id", None) or getattr(assistant, "id", None)

    print("Created assistant.")
    print(f"assistant_id = {assistant_id}")
    print("Put this real value into DEFAULT_BACKBOARD_ASSISTANT_ID in your .env")

    return assistant_id


async def maybe_upload_document(assistant_id: str):
    if not DOCUMENT_PATH.exists():
        print(f"Document not found, skipping upload: {DOCUMENT_PATH}")
        return

    print(f"Uploading document: {DOCUMENT_PATH}")
    document = await upload_document_to_assistant(assistant_id, str(DOCUMENT_PATH))

    document_id = getattr(document, "document_id", None) or getattr(document, "id", None)
    print(f"Uploaded document_id = {document_id}")

    if document_id:
        print("Waiting for indexing...")
        status = await wait_for_document_indexing(document_id)
        print(f"Document indexed. status = {status.status}")


async def seed_memories(assistant_id: str, memories: list[str]):
    print("\n=== SEED MEMORIES ===")

    for i, memory_text in enumerate(memories, start=1):
        thread = await create_thread_for_assistant(assistant_id)
        print(f"\n[{i}] thread_id = {thread.thread_id}")
        print(f"Seeding memory: {memory_text}")

        result = post_message_raw(
            thread_id=thread.thread_id,
            content=memory_text,
            memory="Auto",
        )

        print("Saved response:")
        print(result["content"])



async def test_step_1_web_search(assistant_id: str):
    print("\n=== STEP 1: WEB SEARCH ENABLED ===")
    thread = await create_thread_for_assistant(assistant_id)
    print(f"thread_id = {thread.thread_id}")

    reply = await send_message_to_thread(
        thread_id=thread.thread_id,
        content="What are the latest developments in AI?",
        web_search="auto",
        stream=True,
    )

    print("\nAssistant reply:")
    print(reply)


async def test_step_2_memory_raw_http(assistant_id: str):
    print("\n=== STEP 2: MEMORY ENABLED (RAW HTTP) ===")

    thread_a = await create_thread_for_assistant(assistant_id)
    print(f"thread_a = {thread_a.thread_id}")

    result_a = post_message_raw(
        thread_id=thread_a.thread_id,
        content="I prefer Python over JavaScript for backend development.",
        memory="Auto",
    )

    print("\nRaw response after memory save:")
    print(result_a)

    thread_b = await create_thread_for_assistant(assistant_id)
    print(f"\nthread_b = {thread_b.thread_id}")

    result_b = post_message_raw(
        thread_id=thread_b.thread_id,
        content="What backend language do I prefer?",
        memory="Auto",
    )

    print("\nRaw response in new thread:")
    print(result_b)


async def test_step_3_list_all_memories(assistant_id: str):
    print("\n=== STEP 3: List All Memories ===")

    
    response = requests.get(
        f"https://app.backboard.io/api/assistants/{assistant_id}/memories",
        headers={"X-API-Key": BACKBOARD_API_KEY}
)

    memories = response.json()
    for memory in memories["memories"]:
        print(f"Memory: {memory['content']}")


async def test_step_4_search_memories(assistant_id: str):
    print("\n=== STEP 4: Search Memories ===")

    
    response = requests.post(
        f"https://app.backboard.io/api/assistants/{assistant_id}/memories/search",
        headers={"X-API-Key": BACKBOARD_API_KEY},
        json={"query": "programming language preferences", 
              "limit": 5
              }
                )
    results = response.json()
    print(f"Found {results['total_count']} matching memories")
    for memory in results["memories"]:
        print(f"[{memory['score']:.2f}] {memory['content']}")



async def print_memories_id(assistant_id: str):
    print("\n=== Print all the Memories id's ===")

    
    response = requests.get(
        f"https://app.backboard.io/api/assistants/{assistant_id}/memories",
        headers={"X-API-Key": BACKBOARD_API_KEY}
)

    memories = response.json()
    for memory in memories["memories"]:
        print(f"Memory: {memory['id']}")



async def test_step_5_update_memory(assistant_id: str, memory_id : str, content : str): 
    response = requests.put(
        f"https://app.backboard.io/api/assistants/{assistant_id}/memories/{memory_id}",
        headers={"X-API-Key": BACKBOARD_API_KEY},
        json={
            "content": content
            }
                            )



async def test_step_6_delete_memory(assistant_id: str, memory_id : str): 
    print(f"\nTest6 === Deleting memory {memory_id} ===")

    response = requests.delete(
        f"https://app.backboard.io/api/assistants/{assistant_id}/memories/{memory_id}",
        headers={
            "X-API-Key": BACKBOARD_API_KEY
                }
                                )


async def test_step_7_memories_stats(assistant_id: str):
    print("\nTest7 === check memories stats")

    response = requests.get(
        f"https://app.backboard.io/api/assistants/{assistant_id}/memories",
        headers={"X-API-Key": BACKBOARD_API_KEY},
        params={"page": 1, "page_size": 100},
        timeout=60,
    )

    print("HTTP", response.status_code)
    print(response.text)
    response.raise_for_status()

    data = response.json()
    print("Total memories:", data["total_count"])
    print("Returned on this page:", len(data["memories"]))

async def main():
    assistant_id = await ensure_assistant()

    if not assistant_id:
        raise RuntimeError("Could not determine assistant_id.")
    
    # await maybe_upload_document(assistant_id)
    # await test_step_1_web_search(assistant_id)

    # # run this only when you really want to add new memories
    # await seed_memories(
    #     assistant_id,
    #     [
    #         "I like concise answers.",
    #         "I am building an identity-aware assistant for the MLH hackathon.",
    #     ],
    # )
    # await test_step_2_memory_raw_http(assistant_id)
    await test_step_3_list_all_memories(assistant_id)
    # await print_memories_id(assistant_id)
    # await test_step_4_search_memories(assistant_id)
    # await test_step_5_update_memory(assistant_id, "9bd40bf1-c3ce-4340-aede-797c0fb3d68f", "The user is aim to grow as software developer/engineer")
    # await test_step_6_delete_memory(assistant_id, " 43e1dfd3-6ea8-4b8c-83de-892e86f09be8")
    # await test_step_3_list_all_memories(assistant_id)
    # memories_ids_to_del = [
    #     "43e1dfd3-6ea8-4b8c-83de-892e86f09be8",
    #     "c90a9208-eba2-46c1-a6de-3b8c97cbc07b",
    #     "3ae57599-ebec-44fc-89e8-856811a420ad",
    #     "c1db9a99-073b-45c4-af03-c02ae157431e",
    #     "34abaeec-029f-4647-832d-e6229d56b040",
    #     "b9945727-5274-4188-9fb1-e0d97bd1ee28"
    #                         ]
    # for memory_id in memories_ids_to_del:
    #     await test_step_6_delete_memory(assistant_id, memory_id)
    
    # await test_step_3_list_all_memories(assistant_id)
    await test_step_7_memories_stats(assistant_id)




if __name__ == "__main__":
    asyncio.run(main())