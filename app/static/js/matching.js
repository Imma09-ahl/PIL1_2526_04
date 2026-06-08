document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("matching-results");
    const filterSelect = document.getElementById("score-filter");
    const sortBtn = document.getElementById("sort-score-btn");

    // Animation fade-in
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }
            });
        },
        { threshold: 0.1 }
    );
    document.querySelectorAll(".fade-in").forEach((el) => observer.observe(el));

    if (!grid) return;

    const getCards = () => Array.from(grid.querySelectorAll(".matching-card"));

    const applyFilter = () => {
        const minScore = Number(filterSelect?.value || 0);
        getCards().forEach((card) => {
            const score = Number(card.dataset.score || 0);
            card.style.display = score >= minScore ? "" : "none";
        });
    };

    const applySort = () => {
        const cards = getCards();
        cards
            .sort((a, b) => Number(b.dataset.score) - Number(a.dataset.score))
            .forEach((card) => grid.appendChild(card));
    };

    filterSelect?.addEventListener("change", applyFilter);
    sortBtn?.addEventListener("click", applySort);

    applySort();
    applyFilter();
});