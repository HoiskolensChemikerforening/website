from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist

from chemie.customprofile.forms import GetRFIDForm
from chemie.customprofile.models import Profile, ProfileManager
from .forms import (
    RefillBalanceForm,
    AddCategoryForm,
    AddItemForm,
    HappyHourForm,
    EditItemForm,
)
from .models import Item, ShoppingCart, Category, Order, HappyHour
from decimal import InvalidOperation
from django.utils import timezone


def is_happy_hour():
    now = timezone.now()
    try:
        latest_happy_hour = HappyHour.objects.latest("id")
        diff = now - latest_happy_hour.created
        time_active_seconds = diff.total_seconds()
        time_active_minutes = time_active_seconds / 60
        time_active_hours = time_active_minutes / 60
        if time_active_hours < latest_happy_hour.duration:
            is_happy = True
            time_left_hours = (
                float(latest_happy_hour.duration) - time_active_hours
            )
            time_left_minutes = time_left_hours * 60
        else:
            is_happy = False
            time_left_minutes = None
        return is_happy, time_left_minutes
    except HappyHour.DoesNotExist:
        return False, False


def get_last_year_receipts():
    all_receipts = Order.objects.all()
    now = timezone.now()
    # Get 11 months back
    first_date = timezone.datetime(
        year=now.year - 1, month=now.month + 1, day=1
    )
    receipts = all_receipts.filter(created__gte=first_date, created__lte=now)
    months, m, i = 12, 0, 0
    year, month = now.year, now.month
    item_list = []
    while i < months:
        # Get the receipts at current_month - m
        if (month - m) > 0:
            month_c = month - m
        else:
            year = now.year - 1
            month, month_c = 12, 12
            m = 0
        current_receipts = receipts.filter(
            created__year=year, created__month=month_c
        )
        item_list.append({})
        for r in current_receipts:
            for order_item in r.items.all():
                if order_item.item.name not in item_list[i]:
                    item_list[i][order_item.item.name] = order_item.quantity
                else:
                    item_list[i][order_item.item.name] += order_item.quantity
        m += 1
        i += 1
    return item_list


@login_required
def index(request):
    if request.user.username == "tabletshop":
        context = index_tabletshop(request)
    else:
        context = index_user(request)
    return render(request, "shop/shop.html", context)


def index_user(request):
    is_tablet_user = False
    rfid_form = None
    items = Item.get_active_items()
    try:
        happy_category = Category.objects.get(name="Happy Hour")
        happy_items = Item.objects.filter(category=happy_category)
        items = items.exclude(id__in=happy_items.values("pk"))
    except Category.DoesNotExist:
        pass
    categories = Category.objects.all()
    cart = ShoppingCart(request)
    context = {
        "items": items,
        "categories": categories,
        "cart": cart,
        "is_tablet_user": is_tablet_user,
        "rfid_form": rfid_form,
    }
    if request.method == "POST":
        if "buy" in request.POST:
            post_str = request.POST["buy"]
            item_id, quantity = post_str.split("-")
            if int(quantity) <= 0:
                return context
            item = get_object_or_404(Item, pk=item_id)
            cart.add(item, quantity=int(quantity))
            is_happy = is_happy_hour()
            if is_happy:
                duplicate = item.happy_hour_duplicate
                if duplicate:
                    cart.add(duplicate, quantity=int(quantity))
        if "checkout" in request.POST:
            balance = request.user.profile.balance
            total_price = cart.get_total_price()
            if balance < total_price:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Du har itj nok HC-coin, kiis",
                    extra_tags="Nei!",
                )
            else:
                cart.buy(request)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Kontoen din er trukket {} HC-coins".format(total_price),
                    extra_tags="Kjøp godkjent",
                )
                context["cart"] = cart
    return context


def index_tabletshop(request):
    is_tablet_user = True
    rfid_form = GetRFIDForm(request.POST or None)
    items = Item.get_active_items()
    try:
        happy_category = Category.objects.get(name="Happy Hour")
        happy_items = Item.objects.filter(category=happy_category)
        items = items.exclude(id__in=happy_items.values("pk"))
    except Category.DoesNotExist:
        pass
    categories = Category.objects.all()
    cart = ShoppingCart(request)
    context = {
        "items": items,
        "categories": categories,
        "cart": cart,
        "is_tablet_user": is_tablet_user,
        "rfid_form": rfid_form,
    }
    if request.method == "POST":
        if "buy" in request.POST:
            post_str = request.POST["buy"]
            item_id, quantity = post_str.split("-")
            if int(quantity) <= 0:
                return context
            item = get_object_or_404(Item, pk=item_id)
            cart.add(item, quantity=int(quantity))
            is_happy = is_happy_hour()
            if is_happy:
                duplicate = item.happy_hour_duplicate
                if duplicate:
                    cart.add(duplicate, quantity=int(quantity))
        if "checkout" in request.POST:
            try:
                rfid = request.POST["rfid"]
                access_card = ProfileManager.rfid_to_em(rfid)
                buyer = Profile.objects.get(access_card=access_card)
                balance = buyer.balance
                total_price = cart.get_total_price()
                if balance < total_price:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "Du har itj nok HC-coin, kiis",
                        extra_tags="Nei!",
                    )
                else:
                    cart.buy(request)
                    new_balance = balance - total_price
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        (
                            "Kontoen din er trukket {} HC-coin. Du har igjen",
                            " {} HC-coin".format(total_price, new_balance),
                        ),
                        extra_tags="Kjøp godkjent",
                    )
                context["cart"] = cart
            except ObjectDoesNotExist:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Studentkort ikke registrert, Gå inn på {}".format(
                        reverse("profile:edit")
                    ),
                    extra_tags="Ups",
                )
    return context


# TODO: Change this to a custom permission?
@permission_required("customprofile.refill_balance")
def admin(request):
    order_items = get_last_year_receipts()
    items = Item.objects.all()
    item_list = [item.name for item in items]
    return render(
        request,
        "shop/admin.html",
        {
            "order_items": order_items,
            "items": item_list,
            "order_items": order_items,
        },
    )


@permission_required("customprofile.refill_balance")
def refill(request):
    provider = request.user
    form = RefillBalanceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            receiver = form.cleaned_data.get("receiver")
            amount = form.cleaned_data.get("amount")
            try:
                receiver.profile.balance += amount
                receiver.profile.save()
            except InvalidOperation:
                messages.add_message(
                    request,
                    messages.ERROR,
                    (
                        "Brukeren vil få mer enn 9999 HC-coins på "
                        "konto om du fyller på med beløpet."
                    ),
                    extra_tags="Feil",
                )
                return render(
                    request, "shop/refill-balance.html", {"form": form}
                )
            instance = form.save(commit=False)
            instance.provider = provider
            instance.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Du har fylt på {} HC-coins til brukeren {}".format(
                    amount, receiver.username
                ),
                extra_tags="Suksess",
            )
    return render(request, "shop/refill-balance.html", {"form": form})


@permission_required("shop.add_item")
def add_item(request):
    form = AddItemForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            form.save()
    items = Item.objects.all()
    context = {"form": form, "items": items}
    return render(request, "shop/add_item.html", context)


@permission_required("shop.edit_item")
def edit_item(request, pk):
    item = Item.objects.get(pk=pk)
    form = EditItemForm(
        request.POST or None, request.FILES or None, instance=item
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Varen ble endret.",
                extra_tags="Endret!",
            )
            return redirect(reverse("shop:add-item"))
    context = {"form": form}
    return render(request, "shop/edit_item.html", context)


@permission_required("shop.add_category")
def add_category(request):
    form = AddCategoryForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
    categories = Category.objects.all()
    context = {"form": form, "categories": categories}
    return render(request, "shop/add_category.html", context)


@login_required
def remove_item(request, pk):
    item = Item.objects.get(pk=pk)
    cart = ShoppingCart(request)
    cart.remove(item)
    return JsonResponse({"success": 1})


def activate_happyhour(request):
    form = HappyHourForm(request.POST or None)
    try:
        is_happy, time_left_minutes = is_happy_hour()
        if is_happy:
            messages.add_message(
                request,
                messages.WARNING,
                f"Det er {round(time_left_minutes)} minutter igjen",
                extra_tags="Happy Hour er allerede aktivert!",
            )
            return redirect(reverse("shop:admin"))
        return create_happyhour(request, form)
    except HappyHour.DoesNotExist:
        print("Ingen Happy Hour objekter eksisterer")
        return create_happyhour(request, form)
    except:
        messages.add_message(
            request,
            messages.WARNING,
            "Vi har en teknisk feil og vil prøve å rette opp i det",
            extra_tags="Vennligst ta kontakt med Webkom",
        )
        context = {"form": form}
        return render(request, "shop/happy-hour.html", context)


def create_happyhour(request, form):
    if request.method == "POST":
        if form.is_valid():
            user = request.user
            instance = form.save(commit=False)
            instance.provider = user
            instance.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Happy Hour aktivert!",
                extra_tags=f"Aktivert i {instance.duration} time(r)",
            )
            return redirect(reverse("shop:admin"))
    context = {"form": form}
    return render(request, "shop/happy-hour.html", context)
