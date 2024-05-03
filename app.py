import streamlit as st
import uuid  # For generating unique note IDs
from io import BytesIO
from reportlab.pdfgen import canvas  # For PDF generation


# Note Data Structure (in-memory storage)
notes = {}

# Example note structure
# {
#   "id": "unique_note_id",
#   "title": "Note Title",
#   "content": "Note content",
#   "collaborators": ["user1@email.com", "user2@email.com"],  # Optional collaborators
# }


def create_note(title, content, collaborators=[]):
    """Creates a new note with a unique ID."""
    note_id = str(uuid.uuid4())
    notes[note_id] = {
        "id": note_id,
        "title": title,
        "content": content,
        "collaborators": collaborators,
    }
    st.success("Note created successfully!")


def get_note(note_id):
    """Retrieves a note from the in-memory storage."""
    return notes.get(note_id)


def update_note(note_id, title, content, collaborators=[]):
    """Updates an existing note."""
    if note_id in notes:
        notes[note_id]["title"] = title
        notes[note_id]["content"] = content
        notes[note_id]["collaborators"] = collaborators
        st.success("Note updated successfully!")
    else:
        st.error("Note not found!")


def delete_note(note_id):
    """Deletes a note."""
    if note_id in notes:
        del notes[note_id]
        st.success("Note deleted successfully!")
    else:
        st.error("Note not found!")


def generate_pdf(note):
    """Generates a PDF document from the note content."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 750, f"Title: {note['title']}")
    pdf.drawString(50, 720, f"Content:\n{note['content']}")
    pdf.save()
    buffer.seek(0)
    return buffer


def main():
    """Streamlit app UI for creating, viewing, and collaborating on notes."""

    # Display app title
    st.title("Collaborative Note Taking")

    # Create a new note section
    with st.expander("Create New Note"):
        note_title = st.text_input("Note Title")
        note_content = st.text_area("Note Content")
        collaborator_emails = st.multiselect("Collaborators (optional, comma-separated emails)", [])
        collaborators = [email.strip() for email in collaborator_emails.split(",")]

        if st.button("Create Note"):
            create_note(note_title, note_content, collaborators)

    # View and edit existing notes section
    notes_list = list(notes.values())
    if notes_list:
        selected_note = st.selectbox("Select Note", [note["title"] for note in notes_list])
        selected_note_data = notes[selected_note["id"]]

        st.subheader(f"Note: {selected_note_data['title']}")
        st.write(selected_note_data["content"])

        with st.expander("Edit Note"):
            updated_title = st.text_input("Update Title", selected_note_data["title"])
            updated_content = st.text_area("Update Content", selected_note_data["content"])
            updated_collaborators = st.multiselect(
                "Update Collaborators (optional, comma-separated emails)",
                selected_note_data["collaborators"],
            )

            if st.button("Update Note"):
                update_note(
                    selected_note_data["id"],
                    updated_title,
                    updated_content,
                    updated_collaborators,
                )

        # Download PDF button
        if st.button("Download PDF"):
            pdf_buffer = generate_pdf(selected_note_data)
            st.download_button(
                label="Download Note as PDF",
                data=pdf_buffer,
                file_name=f"{selected_note_data['title']}" )
