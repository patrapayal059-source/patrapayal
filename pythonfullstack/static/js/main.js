document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".delete-book").forEach(btn => {
        btn.addEventListener("click", () => {
            const id = btn.dataset.id;

            if (confirm("Are you sure you want to delete this book?")) {
                fetch(`/delete_book/${id}`)
                    .then(() => location.reload());
            }
        });
    });
});

console.log("Library Management System Loaded");
