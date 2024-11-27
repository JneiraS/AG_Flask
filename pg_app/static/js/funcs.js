export function getData(endpoint, callback) {
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

export function slugify(text) {
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
