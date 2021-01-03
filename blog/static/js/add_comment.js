import { addCommentsToPage } from './get_comments.js'

const form = $('.comment-form')

form.submit((e) => {
    e.preventDefault()

    const formData = new FormData(e.target)
    formData.append('post_id', e.target.dataset.postid)

    $.ajax({
        data: formData,
        type: e.target.method,
        url: e.target.dataset.url,
        processData: false,
        contentType: false,

        success: function (result, status, xhr) {

            if (result.status != 'success'){
                console.log('An error occurred')
                return
            }

            const requestUserID = e.target.dataset.userid

            addCommentsToPage([result.comment])
            sessionStorage.removeItem("comments")

        }
    })

})