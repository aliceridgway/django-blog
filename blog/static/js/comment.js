console.log('hello from comment.js!')

const form = $('.comment-form')

form.submit((e) => {
    e.preventDefault()

    const url = e.target.dataset.url

    const formData = new FormData(e.target)
    formData.append('post_id', e.target.dataset.postid)

    $.ajax({
        data: formData,
        type: e.target.method,
        url: e.target.dataset.url,
        processData: false,
        contentType: false,

        success: function (result, status, xhr) {

            const firstName = e.target.dataset.firstname
            const lastName = e.target.dataset.lastname
            const commentBody = formData.get('body')

            const commentCard = document.createElement('div')
            commentCard.classList.add("card")
            commentCard.classList.add("mb-2")
            commentCard.innerHTML = `
                <div class="card-header">
                    <p class="m-0">By <b>${firstName} ${lastName}</b> <em class="float-right"> Just now</em></p>
                </div>
                <div class="card-body">
                    ${commentBody}
                </div>
            `
            $('.comments-list').append(commentCard)

        }
    })

})