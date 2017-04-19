( function ($) {
    $(document).ready(function () {
        var $toolbar = get_or_create('_itr_toolbar'),
            $dialog = get_or_create('_itr_dialog');

        $('._itr').on('click', function (e) {
            if ($(this).hasClass('show')) {
                e.preventDefault();
                e.stopPropagation();
                $trans_el = $(this);
                $.getJSON(get_poentry_url, {'msgid': $trans_el.data('msgid')}, function (data) {
                        $dialog.html(
                            '<div class="_itr_form">' +
                            '<h3>Translation form</h3>' +
                            '<table>' +
                            '<tr><td>source:</td><td>'+data.msgid+'</td></tr>' +
                            '<tr><td>context:</td><td>'+data.msgctxt+'</td></tr>' +
                            '<tr><td>translation:</td><td>' +
                            '<form action="'+update_poentry_url+'" method="post">' +
                                '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrf_token+'">' +
                                '<input type="hidden" name="msgid" value="'+data.msgid+'">' +
                                '<textarea name="msgstr">'+data.msgstr+'</textarea>' +
                                '<input type="submit" value="save translation"/>' +
                            '</form>'+
                            '</td></tr>' +
                            '</table>' +
                            '</div>'
                        );
                        $dialog.dialog();
                        console.log(data)
                    }
                );
            }
        });

        $toolbar.append("<ul><li><a href='#' class='all'>All</a></li><li><a href='#' class='not_translated'>Not translated</a></li><li><a href='#' class='hide selected'>Hide</a></li></ul>")

        $toolbar.find('.all').on('click', function (e) {
            e.preventDefault();
            $('._itr').addClass('show');
            $toolbar.find('a').removeClass('selected');
            $(this).addClass('selected');
        });

        $toolbar.find('.not_translated').on('click', function (e) {
            e.preventDefault();
            $('._itr').removeClass('show');
            $('._itr.not_translated').addClass('show');
            $toolbar.find('a').removeClass('selected');
            $(this).addClass('selected');
        });

        $toolbar.find('.hide').on('click', function (e) {
            e.preventDefault();
            $('._itr').removeClass('show');
            $toolbar.find('a').removeClass('selected');
            $(this).addClass('selected');
        });

    });

    function get_or_create(element_id) {
        var $el = $('#'+element_id);
        if ($el.length == 0) {
            $('body').prepend("<div id='"+element_id+"'></div>");
            $el = $('#'+element_id);
        }
        return $el;
    }

}(jQuery));
