from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import NoteForm
from .models import Note


def note_list(request):
    """Display all notes, newest first."""
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})


def note_detail(request, pk):
    """Display one note or return HTTP 404 if it does not exist."""
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


def note_create(request):
    """Validate and save a new note, or display an empty form."""
    form = NoteForm(request.POST if request.method == "POST" else None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('note_list')

    return render(request, 'notes/note_form.html', {'form': form})


def note_update(request, pk):
    """Update an existing note using validated form input."""
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST if request.method == "POST" else None, instance=note)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('note_list')

    return render(request, 'notes/note_form.html', {'form': form})


@require_POST
def note_delete(request, pk):
    """Delete a note only after a POST request."""
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect('note_list')
