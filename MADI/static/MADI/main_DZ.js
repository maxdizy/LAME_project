const myDropzone= new Dropzone('#my-dropzone',{
    url: "MADI/upload/",
    maxFiles:1,
    maxFilesize:20,
    acceptedFiles:'.pdf',
})