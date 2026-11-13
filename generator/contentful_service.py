
import requests
from django.conf import settings


SPACE_ID = settings.CONTENTFUL_SPACE_ID
ENVIRONMENT = settings.CONTENTFUL_ENVIRONMENT
CONTENTFUL_MANAGEMENT_TOKEN = settings.CONTENTFUL_MANAGEMENT_TOKEN

BASE_URL = (
    f"https://api.contentful.com/spaces/{SPACE_ID}"
    f"/environments/{ENVIRONMENT}/entries"
)

HEADERS = {
    "Authorization": f"Bearer {CONTENTFUL_MANAGEMENT_TOKEN}",
    "Content-Type": "application/vnd.contentful.management.v1+json",
}


def save_content_to_contentful(
    title,
    topic,
    content_type,
    tone,
    generated_content
):
    url = BASE_URL

    payload = {
        "fields": {
            "title": {"en-US": title},
            "topic": {"en-US": topic},
            "contentType": {"en-US": content_type},
            "tone": {"en-US": tone},
            "generatedContent": {"en-US": generated_content},
        }
    }

    headers = HEADERS.copy()
    headers["X-Contentful-Content-Type"] = "generatedContent"

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    entry = response.json()
    entry_id = entry["sys"]["id"]
    version = entry["sys"]["version"]

    publish_url = f"{url}/{entry_id}/published"

    publish_headers = HEADERS.copy()
    publish_headers["X-Contentful-Version"] = str(version)

    publish_response = requests.put(
        publish_url,
        headers=publish_headers,
        timeout=30
    )
    publish_response.raise_for_status()

    # Return the entry ID directly as a string.
    return entry_id


def get_saved_content_from_contentful():
    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        timeout=30
    )
    response.raise_for_status()

    entries = response.json().get("items", [])

    saved_contents = []

    for entry in entries:
        fields = entry.get("fields", {})

        saved_contents.append({
            "entry_id": entry["sys"]["id"],
            "title": fields.get("title", {}).get("en-US", ""),
            "topic": fields.get("topic", {}).get("en-US", ""),
            "content_type": fields.get("contentType", {}).get("en-US", ""),
            "tone": fields.get("tone", {}).get("en-US", ""),
            "generated_content": fields.get(
                "generatedContent", {}
            ).get("en-US", "")
        })

    return saved_contents


def update_content_in_contentful(
    entry_id,
    title,
    topic,
    content_type,
    tone,
    generated_content
):
    url = f"{BASE_URL}/{entry_id}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )
    response.raise_for_status()

    entry = response.json()
    version = entry["sys"]["version"]

    payload = {
        "fields": {
            "title": {"en-US": title},
            "topic": {"en-US": topic},
            "contentType": {"en-US": content_type},
            "tone": {"en-US": tone},
            "generatedContent": {"en-US": generated_content},
        }
    }

    update_headers = HEADERS.copy()
    update_headers["X-Contentful-Version"] = str(version)

    update_response = requests.put(
        url,
        json=payload,
        headers=update_headers,
        timeout=30
    )
    update_response.raise_for_status()

    return update_response.json()


def delete_content_from_contentful(entry_id):
    url = f"{BASE_URL}/{entry_id}"

    # Step 1: Get the latest entry version.
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )
    response.raise_for_status()

    entry = response.json()
    version = entry["sys"]["version"]
    sys_data = entry.get("sys", {})

    # Step 2: If published, unpublish it first.
    if sys_data.get("publishedVersion") is not None:
        unpublish_url = f"{url}/published"

        unpublish_headers = HEADERS.copy()
        unpublish_headers["X-Contentful-Version"] = str(version)

        unpublish_response = requests.delete(
            unpublish_url,
            headers=unpublish_headers,
            timeout=30
        )
        unpublish_response.raise_for_status()

        # Step 3: Fetch the entry again to get its latest version.
        latest_response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )
        latest_response.raise_for_status()

        latest_entry = latest_response.json()
        version = latest_entry["sys"]["version"]

    # Step 4: Delete using the latest version.
    delete_headers = HEADERS.copy()
    delete_headers["X-Contentful-Version"] = str(version)

    delete_response = requests.delete(
        url,
        headers=delete_headers,
        timeout=30
    )
    delete_response.raise_for_status()

    return True
