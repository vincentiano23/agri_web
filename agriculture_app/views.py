from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Product, PoultryInventory, EggProduction, CartItem, Produce
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ProductForm, ContactForm



# Home Page
@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')

# About Page (Requires Login)
@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')

# Contact Page (Requires Login)
@login_required(login_url='login')
def contact(request):
    return contact_view(request)  # Use the contact_view function for handling form submissions

# Projects Page (Requires Login)
@login_required(login_url='login')
def projects(request):
    return render(request, 'projects.html')

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, f"Registration successful! Welcome, {user.username}")
            return redirect('home')  
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Login successful! Welcome back, {user.username}")
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page after logout

# Upload Product (Requires Login)
@login_required(login_url='login')
def upload_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Product uploaded successfully!")
                return redirect('home')  # Change to the URL name for your product list or homepage
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            # Display form errors for better debugging
            messages.error(request, "Failed to upload product. Please check the form.")
    else:
        form = ProductForm()
    
    return render(request, 'upload_product.html', {'form': form})

# Product List
@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1  # Increment quantity if already in cart
        cart_item.save()
    
    messages.success(request, f"{product.name} added to cart!")
    return redirect('product_list')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated {cart_item.product.name} quantity!")
        else:
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.name} from cart.")
    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, f"Removed {cart_item.product.name} from cart.")
    return redirect('view_cart')

# Contact View
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect('contact')  
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

@login_required(login_url='login')
def farm_dashboard(request):
    total_produce = EggProduction.objects.aggregate(total_produce=Sum('eggs_raised'))['total_produce'] or 0
    total_poultry = PoultryInventory.objects.aggregate(
        total_poultry=Sum('broilers_male') + Sum('broilers_female') + 
                      Sum('layers_female') + Sum('kienyeji_male') + Sum('kienyeji_female')
    )['total_poultry'] or 0
    total_sales = total_produce * 10  # Example: 10 Ksh per egg

    poultry_inventory = PoultryInventory.objects.all()
    egg_production = EggProduction.objects.all()
    

    context = {
        'total_produce': total_produce,
        'total_poultry': total_poultry,
        'total_sales': total_sales,
        'poultry_inventory': poultry_inventory,
        'egg_production': egg_production,
      
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def record_produce(request):
    success_message = None

    if request.method == 'POST':
        produce_type = request.POST.get('produce_type')
        quantity = request.POST.get('produce_quantity')

        if produce_type and quantity:
            Produce.objects.create(produce_type=produce_type, quantity=quantity)
            success_message = f"{quantity} Kg of {produce_type} recorded successfully!"

    return render(request, 'record_produce.html', {'success_message': success_message})

@login_required(login_url='login')
def poultry_management(request):
    success_message = None

    # Handle Inventory Form Submission
    if request.method == 'POST' and 'broilers_male' in request.POST:
        broilers_male = request.POST.get('broilers_male')
        broilers_female = request.POST.get('broilers_female')
        layers_female = request.POST.get('layers_female')
        kienyeji_male = request.POST.get('kienyeji_male')
        kienyeji_female = request.POST.get('kienyeji_female')

        # Update or create inventory
        inventory, created =  PoultryInventory.objects.get_or_create(id=1)
        inventory.broilers_male = broilers_male
        inventory.broilers_female = broilers_female
        inventory.layers_female = layers_female
        inventory.kienyeji_male = kienyeji_male
        inventory.kienyeji_female = kienyeji_female
        inventory.save()

        success_message = "Inventory updated successfully!"

    # Handle Egg Production Form Submission
    if request.method == 'POST' and 'eggs_raised' in request.POST:
        eggs_raised = request.POST.get('eggs_raised')
        EggProduction.objects.create(total=eggs_raised)
        success_message = "Egg production recorded successfully!"

    inventory =  PoultryInventory.objects.first()
    egg_production = EggProduction.objects.last()

    context = {
        'inventory': inventory,
        'egg_production': egg_production,
        'success_message': success_message
    }

    return render(request, 'poultry_management.html', context)