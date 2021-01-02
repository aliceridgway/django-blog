const deleteCommentForm = $('.delete-comment-form')

deleteCommentForm.submit((e) => {
    e.preventDefault()

    const url = e.target.dataset.url
    const commentId = e.target.dataset.commentid

    const formData = new FormData(e.target)
    formData.append('comment_id', commentId)

    $.ajax({
        data: formData,
        type: e.target.method,
        url: e.target.dataset.url,
        processData: false,
        contentType: false,

        success: function (result, status, xhr) {

            const comment = $(`#comment-${commentId}`)
            comment.remove()

        }
    })
})