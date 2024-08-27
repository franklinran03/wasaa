function likePost(postId) {
    $.ajax({
        url: '/post/' + postId + '/like/',
        type: 'POST',
        data: {
            'post_id': postId,
            'csrfmiddlewaretoken': csrfToken // Usa la variable csrfToken
        },
        success: function(response) {
            // Actualiza el contador de likes con la nueva cantidad
            $('#likes-count-' + postId).text('Likes: ' + response.total_likes);
        }
    });
}

