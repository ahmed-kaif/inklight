document.addEventListener('DOMContentLoaded', function () {
    const seeMoreButtons = document.querySelectorAll('.see-more-button');

    seeMoreButtons.forEach(button => {
        button.addEventListener('click', function () {
            const container = this.closest('.truncate-container');
            container.classList.toggle('expanded');
        });
    });
});
