$(document).ready(function(){

    setTimeout(function() {$('#clipboardModal').modal('hide');$('#shareModalDialog').modal('hide');}, 4000);
    $('#shareUrl').popover();

    $('.social-share-icon').click(function(){
        window.open(
            this.href,
            '', 
            'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600'
        );
        return false;
    });
});