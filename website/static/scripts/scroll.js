$('.scroll').on('click', function(e) {
    if (this.has !== '') {
        e.preventDefault();

        const hash = this.hash

        $('html, body').animate(
            {
                scrollTop: $(hash).offset().top
            },
            1000
        );
    }
})