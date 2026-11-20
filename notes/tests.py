from django.urls import reverse
from django.test import TestCase
from .models import Note
from .forms import NoteForm


class NoteModelTest(TestCase):
    """Verify note persistence and model behavior."""

    def test_create_note(self):
        """Verify create note."""
        note = Note.objects.create(
            title='My First Concept',
            content='Every idea starts with a concept.'
            )

        self.assertEqual(note.title, 'My First Concept')
        self.assertEqual(note.content, 'Every idea starts with a concept.')
        self.assertEqual(str(note), 'My First Concept')
        self.assertIsNotNone(note.created_at)

    def test_update_note(self):
        """Verify update note."""
        note = Note.objects.create(
            title='My Aspirations',
            content='I aspire to be a great software engineer.'
            )

        note.title = 'My 2027 Goals'
        note.save()

        updated_note = Note.objects.get(id=note.id)

        self.assertEqual(
            updated_note.title,
            'My 2027 Goals'
        )

    def test_read_note(self):
        """Verify read note."""
        note = Note.objects.create(
            title='My Learning Journey',
            content='Learning One Bug at a Time.'
            )

        retrieved_note = Note.objects.get(id=note.id)

        self.assertEqual(retrieved_note.title, 'My Learning Journey')
        self.assertEqual(
            retrieved_note.content,
            'Learning One Bug at a Time.'
        )

    def test_delete_note(self):
        """Verify delete note."""
        note = Note.objects.create(
            title='My Achieved Goals',
            content='Learning Python and Django.'
            )

        note_id = note.id

        self.assertTrue(
            Note.objects.filter(id=note_id).exists()
        )

        note.delete()
        self.assertFalse(
            Note.objects.filter(id=note_id).exists()
        )


class NoteViewTest(TestCase):
    """Verify CRUD endpoints and rendered content."""

    def test_note_list_view(self):
        """Verify note list view."""
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')

    def test_note_detail_view(self):
        """Verify note detail view."""
        note = Note.objects.create(
            title='My First Concept',
            content='Every idea starts with a concept.'
            )
        response = self.client.get(reverse('note_detail', args=[note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')

    def test_note_create_view(self):
        """Verify note create view."""
        response = self.client.post(reverse('note_create'), {
            'title': 'My Aspirations',
            'content': 'I aspire to be a great software engineer.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title='My Aspirations').exists())

    def test_note_update_view(self):
        """Verify note update view."""
        note = Note.objects.create(
            title='My Learning Journey',
            content='Learning One Bug at a Time.'
            )
        response = self.client.post(reverse('note_update', args=[note.id]), {
            'title': 'My Updated Learning Journey',
            'content': 'Learning Django and Python.'
        })
        self.assertEqual(response.status_code, 302)
        updated_note = Note.objects.get(id=note.id)
        self.assertEqual(updated_note.title, 'My Updated Learning Journey')


class NoteSafetyTest(TestCase):
    """Check safe deletion and missing-note handling."""

    def test_delete_rejects_get(self):
        """Verify delete rejects get."""
        note = Note.objects.create(title='Keep', content='Do not delete')
        response = self.client.get(reverse('note_delete', args=[note.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Note.objects.filter(pk=note.pk).exists())

    def test_delete_accepts_post(self):
        """Verify delete accepts post."""
        note = Note.objects.create(title='Remove', content='Delete me')
        response = self.client.post(reverse('note_delete', args=[note.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=note.pk).exists())

    def test_missing_note_returns_404(self):
        """Verify missing note returns 404."""
        response = self.client.get(reverse('note_detail', args=[999999]))
        self.assertEqual(response.status_code, 404)


class NoteFormTest(TestCase):
    """Test validation of the sticky note form."""

    def test_note_without_title_is_invalid(self):
        """Verify note without title is invalid."""
        form_data = {'title': '', 'content': 'Content without a title'}
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class NoteEdgeCaseTest(TestCase):
    """Cover validation errors, missing notes, and list ordering."""

    def test_invalid_create_shows_errors_and_does_not_save(self):
        """An empty title must display an error without creating a note."""
        response = self.client.post(reverse('note_create'), {'title': '', 'content': 'Text'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertFalse(Note.objects.exists())

    def test_empty_post_is_bound_and_shows_errors(self):
        """An entirely empty POST must show validation errors."""
        response = self.client.post(reverse('note_create'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertFalse(Note.objects.exists())

    def test_invalid_update_shows_errors_and_preserves_note(self):
        """An invalid edit must not change the saved note."""
        note = Note.objects.create(title='Original', content='Keep this')
        response = self.client.post(reverse('note_update', args=[note.pk]), {'title': '', 'content': 'Changed'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        note.refresh_from_db()
        self.assertEqual((note.title, note.content), ('Original', 'Keep this'))

    def test_missing_update_returns_404(self):
        """Editing a nonexistent note must return 404."""
        self.assertEqual(self.client.get(reverse('note_update', args=[999999])).status_code, 404)

    def test_missing_delete_returns_404(self):
        """Deleting a nonexistent note by POST must return 404."""
        self.assertEqual(self.client.post(reverse('note_delete', args=[999999])).status_code, 404)

    def test_empty_list_message(self):
        """The list must explain when no notes exist."""
        self.assertContains(self.client.get(reverse('note_list')), 'No Notes Yet!')

    def test_newest_first(self):
        """The newest note must appear before older notes."""
        Note.objects.create(title='Older', content='First')
        Note.objects.create(title='Newer', content='Second')
        response = self.client.get(reverse('note_list'))
        self.assertEqual([n.title for n in response.context['notes']], ['Newer', 'Older'])

    def test_list_displays_note_content(self):
        """The list must render the note title and content."""
        Note.objects.create(title='Visible title', content='Visible body')
        response = self.client.get(reverse('note_list'))
        self.assertContains(response, 'Visible title')
        self.assertContains(response, 'Visible body')

    def test_detail_displays_note_content(self):
        """The detail page must render the note title and content."""
        note = Note.objects.create(title='Detail title', content='Detail body')
        response = self.client.get(reverse('note_detail', args=[note.pk]))
        self.assertContains(response, 'Detail title')
        self.assertContains(response, 'Detail body')
