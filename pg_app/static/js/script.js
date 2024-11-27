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
  const from = "àáäâèéëêìíïîòóöôùúüñçßÿỳ";
  const to = "aaaaeeeeiiiioooouuuuncsyy";
  const mapping = {};

  for (let i = 0; i < from.length; i++) {
    mapping[from.charAt(i)] = to.charAt(i);
  }

  const replacer = (char) => mapping[char] || char;

  return text
    .toString()
    .toLowerCase()
    .replace(/[\s\W_]/g, "-")
    .replace(/--+/g, "-")
    .replace(/[^\w-]+/g, "")
    .replace(/\u0300-\u036f/g, "")
    .replace(/[^\x00-\x7F]/g, "")
    .replace(/[^\w-]/g, replacer);
}


// Classe abstraite de base pour les API
class AbstractAPI {


  static showResponse(data) {
    throw new Error("La méthode showResponse doit être implémentée");
  }
}


class BookAPI extends AbstractAPI {
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

class SelectionAPI extends AbstractAPI {

  static getBookBySelection(selection) {
    const endpoint = `api/selection/${selection}`; // Utilise l'ID pour l'API
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
        html += `<h2>${bookTitle}</h2><br>`;
        html += `<p><strong>ISBN:</strong> ${book.isbn}</p>`;
        html += `<p><strong>Nombre de pages:</strong> ${book.number_of_pages}</p>`;
        html += `<p><strong>Prix:</strong> ${book.price}</p>`;
        html += `<p><strong>Date de publication:</strong> ${book.publication_date}</p><br>`;
        html += `<p>${book.summary}</p>`;
      });
    } else {
      html += `<p>Données non disponibles</p>`;
    }
    code.innerHTML = html;
  }


}

class RequestForm {
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

class RequestSelection extends RequestForm {
  constructor () {
    super();
    this.debugCard = document.querySelector(".book-selection");
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
    let code = this.debugCard.querySelector(".selection-cta");
    code.innerText = "";
  }

  handleSendClick(event) {
    event.preventDefault();
    const input = document.querySelector(".book-selection input");
    const isId = !isNaN(input.value); // Vérifie si la valeur est un nombre
    console.log(`Valeur entrée: ${input.value}`);
    if (isId) {
      SelectionAPI.getBookBySelection(input.value); // Appelle la méthode pour obtenir le livre par ID
    }
  }



}



const requestByTitleorId = new  RequestForm();
const requestSelection = new  RequestSelection();