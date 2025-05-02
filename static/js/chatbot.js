class CareerGPT {
    constructor() {
        this.messages = [];
        this.initChatbot();
    }
    
    initChatbot() {
        this.chatWindow = document.querySelector('.chatbot-messages');
        this.inputField = document.querySelector('.chatbot-input input');
        this.sendButton = document.querySelector('#send-message');
        
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        
        this.addBotMessage("Hello! I'm CareerGPT, your AI career assistant. How can I help you today?");
    }
    
    async sendMessage() {
        const userMessage = this.inputField.value.trim();
        if (!userMessage) return;
        
        this.addUserMessage(userMessage);
        this.inputField.value = '';
        
        // Show typing indicator
        const typingIndicator = this.addBotMessage("CareerGPT is typing...", true);
        
        // Simulate API call to backend
        setTimeout(() => {
            this.chatWindow.removeChild(typingIndicator);
            const botResponse = this.generateResponse(userMessage);
            this.addBotMessage(botResponse);
        }, 1000 + Math.random() * 2000); // Random delay for realism
    }
    
    addUserMessage(text) {
        this.messages.push({ sender: 'user', text });
        this.renderMessage('user', text);
    }
    
    addBotMessage(text, isTyping = false) {
        if (!isTyping) {
            this.messages.push({ sender: 'bot', text });
        }
        return this.renderMessage('bot', text, isTyping);
    }
    
    renderMessage(sender, text, isTyping = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender} ${isTyping ? 'typing' : ''}`;
        
        const avatar = sender === 'bot' 
            ? '<i class="fas fa-robot me-2"></i>' 
            : '<i class="fas fa-user me-2"></i>';
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-sender">${avatar}</div>
                <div class="message-text">${text}</div>
            </div>
        `;
        
        this.chatWindow.appendChild(messageDiv);
        this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
        return messageDiv;
    }
    
    generateResponse(userMessage) {
        const lowerMessage = userMessage.toLowerCase();
        
        if (lowerMessage.includes('career') || lowerMessage.includes('match')) {
            return "Based on your assessment, I recommend checking your career matches on the dashboard. Would you like me to explain any of them in detail?";
        }
        else if (lowerMessage.includes('skill') || lowerMessage.includes('improve')) {
            return "Looking at your profile, I'd suggest focusing on: <ul><li>Technical skills like Python</li><li>Communication workshops</li></ul>";
        }
        else {
            return "I can help with: <ul><li>Career matching</li><li>Skill improvement</li><li>Interview preparation</li></ul> What would you like to know?";
        }
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    new CareerGPT();
});