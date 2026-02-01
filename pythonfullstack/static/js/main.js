// // ==========================================
// // Library Management System - Main JavaScript
// // ==========================================

// document.addEventListener("DOMContentLoaded", () => {
//     console.log("✅ Library Management System Loaded");

//     // ==========================================
//     // DELETE BOOK CONFIRMATION
//     // ==========================================
//     document.querySelectorAll(".delete-btn").forEach(btn => {
//         btn.addEventListener("click", (e) => {
//             if (!confirm("⚠️ Are you sure you want to delete this book?")) {
//                 e.preventDefault(); // Stop form submission if user cancels
//             }
//         });
//     });

//     // ==========================================
//     // DELETE USER CONFIRMATION
//     // ==========================================
//     document.querySelectorAll(".btn-danger").forEach(btn => {
//         btn.addEventListener("click", (e) => {
//             if (btn.textContent.includes("Delete")) {
//                 if (!confirm("⚠️ Are you sure you want to delete this user?")) {
//                     e.preventDefault();
//                 }
//             }
//         });
//     });

//     // ==========================================
//     // FORM VALIDATION
//     // ==========================================
    
//     // Book Form Validation
//     const bookForms = document.querySelectorAll(".book-form");
//     bookForms.forEach(form => {
//         form.addEventListener("submit", (e) => {
//             const inputs = form.querySelectorAll("input[required]");
//             let isValid = true;

//             inputs.forEach(input => {
//                 if (input.value.trim() === "") {
//                     isValid = false;
//                     input.style.borderColor = "red";
//                 } else {
//                     input.style.borderColor = "#cbd5e1";
//                 }
//             });

//             if (!isValid) {
//                 e.preventDefault();
//                 alert("❌ Please fill all required fields!");
//             }
//         });
//     });

//     // ==========================================
//     // SEARCH INPUT ENHANCEMENT
//     // ==========================================
//     const searchInputs = document.querySelectorAll("input[type='text']");
//     searchInputs.forEach(input => {
//         input.addEventListener("focus", () => {
//             input.style.borderColor = "#38bdf8";
//             input.style.boxShadow = "0 0 0 3px rgba(56, 189, 248, 0.1)";
//         });

//         input.addEventListener("blur", () => {
//             input.style.borderColor = "#cbd5e1";
//             input.style.boxShadow = "none";
//         });
//     });

//     // ==========================================
//     // AUTO-HIDE FLASH MESSAGES
//     // ==========================================
//     const flashMessages = document.querySelectorAll(".flash-message, .alert");
//     if (flashMessages.length > 0) {
//         setTimeout(() => {
//             flashMessages.forEach(msg => {
//                 msg.style.transition = "opacity 0.5s ease";
//                 msg.style.opacity = "0";
//                 setTimeout(() => msg.remove(), 500);
//             });
//         }, 5000); // Hide after 5 seconds
//     }

//     // ==========================================
//     // TABLE ROW HOVER EFFECT ENHANCEMENT
//     // ==========================================
//     const tableRows = document.querySelectorAll("table tbody tr");
//     tableRows.forEach(row => {
//         row.addEventListener("mouseenter", () => {
//             row.style.transform = "scale(1.01)";
//             row.style.transition = "all 0.2s ease";
//         });

//         row.addEventListener("mouseleave", () => {
//             row.style.transform = "scale(1)";
//         });
//     });

//     // ==========================================
//     // SMOOTH SCROLL FOR NAVIGATION
//     // ==========================================
//     document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//         anchor.addEventListener("click", function(e) {
//             e.preventDefault();
//             const target = document.querySelector(this.getAttribute("href"));
//             if (target) {
//                 target.scrollIntoView({
//                     behavior: "smooth",
//                     block: "start"
//                 });
//             }
//         });
//     });

//     // ==========================================
//     // BOOK CATEGORY FILTER (if exists)
//     // ==========================================
//     const categoryFilter = document.querySelector("#category-filter");
//     if (categoryFilter) {
//         categoryFilter.addEventListener("change", () => {
//             const category = categoryFilter.value;
//             const bookCards = document.querySelectorAll(".book-card");

//             bookCards.forEach(card => {
//                 if (category === "all" || card.dataset.category === category) {
//                     card.style.display = "block";
//                 } else {
//                     card.style.display = "none";
//                 }
//             });
//         });
//     }

//     // ==========================================
//     // INPUT CHARACTER COUNTER
//     // ==========================================
//     const textInputs = document.querySelectorAll("input[type='text'], textarea");
//     textInputs.forEach(input => {
//         if (input.hasAttribute("maxlength")) {
//             const maxLength = input.getAttribute("maxlength");
//             const counter = document.createElement("small");
//             counter.style.display = "block";
//             counter.style.textAlign = "right";
//             counter.style.color = "#64748b";
//             counter.style.marginTop = "4px";
            
//             input.parentNode.insertBefore(counter, input.nextSibling);

//             const updateCounter = () => {
//                 const remaining = maxLength - input.value.length;
//                 counter.textContent = `${input.value.length}/${maxLength} characters`;
//                 counter.style.color = remaining < 10 ? "#ef4444" : "#64748b";
//             };

//             input.addEventListener("input", updateCounter);
//             updateCounter();
//         }
//     });

//     // ==========================================
//     // LOADING INDICATOR FOR FORMS
//     // ==========================================
//     const forms = document.querySelectorAll("form");
//     forms.forEach(form => {
//         form.addEventListener("submit", (e) => {
//             const submitBtn = form.querySelector("button[type='submit']");
//             if (submitBtn && !form.classList.contains("no-loading")) {
//                 submitBtn.disabled = true;
//                 submitBtn.innerHTML = "⏳ Loading...";
//                 submitBtn.style.opacity = "0.6";
//             }
//         });
//     });

//     // ==========================================
//     // PRINT FUNCTIONALITY
//     // ==========================================
//     const printButtons = document.querySelectorAll(".print-btn");
//     printButtons.forEach(btn => {
//         btn.addEventListener("click", () => {
//             window.print();
//         });
//     });

//     // ==========================================
//     // DARK MODE TOGGLE (Optional Enhancement)
//     // ==========================================
//     const darkModeToggle = document.querySelector("#dark-mode-toggle");
//     if (darkModeToggle) {
//         darkModeToggle.addEventListener("click", () => {
//             document.body.classList.toggle("dark-mode");
//             localStorage.setItem("darkMode", 
//                 document.body.classList.contains("dark-mode")
//             );
//         });

//         // Load saved preference
//         if (localStorage.getItem("darkMode") === "true") {
//             document.body.classList.add("dark-mode");
//         }
//     }

//     // ==========================================
//     // TOOLTIP INITIALIZATION
//     // ==========================================
//     const tooltipElements = document.querySelectorAll("[data-tooltip]");
//     tooltipElements.forEach(element => {
//         element.addEventListener("mouseenter", (e) => {
//             const tooltip = document.createElement("div");
//             tooltip.className = "custom-tooltip";
//             tooltip.textContent = element.getAttribute("data-tooltip");
//             tooltip.style.position = "absolute";
//             tooltip.style.background = "#1e293b";
//             tooltip.style.color = "white";
//             tooltip.style.padding = "8px 12px";
//             tooltip.style.borderRadius = "6px";
//             tooltip.style.fontSize = "14px";
//             tooltip.style.zIndex = "1000";
//             tooltip.style.whiteSpace = "nowrap";

//             document.body.appendChild(tooltip);

//             const rect = element.getBoundingClientRect();
//             tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + "px";
//             tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + "px";

//             element._tooltip = tooltip;
//         });

//         element.addEventListener("mouseleave", () => {
//             if (element._tooltip) {
//                 element._tooltip.remove();
//                 delete element._tooltip;
//             }
//         });
//     });

//     // ==========================================
//     // REAL-TIME SEARCH (Optional)
//     // ==========================================
//     const searchBox = document.querySelector("#live-search");
//     if (searchBox) {
//         let searchTimeout;
//         searchBox.addEventListener("input", (e) => {
//             clearTimeout(searchTimeout);
//             searchTimeout = setTimeout(() => {
//                 const query = e.target.value.toLowerCase();
//                 const items = document.querySelectorAll(".searchable-item");

//                 items.forEach(item => {
//                     const text = item.textContent.toLowerCase();
//                     item.style.display = text.includes(query) ? "" : "none";
//                 });
//             }, 300);
//         });
//     }

// });

// // ==========================================
// // UTILITY FUNCTIONS
// // ==========================================

// // Show notification
// function showNotification(message, type = "info") {
//     const notification = document.createElement("div");
//     notification.className = `notification ${type}`;
//     notification.textContent = message;
//     notification.style.cssText = `
//         position: fixed;
//         top: 20px;
//         right: 20px;
//         padding: 15px 25px;
//         background: ${type === "success" ? "#22c55e" : type === "error" ? "#ef4444" : "#38bdf8"};
//         color: white;
//         border-radius: 8px;
//         box-shadow: 0 4px 12px rgba(0,0,0,0.15);
//         z-index: 9999;
//         animation: slideIn 0.3s ease;
//     `;

//     document.body.appendChild(notification);

//     setTimeout(() => {
//         notification.style.animation = "slideOut 0.3s ease";
//         setTimeout(() => notification.remove(), 300);
//     }, 3000);
// }

// // Format date
// function formatDate(dateString) {
//     const options = { year: 'numeric', month: 'long', day: 'numeric' };
//     return new Date(dateString).toLocaleDateString('en-US', options);
// }

// // Validate email
// function isValidEmail(email) {
//     const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//     return regex.test(email);
// }

// // Add animations CSS
// const style = document.createElement("style");
// style.textContent = `
//     @keyframes slideIn {
//         from {
//             transform: translateX(400px);
//             opacity: 0;
//         }
//         to {
//             transform: translateX(0);
//             opacity: 1;
//         }
//     }

//     @keyframes slideOut {
//         from {
//             transform: translateX(0);
//             opacity: 1;
//         }
//         to {
//             transform: translateX(400px);
//             opacity: 0;
//         }
//     }
// `;
// document.head.appendChild(style);

// console.log("🚀 All JavaScript features loaded successfully!");
