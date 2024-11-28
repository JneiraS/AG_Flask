import { BookAPI, SelectionAPI } from "./api_request.js";

export class RequestForm {
  constructor() {
    this.debugCard = document.querySelector(".book-by-id-card");
    this.form = this.debugCard.querySelector(".debug-form");
    this.initializeButtons();
  }

  initializeButtons() {
    this.clearButton = this.form.querySelector("button[data-action='clear']");
    this.clearButton.addEventListener("click", this.handleClearClick.bind(this));
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

export class RequestSelection extends RequestForm {
  constructor() {
    super();
    this.debugCard = document.querySelector(".book-selection");
    this.form = this.debugCard.querySelector(".debug-form");
    this.initializeButtons();
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

export class RequestAddBookToSelection extends RequestForm {
  constructor() {
    super();
    this.debugCard = document.querySelector(".add-book-to-selection");
    this.form = this.debugCard.querySelector(".debug-form");
    this.initializeButtons();
  }

  handleClearClick(event) {
    event.preventDefault();
    let code = this.debugCard.querySelector(".add-selection-cta");
    code.innerText = "";
  }

  handleSendClick(event) {
    event.preventDefault();
    const input = document.querySelector(
      ".add-book-to-selection input[name='selection_id']"
    );
    const input_id = document.querySelector(".add-book-to-selection #book-id");
    console.log(`Valeur entrée pour la sélection: ${input.value}`); 
    console.log(`Valeur entrée pour l'ID du livre: ${input_id.value}`); 
    SelectionAPI.addBookToSelection(input.value, input_id.value);
  }
}