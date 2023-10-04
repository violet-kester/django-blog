from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.views.decorators import require_POST


def post_list(request):
    """Retrieves all published posts in paginated form."""

    post_list = Post.objects.filter(status='PB')

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
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    """Retrieves individual published Post by ID."""

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


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

    post = get_object_or_404(Post, id=post_id, status=Post.status.PUBLISHED)
    comment = None

    # instantiate form using submitted POST data when a comment is posted
    form = CommentForm(data=request.Post)
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
