import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { HttpClient } from '@angular/common/http';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule, HttpClientModule]
})
export class AppComponent {
  title = 'Chat Application';
  userId: string = '';
  chatId: string = '';
  userInput: string = '';
  messages: Message[] = [];

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (!this.userInput.trim()) return;

    // Add user message to chat
    this.messages.push({
      text: this.userInput,
      sender: 'user'
    });

    // Prepare API call parameters
    const payload = {
      query: this.userInput
    };

    // Make API call
    this.http.post<{system: string}>(`https://agent-communication-324653977572.us-central1.run.app?user_id=${this.userId}&chat_name=${this.chatId}`, payload)
      .subscribe({
        next: (response) => {
          // Add bot response to chat
          this.messages.push({
            text: response.system,
            sender: 'bot'
          });
        },
        error: (error) => {
          console.error('Error sending message', error);
          this.messages.push({
            text: 'Sorry, there was an error processing your message.',
            sender: 'bot'
          });
        }
      });

    // Clear input after sending
    this.userInput = '';
  }
}
