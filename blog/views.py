from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):
    """Renders a template of all published posts in paginated form.
       Optionally filters posts by tag slug URL parameter.

       Context variables:

       - `posts` - A Page object containing a list of Post objects.
       - `tag` - A Tag object if tag slug is provided, or None.

    """

    post_list = Post.objects.filter(status='PB')
    tag = None

    # if tag_slug provided, filter posts by tag
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # paginate posts - 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page not an integer, show first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page number out of range, show last page
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    """Renders a template of a single published post.

       Context variables:

       - `post` - The Post object.
       - `comments` - A QuerySet of related comment objects.
       - `form` - A CommentForm instance for posting new comments.
       - `similar_posts` - A QuerySet of recommended Posts sharing the same tags.
    """

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # active comments for this post
    comments = post.comments.filter(active=True)

    # form for posting comments
    form = CommentForm()

    # list of similar, recommended posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status='PB')\
                                .filter(tags__in=post_tags_ids)\
                                .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


class PostListView(ListView):
    """Alternative class-based post_list view."""

    # set queryset attribute to filter posts to display
    queryset = Post.objects.filter(status='PB')

    # set context_object_name attribute to be referenced in template
    context_object_name = 'posts'

    # enable pagination - 3 posts per page
    paginate_by = 3

    # specify template to render the view
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    """Shares a published post by email using a form."""

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}" \
                      f"{data['name']}\'s comments: {data['comments']}"
            send_mail(subject, message,
                      'kester.violet.j@gmail.com', [data['to']])
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    """Create and save a comment for a published post."""

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    # instantiate form using submitted POST data when a comment is posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create a comment without saving it to the database
        comment = form.save(commit=False)
        # assign comment to post
        comment.post = post
        # save the comment to the database
        comment.save()

    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


def post_search(request):
    """Search for blog posts by query."""

    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(status='PB').annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
