function getData(endpoint, callback) {
  const request = new XMLHttpRequest();
  request.onload = () => {
    if (request.status === 200) {
      callback(request.response);
    } else {
      console.error(`Erreur lors de la récupération des données : ${request.status}`);
    }
  };
  request.open("GET", endpoint);
  request.send();
}

function slugify(text) {
  return text
    .toString()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-') // Remplace les espaces par des tirets
    .replace(/[^\w-]+/g, '') // Supprime les caractères non alphanumériques
    .replace(/--+/g, '-'); // Remplace les doubles tirets par un seul
}

class BookAPI {
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
      html += `<h1>${response.book.title}</h1>`;
      html += `<p>isbn: ${response.book.isbn}</p>`;
      html += `<p>Nombre de pages: ${response.book.number_of_pages}</p>`;
      html += `<p>Prix: ${response.book.price}</p>`;
      html += `<p>Date de publication: ${response.book.publication_date}</p>`;
      html += `<p>${response.book.summary}</p>`;
    } else {
      html += `<p>Données non disponibles</p>`;
    }
    code.innerHTML = html;
  }
}

class DebugForm {
  constructor() {
    this.debugCard = document.querySelector(".book-by-id-card");
    this.form = this.debugCard.querySelector(".debug-form");
    this.clearButton = this.form.querySelector("button[data-action='clear']");
    this.clearButton.addEventListener(
      "click",
      this.handleClearClick.bind(this)
    );
    this.sendButton = this.form.querySelector("button[data-action='read']");
    this.sendButton.addEventListener("click", this.handleSendClick.bind(this));
  }

  handleClearClick(event) {
    event.preventDefault();
    let code = this.debugCard.querySelector(".boock-cta");
    code.innerText = "";
  }

  handleSendClick(event) {
    event.preventDefault();
    const input = document.querySelector(".book-by-id-card input");
    const isId = !isNaN(input.value); // Vérifie si la valeur est un nombre
    console.log(`Valeur entrée: ${input.value}`);
    if (isId) {
      BookAPI.getBookById(input.value); // Appelle la méthode pour obtenir le livre par ID
    } else {
      BookAPI.getBookByTitle(input.value); // Appelle la méthode pour obtenir le livre par titre
    }
  }
}

new DebugForm();