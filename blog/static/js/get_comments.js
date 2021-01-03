import { deleteComment } from './delete_comment.js'

$(document).ready(function () {

    const commentsContainer = $('.comments-list')

    const url = commentsContainer[0].dataset.ajaxurl

    const cachedComments = sessionStorage.getItem("comments")

    if (cachedComments) {
        addCommentsToPage(JSON.parse(cachedComments))

    } else {
        $.ajax({
            type: 'GET',
            url: url,
            cache: true,
            success: function (result, status, xhr) {

                if (result.status != 'success') {
                    console.log('An error occurred')
                    return
                }

                const comments = result.comments
                sessionStorage.setItem("comments", JSON.stringify(comments))

                // Update comment count
                $('.comment-count')[0].innerText = comments.length
                addCommentsToPage(comments)

            }
        })
    }


});

export function addCommentsToPage(comments) {

    const commentsList = $('.comments-list')[0]
    const deleteURL = commentsList.dataset.deleteurl
    const requestUserID = commentsList.dataset.userid

    for (let i = 0; i < comments.length; i++) {

        const commentCard = document.createElement('div')

        commentCard.classList.add("card")
        commentCard.classList.add("mb-2")

        const comment = comments[i]

        commentCard.innerHTML = `
            <div class="card-header">
                <p class="m-0">By <b>${comment.user_from.first_name} ${comment.user_from.last_name}</b> <em class="float-right">${dayjs().to(dayjs(comment.timestamp))}</em></p>
            </div>
            <div class="card-body">
                ${comment.body}
            </div>
        `

        const commentFooter = document.createElement('div')
        commentFooter.classList.add('card-footer')

        if (requestUserID == comment.user_from.id) {
            commentFooter.innerHTML = `
                <form class="delete-comment-form" method="POST" data-url=${deleteURL} data-commentid=${comment.id}>
                    <input type="submit" value="delete" class="btn btn-outline-danger btn-sm">
                </form>
            `
        }

        commentCard.classList.add(`comment-${comment.id}`)
        commentCard.append(commentFooter)
        commentsList.append(commentCard)

    }

    const deleteForms = [...$('.delete-comment-form')]

    deleteForms.forEach(form => {
        form.addEventListener('submit', e => {
            deleteComment(e)
        })
    })

}
