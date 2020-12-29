// Follow.js
//
// Used in profile_card.html
//
// Listens for a press of the follow button and sends an AJAX request to the server.
// Toggles the button state after a successful response from the server.

const form = $('#follow')
const button = $("#follow input[type='submit']")[0]

// Send follow/unfollow action to the server

form.submit((e) => {
    e.preventDefault()
    console.log('form submitted')
    console.log(e.target)

    const action = e.target.dataset.action
    const formData = new FormData(e.target)
    formData.append('id', e.target.dataset.id)
    formData.append('action', action)

    $.ajax({
        data: formData,
        type: e.target.method,
        url: e.target.dataset.url,
        processData: false,
        contentType: false,

        success: function (result, status, xhr) {
            if (status == 'success') {

                const followers = $("#follower_count")[0]
                let follower_count = parseInt(followers.innerText)

                // Toggle action
                if (action === 'follow') {
                    e.target.dataset.action = 'unfollow'
                    followers.innerText = follower_count + 1
                    button.value = 'Following'
                    button.blur()
                } else {
                    e.target.dataset.action = 'follow'
                    followers.innerText = follower_count - 1
                    button.value = 'Follow'
                    button.classList.remove('bg-danger')
                    button.classList.add('bg-primary')
                    button.blur()
                }

            }
        },
    })
})

// // Change to unfollow button on hover
if (button) {
    button.addEventListener('mouseover', (e) => {

        const action = form[0].dataset.action

        if (action === 'unfollow') {
            e.target.value = 'Unfollow'
            e.target.classList.remove('bg-primary')
            e.target.classList.add('bg-danger')
        }

    })
    button.addEventListener('mouseleave', (e) => {

        const action = form[0].dataset.action

        if (action === 'unfollow') {
            e.target.value = 'Following'
            e.target.classList.remove('bg-danger')
            e.target.classList.add('bg-primary')
        }
    })
}

