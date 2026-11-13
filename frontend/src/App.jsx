
import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api";

function App() {
  const [topic, setTopic] = useState("");
  const [contentType, setContentType] = useState("Blog");
  const [tone, setTone] = useState("Professional");
  const [length, setLength] = useState("Medium");

  const [generatedContent, setGeneratedContent] = useState("");
  const [savedContents, setSavedContents] = useState([]);

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const [error, setError] = useState("");
  const [topicError, setTopicError] = useState("");
  const [saveMessage, setSaveMessage] = useState("");
  const [editingEntryId, setEditingEntryId] = useState(null);

  // Generate Content
  const handleGenerate = async () => {
    if (!topic.trim()) {
      setTopicError("Please enter a topic");
      setGeneratedContent("");
      setError("");
      return;
    }

    setTopicError("");
    setLoading(true);
    setError("");
    setSaveMessage("");
    setGeneratedContent("");

    try {
      const response = await fetch(
        `${API_URL}/generate-content/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            topic: topic.trim(),
            content_type: contentType,
            tone,
            length,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || "Content generation failed"
        );
      }

      setGeneratedContent(data.generated_content);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Save Content
  const handleSave = async () => {
    if (!generatedContent.trim()) {
      setError("Please generate content before saving");
      return;
    }

    setSaving(true);
    setError("");
    setSaveMessage("");

    try {
      const response = await fetch(
        `${API_URL}/save-content/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: topic.trim(),
            topic: topic.trim(),
            content_type: contentType,
            tone,
            generated_content: generatedContent,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || "Unable to save content"
        );
      }

      setSaveMessage(
        `Content saved successfully! Entry ID: ${data.entry_id}`
      );

      await handleViewSavedContent();

    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  // Get Saved Content
  const handleViewSavedContent = async () => {
    setFetching(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/saved-content/`
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || "Unable to fetch saved content"
        );
      }

      setSavedContents(data.data);

    } catch (err) {
      setError(err.message);
    } finally {
      setFetching(false);
    }
  };

  // Edit Content
  const handleEdit = (item) => {
    setEditingEntryId(item.entry_id);
    setTopic(item.topic);
    setContentType(item.content_type);
    setTone(item.tone);
    setGeneratedContent(item.generated_content);

    setError("");
    setTopicError("");

    setSaveMessage(
      "Editing saved content. Make your changes below."
    );

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // Update Content
  const handleUpdate = async () => {
    if (!editingEntryId) {
      setError("Please select content to edit");
      return;
    }

    if (!topic.trim() || !generatedContent.trim()) {
      setError(
        "Topic and generated content are required"
      );
      return;
    }

    setUpdating(true);
    setError("");
    setSaveMessage("");

    try {
      const response = await fetch(
        `${API_URL}/update-content/${editingEntryId}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: topic.trim(),
            topic: topic.trim(),
            content_type: contentType,
            tone,
            generated_content: generatedContent,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || "Unable to update content"
        );
      }

      setSaveMessage(
        "Content updated successfully!"
      );

      setEditingEntryId(null);

      await handleViewSavedContent();

    } catch (err) {
      setError(err.message);
    } finally {
      setUpdating(false);
    }
  };

  // Cancel Edit
  const handleCancelEdit = () => {
    setEditingEntryId(null);
    setTopic("");
    setContentType("Blog");
    setTone("Professional");
    setLength("Medium");
    setGeneratedContent("");

    setError("");
    setTopicError("");
    setSaveMessage("");
  };

  // Delete Content
  const handleDelete = async (entryId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this content?"
    );

    if (!confirmed) return;

    setDeletingId(entryId);
    setError("");
    setSaveMessage("");

    try {
      const response = await fetch(
        `${API_URL}/delete-content/${entryId}/`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || "Unable to delete content"
        );
      }

      setSaveMessage(
        "Content deleted successfully!"
      );

      if (editingEntryId === entryId) {
        handleCancelEdit();
      }

      await handleViewSavedContent();

    } catch (err) {
      setError(err.message);
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <h1>AI Content Generator</h1>
        <p>Create quality content in seconds</p>
      </header>

      <main className="container">

        {/* Generate / Edit Form */}
        <section className="form-section">

          <h2>
            {editingEntryId
              ? "Edit Saved Content"
              : "Generate Your Content"}
          </h2>

          {/* Topic */}
          <label>Topic</label>

          <input
            type="text"
            placeholder="Enter your topic"
            value={topic}
            onChange={(e) => {
              setTopic(e.target.value);
              setTopicError("");
            }}
          />

          {topicError && (
            <p className="error">{topicError}</p>
          )}

          {/* Content Type */}
          <label>Content Type</label>

          <select
            value={contentType}
            onChange={(e) =>
              setContentType(e.target.value)
            }
          >
            <option>Blog</option>
            <option>Product Description</option>
            <option>Social Media Post</option>
            <option>SEO Description</option>
          </select>

          {/* Tone */}
          <label>Tone</label>

          <select
            value={tone}
            onChange={(e) =>
              setTone(e.target.value)
            }
          >
            <option>Professional</option>
            <option>Friendly</option>
            <option>Creative</option>
          </select>

          {/* Length */}
          {!editingEntryId && (
            <>
              <label>Length</label>

              <select
                value={length}
                onChange={(e) =>
                  setLength(e.target.value)
                }
              >
                <option>Short</option>
                <option>Medium</option>
                <option>Long</option>
              </select>
            </>
          )}

          {/* Buttons */}
          {editingEntryId ? (
            <>
              <button
                type="button"
                onClick={handleUpdate}
                disabled={
                  updating ||
                  !topic.trim() ||
                  !generatedContent.trim()
                }
              >
                {updating
                  ? "Updating..."
                  : "Update Content"}
              </button>

              <button
                type="button"
                onClick={handleCancelEdit}
                disabled={updating}
              >
                Cancel Edit
              </button>
            </>
          ) : (
            <button
              type="button"
              onClick={handleGenerate}
              disabled={loading || saving}
            >
              {loading
                ? "Generating..."
                : "Generate Content"}
            </button>
          )}

        </section>

        {/* Generated Content */}
        <section className="output-section">

          <h2>Generated Content</h2>

          {error && (
            <p className="error">{error}</p>
          )}

          {saveMessage && (
            <p className="success">
              {saveMessage}
            </p>
          )}

          {generatedContent ? (
            <>
              <textarea
                value={generatedContent}
                onChange={(e) => {
                  setGeneratedContent(e.target.value);
                  setSaveMessage("");
                }}
                rows={15}
              />

              {!editingEntryId && (
                <button
                  type="button"
                  onClick={handleSave}
                  disabled={
                    saving ||
                    loading ||
                    !generatedContent.trim()
                  }
                >
                  {saving
                    ? "Saving..."
                    : "Save to Contentful"}
                </button>
              )}
            </>
          ) : (
            <p>
              Your generated content will appear here.
            </p>
          )}

        </section>

      </main>

      {/* Saved Content */}
      <section className="saved-section">

        <h2>Saved Content</h2>

        <button
          type="button"
          onClick={handleViewSavedContent}
          disabled={fetching}
        >
          {fetching
            ? "Loading..."
            : "View Saved Content"}
        </button>

        <div className="saved-list">

          {savedContents.map((item) => (
            <div
              className="saved-card"
              key={item.entry_id}
            >

              <h3>{item.title}</h3>

              <p>
                <strong>Topic:</strong> {item.topic}
              </p>

              <p>
                <strong>Content Type:</strong>{" "}
                {item.content_type}
              </p>

              <p>
                <strong>Tone:</strong> {item.tone}
              </p>

              <div className="saved-content">
                <strong>Generated Content:</strong>

                <pre>
                  {item.generated_content}
                </pre>
              </div>

              {/* Edit Button */}
              <button
                type="button"
                onClick={() => handleEdit(item)}
                disabled={
                  updating || deletingId !== null
                }
              >
                Edit
              </button>

              {/* Delete Button */}
              <button
                type="button"
                onClick={() =>
                  handleDelete(item.entry_id)
                }
                disabled={
                  deletingId !== null || updating
                }
              >
                {deletingId === item.entry_id
                  ? "Deleting..."
                  : "Delete"}
              </button>

            </div>
          ))}

          {savedContents.length === 0 &&
            !fetching && (
              <p>
                Click "View Saved Content" to see
                your saved entries.
              </p>
            )}

        </div>

      </section>

    </div>
  );
}

export default App;
