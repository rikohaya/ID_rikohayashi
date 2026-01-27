let currentConversationId = null;
let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
    loadConversations();
    adjustTextareaHeight();
});

async function loadConversations() {
    try {
        const response = await fetch('/api/conversations');
        const conversations = await response.json();
        renderConversationsList(conversations);
    } catch (error) {
        console.error('Failed to load conversations:', error);
    }
}

function renderConversationsList(conversations) {
    const container = document.getElementById('conversationsList');
    container.innerHTML = '';

    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = `conversation-item ${conv.id === currentConversationId ? 'active' : ''}`;
        item.innerHTML = `
            <span class="conversation-title">${escapeHtml(conv.title)}</span>
            <button class="delete-btn" onclick="deleteConversation(event, ${conv.id})">
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                </svg>
            </button>
        `;
        item.onclick = (e) => {
            if (!e.target.closest('.delete-btn')) {
                selectConversation(conv.id);
            }
        };
        container.appendChild(item);
    });
}

async function createNewChat() {
    currentConversationId = null;
    document.getElementById('messagesContainer').innerHTML = `
        <div class="welcome-message" id="welcomeMessage">
            <h1>Gemini Chat</h1>
            <p>何でも聞いてください</p>
        </div>
    `;
    updateActiveConversation();
}

async function selectConversation(conversationId) {
    try {
        const response = await fetch(`/api/conversations/${conversationId}`);
        if (!response.ok) throw new Error('Failed to load conversation');

        const conversation = await response.json();
        currentConversationId = conversationId;

        renderMessages(conversation.messages);
        updateActiveConversation();
    } catch (error) {
        console.error('Failed to select conversation:', error);
    }
}

function renderMessages(messages) {
    const container = document.getElementById('messagesContainer');
    container.innerHTML = '';

    if (messages.length === 0) {
        container.innerHTML = `
            <div class="welcome-message" id="welcomeMessage">
                <h1>Gemini Chat</h1>
                <p>何でも聞いてください</p>
            </div>
        `;
        return;
    }

    messages.forEach(msg => {
        addMessageToUI(msg.role, msg.content);
    });

    scrollToBottom();
}

function addMessageToUI(role, content) {
    const container = document.getElementById('messagesContainer');

    const welcomeMessage = document.getElementById('welcomeMessage');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = role === 'user' ? 'U' : 'G';
    const formattedContent = formatMessage(content);

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">${formattedContent}</div>
    `;

    container.appendChild(messageDiv);
}

function formatMessage(content) {
    let formatted = escapeHtml(content);

    formatted = formatted.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
    formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    formatted = formatted.replace(/\n/g, '<br>');

    return formatted;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function sendMessage(event) {
    event.preventDefault();

    if (isLoading) return;

    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message) return;

    input.value = '';
    adjustTextareaHeight();

    addMessageToUI('user', message);
    scrollToBottom();

    isLoading = true;
    setLoadingState(true);

    const loadingDiv = addLoadingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: currentConversationId,
            }),
        });

        if (!response.ok) throw new Error('Failed to send message');

        const data = await response.json();

        loadingDiv.remove();

        if (!currentConversationId) {
            currentConversationId = data.conversation_id;
            await loadConversations();
        }

        addMessageToUI('assistant', data.assistant_message.content);
        scrollToBottom();

    } catch (error) {
        console.error('Failed to send message:', error);
        loadingDiv.remove();
        addMessageToUI('assistant', 'エラーが発生しました。もう一度お試しください。');
    } finally {
        isLoading = false;
        setLoadingState(false);
    }
}

function addLoadingIndicator() {
    const container = document.getElementById('messagesContainer');

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = `
        <div class="message-avatar">G</div>
        <div class="message-content">
            <div class="loading">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    container.appendChild(loadingDiv);
    scrollToBottom();

    return loadingDiv;
}

function setLoadingState(loading) {
    const button = document.getElementById('sendButton');
    const input = document.getElementById('messageInput');

    button.disabled = loading;
    input.disabled = loading;
}

async function deleteConversation(event, conversationId) {
    event.stopPropagation();

    if (!confirm('この会話を削除しますか？')) return;

    try {
        const response = await fetch(`/api/conversations/${conversationId}`, {
            method: 'DELETE',
        });

        if (!response.ok) throw new Error('Failed to delete conversation');

        if (currentConversationId === conversationId) {
            createNewChat();
        }

        await loadConversations();
    } catch (error) {
        console.error('Failed to delete conversation:', error);
    }
}

function updateActiveConversation() {
    const items = document.querySelectorAll('.conversation-item');
    items.forEach(item => {
        item.classList.remove('active');
    });

    if (currentConversationId) {
        const activeItem = document.querySelector(`.conversation-item[data-id="${currentConversationId}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }

    loadConversations();
}

function scrollToBottom() {
    const container = document.getElementById('messagesContainer');
    container.scrollTop = container.scrollHeight;
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage(event);
    }
}

function adjustTextareaHeight() {
    const textarea = document.getElementById('messageInput');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

document.getElementById('messageInput').addEventListener('input', adjustTextareaHeight);
