$(function () {
    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    $("#id_cover_photo").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#modalCoverPhotoCrop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    $("#modalCoverPhotoCrop").on("shown.bs.modal", function () {
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1980/300,
            minCropBoxWidth: 50,
            minCropBoxHeight: 50,
            ready: function () {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        });
    }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    });

    $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
    });

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#modalCoverPhotoCrop").modal("hide");
        $("#coverphotoUpload").submit();
    });

});

$("#coverphotoUpload").submit(function (event) {
    event.preventDefault()

    const form = $("#coverphotoUpload")[0]
    let formData = new FormData(form)
    const postURL = form.dataset.url

    console.log('form submitted')
    $.ajax({
        data: formData,
        type: $(this).attr('method'),
        url: postURL,
        processData: false,
        contentType: false,
        success: function (result, status, xhr) {
            if (status == 'success') {
                const photo = $(".cover_photo__img")[0]
                photo.src = result.photo_url
            }
        },
    })
})