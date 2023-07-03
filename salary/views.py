import secrets
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import datetime, timedelta


users_db = {
    "ivan": {"password": "12345", "salary": 50000, "next_raise": "2023-09-01"},
    "vova": {"password": "54321", "salary": 60000, "next_raise": "2023-10-01"},
    "oleg": {"password": "qwerty", "salary": 70000, "next_raise": "2023-11-01"},
    "masha": {"password": "ytrewq", "salary": 80000, "next_raise": "2023-12-01"},
}

active_tokens = {}


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username in users_db and users_db[username]["password"] == password:
            token = generate_token()
            active_tokens[token] = {
                "username": username,
                "created_at": datetime.now()
            }
            return render(request, "token.html", {"token": token})
        else:
            return render(request, "login.html", {"error_message": "Invalid username or password"})

    return render(request, "login.html")


def get_salary(request):
    token = request.GET.get("token")

    if not token or token not in active_tokens:
        return render(request, "wrong.html")

    token_data = active_tokens[token]
    username = token_data["username"]
    created_at = token_data["created_at"]
    elapsed_time = datetime.now() - created_at
    token_lifetime = timedelta(minutes=1)

    if elapsed_time > token_lifetime:
        del active_tokens[token]
        return render(request, "expired.html")

    user_data = users_db.get(username)

    if user_data:
        salary = user_data["salary"]
        next_raise = user_data["next_raise"]

        return render(request, "salary.html", {"salary": salary, "next_raise": next_raise})
    else:
        return HttpResponseNotFound("User not found")



def index(request):
    return render(request, "login.html")


def generate_token():
    return secrets.token_hex(16)


def token(request):
    return redirect("login")


def index(request):
    return redirect("login")

def expired(request):
    return render(request, "expired.html")