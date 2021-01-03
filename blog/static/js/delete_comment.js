export function deleteComment(e){
    e.preventDefault()
    const id = e.target.dataset.commentid

    const url = e.target.dataset.url
    const commentId = e.target.dataset.commentid
    const csrfToken = $('.comments-list')[0].dataset.csrf

    const formData = new FormData(e.target)
    formData.append('comment_id', commentId)
    formData.append('csrfmiddlewaretoken', csrfToken)

    $.ajax({
        data: formData,
        type: 'POST',
        url: url,
        processData: false,
        contentType: false,

        success: function (result, status, xhr) {

            const comment = $(`.comment-${commentId}`)
            comment.remove()
            sessionStorage.removeItem("comments")

            const counter = $('.comment-count')[0]
            counter.innerText = parseInt(counter.innerText) - 1
        }
    })
}