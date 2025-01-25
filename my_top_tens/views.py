from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.http import Http404 

from .models import Topic, Entry
from .forms import TopicForm, MultiRankForm


def index(request):
    """The home page for My Top Tens."""
    return render(request, 'my_top_tens/index.html')

@login_required
def topics(request): #Only ran if the user is logged in
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'my_top_tens/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and its ranked entries."""
    topic = get_object_or_404(Topic, id=topic_id)

    # Make sure the topic belongs to the current user. 
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('rank')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'my_top_tens/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        form = TopicForm()
    else: 
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('my_top_tens:topics')
    context = {'form': form}
    return render(request, 'my_top_tens/new_topic.html', context)

@login_required
def manage_ranks(request, topic_id):
    """Page for adding or editing ranks 1-10 for a topic."""
    topic = get_object_or_404(Topic, id=topic_id)
    
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('rank')

    # Forms for each rank
    forms = []
    for rank in range(1, 11):
        entry = entries.filter(rank=rank).first()
        initial_data = {'text': entry.text, 'description': entry.description} if entry else {}
        form = MultiRankForm(initial=initial_data, prefix=f'rank_{rank}')
        forms.append({'rank': rank, 'form': form})

    if request.method == 'POST':
        for rank, form_dict in enumerate(forms, start=1):
            form = MultiRankForm(data=request.POST, prefix=f'rank_{rank}')
            if form.is_valid():
                text = form.cleaned_data['text']
                description = form.cleaned_data['description']

                if text: 
                    entry = entries.filter(rank=rank).first()
                    if entry:
                        entry.text = text
                        entry.description = description
                        entry.save()
                    else:
                        Entry.objects.create(topic=topic, rank=rank, text=text, description=description)
                elif entries.filter(rank=rank).exists():
                    # Delete entry if text is empty
                    entries.filter(rank=rank).delete()

        return redirect('my_top_tens:topic', topic_id=topic_id)

    context = {'topic': topic, 'forms': forms}
    return render(request, 'my_top_tens/manage_ranks.html', context)

@login_required
def edit_topic_description(request, topic_id):
    """Edit the description of a specific topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(data=request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('my_top_tens:topic', topic_id=topic_id)  # Redirect back to the topic page

    context = {'topic': topic, 'form': form}
    return render(request, 'my_top_tens/edit_topic_description.html', context)

@login_required
def select_topic_to_delete(request):
    """Show a page where the user can select a topic to delete."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'my_top_tens/select_topic_to_delete.html', context)


@login_required
def delete_topic(request):
    """Handle topic deletion after selection."""
    if request.method == "POST":
        topic_id = request.POST.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_id)

        # Ensure the topic belongs to the logged-in user
        if topic.owner != request.user:
            raise Http404

        topic.delete()
        return redirect('my_top_tens:topics')