function copyToClipboard(value) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val("Hello World").select();
    //value.select();
    console.log(value);
    document.execCommand("copy");
    $temp.remove();
}