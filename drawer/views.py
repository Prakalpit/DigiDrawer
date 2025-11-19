from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth import logout

from .models import Tag,File

def is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"



'''
        Core Views
'''

def index(request):
    return render(request, 'index.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

'''
        Tag View
'''

@login_required
def tag_list(request):
    tags = Tag.objects.all().order_by("name")
    return render(request, "tag/view.html", {"tags": tags})

@require_POST
@login_required
def tag_create(request):
    name = request.POST.get("name")
    if name:
        Tag.objects.create(name=name)
    return redirect("tag_list")


@login_required
@require_POST
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    name = request.POST.get("name")

    if name:
        tag.name = name
        tag.save()

    return redirect("tag_list")

@login_required
@require_POST
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return redirect("tag_list")



'''
        File View
'''

@login_required
def file_list(request):
    view_mode = request.GET.get("view", "active")
    search_query = request.GET.get("search", "").strip()
    tag_filter = request.GET.get("tag")

    # Base queryset
    if view_mode == "archived":
        queryset = File.objects.filter(is_archived=True)
    else:
        queryset = File.objects.filter(is_archived=False)

    # Search
    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    # Tag filter
    selected_tag = None
    if tag_filter and tag_filter.isdigit():
        queryset = queryset.filter(tags__id=tag_filter)
        try:
            selected_tag = Tag.objects.get(id=tag_filter)
        except Tag.DoesNotExist:
            selected_tag = None

    queryset = queryset.order_by("-created_at")

    # Pagination
    paginator = Paginator(queryset, 10)
    page = request.GET.get("page")
    files = paginator.get_page(page)

    tags = Tag.objects.all()

    return render(request, "file/view.html", {
        "files": files,
        "tags": tags,
        "view_mode": view_mode,
        "search_query": search_query,
        "tag_filter": tag_filter,
        "selected_tag": selected_tag,  # ← we pass this
    })




@login_required
@require_POST
def file_create(request):
    uploaded_file = request.FILES.get("file")
    name = request.POST.get("name")
    tag_ids = request.POST.get("tags", "").split(",")

    if uploaded_file:
        file_obj = File.objects.create(
            file=uploaded_file,
            name=name if name else uploaded_file.name,
        )

        # Clean tag list
        cleaned = [tid for tid in tag_ids if tid.isdigit()]
        file_obj.tags.set(cleaned)

    return redirect("file_list")



@login_required
@require_POST
def file_archive(request, pk):
    file_obj = get_object_or_404(File, pk=pk)
    file_obj.is_archived = not file_obj.is_archived
    file_obj.save()
    return redirect("file_list")


@login_required
@require_POST
def file_delete(request, pk):
    file_obj = get_object_or_404(File, pk=pk)

    # delete actual file from storage
    file_obj.file.delete(save=False)

    file_obj.delete()
    return redirect("file_list")

