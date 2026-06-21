from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from item.models import Item
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm  

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    
    # Se o dono do item tentar abrir conversa com ele mesmo, manda pro dashboard
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    # Busca se já existe uma conversa deste usuário sobre este item específico
    conversations = Conversation.objects.filter(item=item, members__in=[request.user.id])

    # SE JÁ EXISTIR: Redireciona o usuário direto para a página de detalhes daquela conversa
    if conversations.exists():
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # Cria a nova conversa e adiciona os dois membros (comprador e vendedor)
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            # Salva a mensagem atrelando ela à conversa e ao autor
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('conversation:detail', pk=conversation.id)
    else:
        form = ConversationMessageForm()
        
    return render(request, 'conversation/new.html', {
        'form': form,
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })

@login_required
def detail(request, pk):
    # Garante que o usuário só consiga ver os detalhes se ele for um dos membros da conversa
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save() # Atualiza o status/modificação da conversa

            return redirect('conversation:detail', pk=pk)
    else:
        # CORRIGIDO: Agora este 'else' pertence ao 'if request.method == "POST"'
        # Garante que o formulário vazio seja criado em acessos normais (GET)
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })