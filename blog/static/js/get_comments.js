$( document ).ready(function() {

    const commentsContainer = $('.comments-list')

    const url = commentsContainer[0].dataset.ajaxurl

    cachedComments = sessionStorage.getItem("comments")

    if (cachedComments){
        addCommentsToPage(JSON.parse(cachedComments))

    } else{
        $.ajax({
            type: 'GET',
            url: url,
            cache: true,
            success: function (result, status, xhr) {

                if (result.status != 'success'){
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

function addCommentsToPage(comments){

    for (let i = 0; i<comments.length; i++){

        const commentCard = document.createElement('div')

        commentCard.classList.add("card")
        commentCard.classList.add("mb-2")

        const comment = comments[i]

        commentCard.innerHTML = `
            <div class="card-header">
                <p class="m-0">By <b>${comment.user_from.first_name} ${comment.user_from.last_name}</b> <em class="float-right"> TO DO: datejs</em></p>
            </div>
            <div class="card-body">
                ${comment.body}
            </div>
        `
        $('.comments-list').append(commentCard)
    }
}