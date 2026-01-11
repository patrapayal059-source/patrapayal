// const API_URL = "/api/books"; // relative URL works in Codespaces

// // Load books and display in table
// async function loadBooks() {
//     const res = await fetch(API_URL);
//     const data = await res.json();

//     const tbody = document.querySelector("#booksTable tbody");
//     tbody.innerHTML = "";

//     data.forEach(book => {
//         const tr = document.createElement("tr");
//         tr.innerHTML = `
//             <td>${book.title}</td>
//             <td>${book.author}</td>
//             <td>${book.isbn}</td>
//             <td>${book.year || "N/A"}</td>
//         `;
//         tbody.appendChild(tr);
//     });
// }

// // Add new book
// document.getElementById("bookForm").addEventListener("submit", async function(e) {
//     e.preventDefault();

//     const book = {
//         title: document.getElementById("title").value,
//         author: document.getElementById("author").value,
//         isbn: document.getElementById("isbn").value,
//         year: document.getElementById("year").value ? parseInt(document.getElementById("year").value) : null
//     };

//     const res = await fetch(API_URL, {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify(book)
//     });

//     if(res.ok) {
//         this.reset();
//         loadBooks();
//     } else {
//         alert("Failed to save book");
//     }
// });

// // Search filter
// document.getElementById("search").addEventListener("input", () => {
//     const filter = document.getElementById("search").value.toLowerCase();
//     document.querySelectorAll("#booksTable tbody tr").forEach(row => {
//         row.style.display = row.textContent.toLowerCase().includes(filter) ? "" : "none";
//     });
// });

// // Load books on page load
// window.addEventListener("DOMContentLoaded", loadBooks);
