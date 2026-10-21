document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("menuToggle");
    const nav = document.getElementById("navLinks");
    if (toggle && nav) {
        toggle.addEventListener("click", () => nav.classList.toggle("nav-open"));
    }

    const search = document.getElementById("productSearch");
    const cards = Array.from(document.querySelectorAll(".product-card"));
    const noResults = document.getElementById("noResults");
    if (search) {
        search.addEventListener("input", () => {
            const term = search.value.trim().toLowerCase();
            let visible = 0;
            cards.forEach(card => {
                const matches = (card.dataset.name + " " + card.dataset.description).includes(term);
                card.hidden = !matches;
                if (matches) visible += 1;
            });
            if (noResults) noResults.hidden = visible !== 0;
        });
    }

    document.querySelectorAll(".message").forEach(message => {
        window.setTimeout(() => {
            message.classList.add("message-hide");
            window.setTimeout(() => message.remove(), 350);
        }, 4500);
    });
});
