const API_URL = "http://127.0.0.1:5000/api/books/";

function loadBooks() {
    fetch(API_URL)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("books-list");
            list.innerHTML = "";

            data.forEach(book => {
                const li = document.createElement("li");
                li.innerHTML = `
                    <span>
                        <b>${book.title}</b> by ${book.author} (${book.year || "N/A"})
                    </span>
                    <div class="actions">
                        <button onclick="deleteBook(${book.id})">Delete</button>
                    </div>
                `;
                list.appendChild(li);
            });
        });
}

document.getElementById("book-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const book = {
        title: title.value,
        author: author.value,
        isbn: isbn.value,
        year: year.value ? parseInt(year.value) : null
    };

    fetch(API_URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(book)
    }).then(() => {
        this.reset();
        loadBooks();
    });
});

function deleteBook(id) {
    fetch(API_URL + id, { method: "DELETE" })
        .then(() => loadBooks());
}

loadBooks();
