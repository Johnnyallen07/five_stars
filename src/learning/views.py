import json

import markdown2
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Course, MaterialPost
from five_stars.models import CustomUser
from typing import cast
from django.contrib import messages
from django.http import HttpResponse
from learning.forms import SavePost


# Create your views here.
def course_layout_view(request, course, user):
    topics = course.topics.all()
    return render(
        request,
        "course_layout.html",
        {"topics": topics, "course": course, "user": user},
    )


def course_access(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    user = cast(CustomUser, request.user)
    if user.is_authenticated and course in user.subscriptions.all():
        # If the user has access, redirect to the topics page
        return course_layout_view(request, course, user)
    else:
        return redirect(reverse("purchase"))


def material_page(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    user = cast(CustomUser, request.user)
    if course not in user.subscriptions.all():
        return redirect(reverse("purchase"))
    posts = MaterialPost.objects.filter(course_title=course).all()
    context = {"posts": posts, "postsLen": posts.count(), "course": course}
    return render(request, "material_page.html", context)


def upload_page(request, course_id):
    user = cast(CustomUser, request.user)
    if not user.is_teacher:
        return redirect(reverse("course_material", args=[course_id]))
    course = get_object_or_404(Course, course_id=course_id)
    posts = MaterialPost.objects.filter(course_title=course).all()
    context = {"posts": posts, "postsLen": posts.count(), "course": course}

    return render(request, "upload_page.html", context)


def course_info(reqeust, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    markdown_file_path = "D:\Desktop\Python Project/five_stars\static\markdown.md"  # Update the path accordingly
    try:
        with open(markdown_file_path, "r") as f:
            markdown_text = f.read()
    except FileNotFoundError:
        markdown_text = "Content not found."

    # Convert markdown to HTML
    html_content = markdown2.markdown(markdown_text)
    return render(
        reqeust, "course_info.html", {"course": course, "html_content": html_content}
    )


# add and change!
def manage_post(request, course_id, post_id):
    context = {"post": {}}
    course = get_object_or_404(Course, course_id=course_id)
    post = get_object_or_404(MaterialPost, pk=post_id, course_title=course_id)
    context["post"] = post
    context["course"] = course
    return render(request, "manage_post.html", context)


def add_post(request, course_id):
    context = {"post": {}}
    course = get_object_or_404(Course, course_id=course_id)
    context["course"] = course
    return render(request, "manage_post.html", context)


def delete_post(request):
    resp = {"status": "failed", "msg": ""}
    if request.method == "POST":
        try:
            post = MaterialPost.objects.get(id=request.POST["id"])
            post.delete()
            resp["status"] = "success"
            messages.success(request, "Post has been deleted successfully")
        except:
            resp["msg"] = "Undefined Post ID"
    return HttpResponse(json.dumps(resp), content_type="application/json")


def save_post(request):
    resp = {"status": "failed", "msg": ""}
    if request.method == "POST":
        print(request.POST)
        form = SavePost(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "File has been saved successfully.")
            resp["status"] = "success"
        else:
            for fields in form:
                for error in fields.errors:
                    resp["msg"] += str(error + "<br/>")
            form = SavePost(request.POST, request.FILES)

    else:
        resp["msg"] = "No Data sent."
    print(resp)
    return HttpResponse(json.dumps(resp), content_type="application/json")
