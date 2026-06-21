from django import forms 
from .models import Item

# Suas classes de estilização do Tailwind
INPUT_CLASSES = 'w-full py-3.5 px-4 rounded-xl border border-slate-200 bg-slate-50/50 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:bg-white transition-all duration-200 text-sm'

class NewItemForm(forms.ModelForm):
    class Meta:
    
        model = Item
        fields = ['category', 'name', 'description', 'price', 'image']       
        
        # 1. TRADUÇÃO DOS CAMPOS (Labels)
        labels = {
            'category': 'Categoria',
            'name': 'Nome do Item',
            'description': 'Descrição',
            'price': 'Preço',
            'image': 'Imagem do Produto',
        }

        # 2. ESTILIZAÇÃO COMPLETA COM TAILWIND (Widgets)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Bicicleta Aro 29...',
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Conte detalhes sobre o estado do produto, tamanho, etc.',
                'class': INPUT_CLASSES,
                'rows': 4 # Limita a altura inicial da caixa de texto
            }),
            'price': forms.TextInput(attrs={
                'placeholder': '0.00',
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full py-2.5 px-4 rounded-xl border border-slate-200 text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition-all text-sm'
            }),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'image', 'is_sold']       
        
        labels = {
            'category': 'Categoria',
            'name': 'Nome do Item',
            'description': 'Descrição',
            'price': 'Preço',
            'image': 'Imagem do Produto',
            'is_sold': 'Item Vendido?',
        }

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Bicicleta Aro 29...',
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Conte detalhes sobre o estado do produto, tamanho, etc.',
                'class': INPUT_CLASSES,
                'rows': 4 # Limita a altura inicial da caixa de texto
            }),
            'price': forms.TextInput(attrs={
                'placeholder': '0.00',
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full py-2.5 px-4 rounded-xl border border-slate-200 text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition-all text-sm'
            }),
            'is_sold': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500 focus:ring-offset-0 transition-all cursor-pointer'
            })
        }