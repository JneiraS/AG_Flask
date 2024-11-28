import { getData, slugify } from "./funcs.js";


// Classe abstraite de base pour les API
export class AbstractAPI {
  static showResponse(data) {
    throw new Error("La méthode showResponse doit être implémentée");
  }
}

export class BookAPI extends AbstractAPI {
  static getBookByTitle(title) {
    const sluggedValue = slugify(title);

    const endpoint = `api/books/${sluggedValue}`; // Utilise le slug pour l'API
    return getData(endpoint, this.showResponse);
  }

  static getBookById(bookId) {
    const endpoint = `api/books/${bookId}`; // Utilise l'ID pour l'API
    return getData(endpoint, this.showResponse);
  }

  static showResponse(data) {
    const debugCard = document.querySelector(".book-by-id-card");
    let codes = debugCard.querySelector(".boock-cta");
    const response = JSON.parse(data);
    let html = "";
    if (response.book) {
      html += `<h1>${response.book.title}</h1><br>`;
      html += `<p><strong>isbn:</strong> ${response.book.isbn}</p>`;
      html += `<p><strong>Nombre de pages:</strong> ${response.book.number_of_pages}</p>`;
      html += `<p><strong>Prix:</strong> ${response.book.price}</p>`;
      html += `<p><strong>Date de publication:</strong> ${response.book.publication_date}</p><br>`;
      html += `<p>${response.book.summary}</p>`;
    } else {
      html += `<p>Données non disponibles</p>`;
    }
    codes.innerHTML = html;
  }
}

export class SelectionAPI extends AbstractAPI {

  static getBookBySelection(selection) {
    const endpoint = `api/selection/${selection}`; // Utilise le numero de selection
    console.log(endpoint);
    return getData(endpoint, this.showResponse);
  }

  static showResponse(data) {
    const response = JSON.parse(data);
    const debugCard = document.querySelector(".book-selection");
    let code = debugCard.querySelector(".selection-cta");
    let html = "";
    if (response.books) {
      Object.keys(response.books).forEach((bookTitle) => {
        const book = response.books[bookTitle];
        html += `<div class="book-element">`;
        html += `<br><h2>${bookTitle}</h2><br>`;
        html += `<p><strong>ISBN:</strong> ${book.isbn}</p>`;
        html += `<p><strong>Nombre de pages:</strong> ${book.number_of_pages}</p>`;
        html += `<p><strong>Prix:</strong> ${book.price}</p>`;
        html += `<p><strong>Date de publication:</strong> ${book.publication_date}</p><br>`;
        html += `<p>${book.summary}</p>`;
        html += `</div>`;
      });
    } else {
      html += `<p>Données non disponibles</p>`;
    }
    code.innerHTML = html;
  }

  static async addBookToSelection(selectionId, bookId) {
    const bookIdsArray = bookId.split(',');
    const endpoint = `api/selection/${selectionId}`;
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "book_ids" : bookIdsArray})
    });

    if (!response.ok) {
      throw new Error(`Failed to add book: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    const debugCard = document.querySelector(".add-book-to-selection");
    const messageElement = debugCard.querySelector(".selection-cta");

    if (result.success) {
      messageElement.innerHTML = `<p>Book ${bookId} added to selection ${selectionId} successfully.</p>`;
    } else {
      messageElement.innerHTML = `<p>${result.message || 'Unknown error'}</p>`;
    }
  }


}