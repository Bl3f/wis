!function($){
    $('#X-Progress-ID').val('random string');
    var options = {
          dataType: 'xml',
            url: '/upload?X-Progress-ID='+$('#X-Progress-ID').val(),
              beforeSubmit: showRequest,
                success: showResponse
    }
    $('#form_upload').ajaxSubmit(options);
}(window.jQuery);
