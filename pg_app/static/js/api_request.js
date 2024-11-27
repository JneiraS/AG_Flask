
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
    console.log(`Slug généré pour le titre "${title}": ${sluggedValue}`);
    const endpoint = `api/books/${sluggedValue}`; // Utilise le slug pour l'API
    return getData(endpoint, this.showResponse);
  }

  static getBookById(bookId) {
    const endpoint = `api/books/${bookId}`; // Utilise l'ID pour l'API
    return getData(endpoint, this.showResponse);
  }

  static showResponse(data) {
    const debugCard = document.querySelector(".book-by-id-card");
    let code = debugCard.querySelector(".boock-cta");
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
    code.innerHTML = html;
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

  static addBookToSelection(selection, bookId) {
    const endpoint = `api/selection/${selection}/${bookId}`; // Utilise le numero de selection et l'ID du livre
    fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ selection, bookId })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to load resource: the server responded with a status of ${response.status} (${response.statusText})`);
      }
      return response.json();
    })
    .then(data => {
        const debugCard = document.querySelector(".add-book-to-selection");
        let code = debugCard.querySelector(".selection-cta");
        code.innerHTML = `<p>Livre ${bookId} ajouté avec succès à la sélection ${selection}</p>`;
        console.log('Succès:', data);
    })
    .catch(error => {
        const debugCard = document.querySelector(".add-book-to-selection");
        let code = debugCard.querySelector(".selection-cta");
        code.innerHTML = `<p>Erreur: ${error.message}</p>`;
        console.error('Erreur détaillée:', error);
    });
}


}