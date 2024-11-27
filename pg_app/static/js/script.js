import { BookAPI, SelectionAPI } from "./api_request.js";
// ... reste du code inchangé

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
  constructor() {
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

const requestByTitleorId = new RequestForm();
const requestSelection = new RequestSelection();
