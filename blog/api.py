from typing import Optional
from ninja import Router, Schema
from django.http import HttpRequest
from django.utils.text import slugify

from blog.models import BlogPost
from blog.choices import BlogPostStatus
from talentleads.auth import TokenAuth
from talentleads.utils import get_talentleads_logger

logger = get_talentleads_logger(__name__)


# Schemas
class BlogPostCreateSchema(Schema):
    title: str
    description: Optional[str] = ""
    slug: Optional[str] = None
    tags: str = ""
    content: str
    status: str = BlogPostStatus.DRAFT


class BlogPostResponseSchema(Schema):
    id: int
    title: str
    description: str
    slug: str
    tags: str
    content: str
    status: str
    created: str
    modified: str

    @staticmethod
    def resolve_created(obj):
        return obj.created.isoformat()

    @staticmethod
    def resolve_modified(obj):
        return obj.modified.isoformat()


class ErrorSchema(Schema):
    detail: str


router = Router(tags=["Blog"])


@router.post(
    "/posts",
    response={201: BlogPostResponseSchema, 403: ErrorSchema, 400: ErrorSchema, 401: ErrorSchema},
    auth=TokenAuth(),
)
def create_blog_post(request: HttpRequest, payload: BlogPostCreateSchema):
    """
    Create a new blog post.
    Only superusers can create blog posts.
    """
    if not request.auth.is_superuser:
        return 403, {"detail": "Only superusers can create blog posts"}

    if payload.status not in [BlogPostStatus.DRAFT, BlogPostStatus.PUBLISHED]:
        return 400, {"detail": f"Invalid status. Must be '{BlogPostStatus.DRAFT}' or '{BlogPostStatus.PUBLISHED}'"}

    slug = payload.slug if payload.slug else slugify(payload.title)

    if BlogPost.objects.filter(slug=slug).exists():
        return 400, {"detail": f"A blog post with slug '{slug}' already exists"}

    # Create the blog post
    blog_post = BlogPost.objects.create(
        title=payload.title,
        description=payload.description,
        slug=slug,
        tags=payload.tags,
        content=payload.content,
        status=payload.status,
    )

    return 201, blog_post


@router.get(
    "/posts",
    response={200: list[BlogPostResponseSchema], 401: ErrorSchema},
    auth=TokenAuth(),
)
def list_blog_posts(request: HttpRequest, status: Optional[str] = None):
    """
    List all blog posts.
    Superusers can see all posts. Regular users can only see published posts.
    """
    queryset = BlogPost.objects.all().order_by("-created")

    if status:
        queryset = queryset.filter(status=status)
    elif not request.auth.is_superuser:
        queryset = queryset.filter(status=BlogPostStatus.PUBLISHED)

    return queryset


@router.get(
    "/posts/{slug}",
    response={200: BlogPostResponseSchema, 404: ErrorSchema, 401: ErrorSchema},
    auth=TokenAuth(),
)
def get_blog_post(request: HttpRequest, slug: str):
    """
    Get a specific blog post by slug.
    Superusers can see all posts. Regular users can only see published posts.
    """
    try:
        if request.auth.is_superuser:
            blog_post = BlogPost.objects.get(slug=slug)
        else:
            blog_post = BlogPost.objects.get(slug=slug, status=BlogPostStatus.PUBLISHED)
        return 200, blog_post
    except BlogPost.DoesNotExist:
        return 404, {"detail": "Blog post not found"}
