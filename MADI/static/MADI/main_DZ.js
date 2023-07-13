Dropzone.autoDiscover=false;
const myDropzone= new Dropzone('#my-dropzone',{
    url:'upload/',
    maxFiles:1,
    maxFilesize:20,
    acceptedFiles:'.pdf',
})