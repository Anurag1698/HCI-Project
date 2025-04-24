from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    Blog,
    Room,
    RoomRequest,
    Topic,
    Message,
    User,
    Curriculam,
    Comment,
    Contact,
    Profile,
    RoomNotification,
)
from .forms import RoomForm, UserForm

from django.contrib.auth.models import auth, User

from django.core.mail import send_mail
from django.conf import settings

from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.views.decorators.http import require_POST


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Invalid User")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Handle approved room requests
            approved_requests = RoomRequest.objects.filter(user=user, is_approved=True)
            if approved_requests.exists():
                for req in approved_requests:
                    room = req.room
                    room.participants.add(user)
                    req.delete()
                room_names = ", ".join([req.room.name for req in approved_requests])
                messages.success(request, f"You've been added to: {room_names}")

            # ✅ Notify host about pending join requests
            pending_requests = RoomRequest.objects.filter(
                room__host=user, is_approved=False
            )
            if pending_requests.exists():
                messages.info(
                    request,
                    f"You have {pending_requests.count()} pending join request(s) to review.",
                )

            # ✅ Notify if user was removed from any rooms
            removed_notices = RoomNotification.objects.filter(user=user)

            if removed_notices.exists():
                removed_rooms = ", ".join(
                    [n.room.name for n in removed_notices if n.type == "removed"]
                )
                rejected_rooms = ", ".join(
                    [n.room.name for n in removed_notices if n.type == "rejected"]
                )

                if removed_rooms:
                    messages.warning(request, f"You were removed from: {removed_rooms}")
                if rejected_rooms:
                    messages.error(
                        request, f"Your join request was rejected for: {rejected_rooms}"
                    )

                removed_notices.delete()

            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials!!!")

    context = {"page": page}
    return render(request, "base/login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "User logged out!!!")
    return redirect("login")


def registerPage(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration, please valid credentials!!!"
        )
    form = NewUserForm()
    return render(
        request=request,
        template_name="base/register.html",
        context={"register_form": form},
    )


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(host__username__icontains=q)
        | Q(description__icontains=q)
    )

    blogs = Blog.objects.all()
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
        "blogs": blogs,
    }
    return render(request, "base/home.html", context)


def rooms(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(host__username__icontains=q)
        | Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "base/rooms.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    curriculam = room.curriculam_set.all()
    rooms = Room.objects.all()

    if request.method == "POST" and request.FILES["file"]:
        curriculam = Curriculam.objects.create(
            name=request.POST.get("name"), room=room, file=request.FILES["file"]
        )
        messages.success(request, "Curriculam Added !!!")
        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
        "curriculam": curriculam,
        "rooms": rooms,
    }
    return render(request, "base/room.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST" and request.FILES["image"]:
        topic_name = request.POST.get("topic")
        topic, create = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            image=request.FILES["image"],
        )
        messages.success(request, "Room created!!!")
        return redirect("create-room")

    context = {"form": form, "topics": topics}
    return render(request, "base/create-room.html", context)


@login_required(login_url="/login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        messages.warning(request, "Invalid request!! ")
        return redirect("home")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        messages.success(request, "Room updated")
        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/update-room.html", context)


@login_required(login_url="/login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.warning(request, "Invalid request!!! ")
        return redirect("home")

    if request.method == "POST":
        room.delete()
        messages.warning(request, "Room deleted")
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="/login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        messages.warning(request, "Invalid request!! ")
        return redirect("home")

    if request.method == "POST":
        message.delete()
        messages.warning(request, "Message deleted")
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="/login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect("update-user")

    return render(request, "base/update-user.html", {"form": form})


def blogs(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(host__username__icontains=q)
        | Q(body__icontains=q)
    )

    topics = Topic.objects.all()
    blog_count = blogs.count()
    blog_comments = Comment.objects.filter(Q(blog__topic__name__icontains=q))

    context = {
        "blogs": blogs,
        "topics": topics,
        "blog_comments": blog_comments,
        "blog_count": blog_count,
    }
    return render(request, "base/blogs.html", context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    blogs = Blog.objects.all()
    blog_messages = blog.comment_set.all()

    if request.method == "POST":
        comment = Comment.objects.create(
            user=request.user, blog=blog, body=request.POST.get("body")
        )
        room.participants.add(request.user)

        messages.success(request, "Message sent!!!")
        return redirect("room", pk=room.id)

    context = {"blog": blog, "blogs": blogs, "blog_messages": blog_messages}
    return render(request, "base/blog.html", context)


def contact(request):
    if request.method == "POST":
        contact = Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            body=request.POST.get("body"),
        )
        messages.success(request, "Message sent")

        subject = "StudyRoom Online Lerning Community Message"
        message = f"Hi {contact.name}, thank you for your message to StudyRoom Online Lerning Community"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [contact.email]
        send_mail(subject, message, email_from, recipient_list)

    context = {}
    return render(request, "base/contact.html", context)


def about(request):
    context = {}
    return render(request, "base/about.html", context)


def service(request):
    context = {}
    return render(request, "base/service.html", context)


def faq(request):
    context = {}
    return render(request, "base/faq.html", context)


@login_required
def joinUs(request, pk):
    room = Room.objects.get(id=pk)
    user = request.user

    # If user is already a participant
    if user in room.participants.all():
        messages.info(request, "You are already a participant of this room.")
        return redirect("room", pk=room.id)

    # If user has already requested
    if RoomRequest.objects.filter(user=user, room=room).exists():
        messages.info(request, "You have already requested to join this room.")
        return redirect("room", pk=room.id)

    # Create join request
    RoomRequest.objects.create(user=user, room=room)
    messages.success(request, "Your request to join the room has been sent.")
    return redirect("room", pk=room.id)


@login_required
def manage_room_requests(request, room_id):
    room = Room.objects.get(id=room_id)

    # Only allow the host to view this page
    if request.user != room.host:
        return redirect("home")

    pending_requests = RoomRequest.objects.filter(room=room, is_approved=False)

    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        if action in ["approve", "reject"]:
            join_request = RoomRequest.objects.get(user_id=user_id, room=room)
            if action == "approve":
                join_request.is_approved = True
                join_request.save()
                # ✅ Add the user to participants immediately
                room.participants.add(join_request.user)

                # ✅ Optional: Delete the request if no longer needed
                # join_request.delete()
                messages.success(
                    request, f"Approved {join_request.user.username} for {room.name}"
                )
            else:
                # Notify the user that they were rejected
                RoomNotification.objects.create(
                    user=join_request.user, room=room, type="rejected"
                )
                join_request.delete()
                messages.warning(
                    request, f"Rejected {join_request.user.username} for {room.name}"
                )

        return redirect("manage-room-requests", room_id=room.id)

    return render(
        request,
        "base/manage_requests.html",
        {"room": room, "pending_requests": pending_requests},
    )


@login_required
@require_POST
def kick_participant(request, room_id, user_id):
    room = get_object_or_404(Room, id=room_id)
    user_to_remove = get_object_or_404(User, id=user_id)

    if request.user != room.host:
        messages.error(request, "You're not authorized to perform this action.")
        return redirect("room", pk=room_id)

    if user_to_remove == room.host:
        messages.error(request, "You cannot remove yourself.")
        return redirect("room", pk=room_id)

    room.participants.remove(user_to_remove)

    # Notify the user that they were removed
    RoomNotification.objects.create(user=user_to_remove, room=room, type="removed")

    messages.warning(
        request, f"{user_to_remove.username} has been removed from {room.name}."
    )

    return redirect("room", pk=room_id)
