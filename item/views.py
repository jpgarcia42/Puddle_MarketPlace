from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .models import Category, Item
from .forms import NewItemForm, EditItemForm

def items(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()
    
    # CORRIGIDO: Pegamos o valor da URL e tentamos converter para inteiro de forma segura
    category_id = request.GET.get('category_id', 0)
    
    try:
        category_id = int(category_id)
    except (ValueError, TypeError):
        category_id = 0 # Caso venha algo bizarro na URL, resetamos para 0
        
    items = Item.objects.filter(is_sold=False)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # CORRIGIDO: Agora a comparação no banco de dados funciona porque category_id é um número de verdade
    if category_id:
        items = items.filter(category_id=category_id)
        
    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': category_id, # Removido o int() daqui pois já foi convertido acima
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3] 
    
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            return redirect('item:detail', pk=item.id) 
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Novo Item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            form.save() # CORRIGIDO: Alterado de item.save() para form.save() para aplicar as mudanças do formulário
            
            return redirect('item:detail', pk=item.id) 
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Editar Item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    
    return redirect('dashboard:index')