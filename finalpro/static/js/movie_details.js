document.addEventListener("DOMContentLoaded", function() {
    var deleteBtn = document.getElementById("delete-btn");

    if (deleteBtn) {
        deleteBtn.addEventListener("click", function() {
            if (confirm("Are you sure you want to delete this movie?")) {
                var deleteForm = document.getElementById("delete-form");
                if (deleteForm) {
                    deleteForm.submit();
                }
            } else {
                // Redirect to the movie_detail page
                var movieId = deleteBtn.getAttribute("data-movie-id");
                if (movieId) {
                    window.location.href = "/shop/movie_detail/" + movieId;
                }
            }
        });
    }
});
