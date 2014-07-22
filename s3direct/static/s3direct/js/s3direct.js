(function () {
    'use strict';

    var $s3Direct = jQuery.noConflict();

    $s3Direct(function () {

        var showControls = function ($el, className) {
            $el.find('.progress-controls').hide();
            $el.find('.link-controls').hide();
            $el.find('.form-controls').hide();
            $el.find(className).show();
        };

        var formatTime = function (seconds) {
            var date = new Date(seconds * 1000),
                days = Math.floor(seconds / 86400);
            days = days ? days + 'd ' : '';
            return days +
                ('0' + date.getUTCHours()).slice(-2) + ':' +
                ('0' + date.getUTCMinutes()).slice(-2) + ':' +
                ('0' + date.getUTCSeconds()).slice(-2);
        };

        var formatPercentage = function (floatValue) {
            return (floatValue * 100).toFixed(2) + ' %';
        };

        var attach = function ($fileInput, policy_url, el) {

            var $el = $s3Direct(el);

            $fileInput.fileupload({
                paramName: 'file',
                autoUpload: true,
                dataType: 'xml',
                add: function (e, data) {
                    $s3Direct(".submit-row input[type=submit]").prop('disabled', true);
                    showControls($el, '.progress-controls');

                    $s3Direct.ajax({
                        url: policy_url,
                        type: 'POST',
                        data: {
                            type: data.files[0].type,
                            name: data.files[0].name
                        },
                        success: function (fields) {
                            data.url = fields.form_action;
                            delete fields.form_action;
                            data.formData = fields;
                            var jqXHR = data.submit();
                            $el.find('.abort').on('click', function () {
                                jqXHR.abort();
                                showControls($el, '.form-controls');
                                $el.find('.progress-bar').css({width: '0%'});
                                $el.find('.info').text('');
                            })
                        }
                    });
                },

                progress: function (e, data) {
                    var progress = parseInt(data.loaded / data.total * 100, 10);
                    $el.find('.progress-bar').css({width: progress + '%'});
                    var infoText = formatTime((data.total - data.loaded) * 8 / data.bitrate) + ' | ' +
                        formatPercentage(data.loaded / data.total);
                    $el.find('.info').text(infoText);
                },

                done: function (e, data) {
                    if (data.textStatus === 'success') {
                        var url = $s3Direct(data.result).find('Location').text().replace(/%2F/g, '/');
                        var file_name = url.replace(/^.*[\\\/]/, '');
                        $el.find('.link').attr('href', url).text(file_name);
                        showControls($el, '.link-controls');
                        $el.find('input[type=hidden]').val(url);
                        $el.find('.progress-bar').css({width: '0%'});
                        $el.find('.info').text('');
                        $s3Direct(".submit-row input[type=submit]").prop('disabled', false);
                    } else {
                        showControls($el, '.form-controls');
                    }
                }
            });
        };

        var setup = function (el) {
            var $el = $s3Direct(el);

            var policy_url = $el.data('url');
            var file_url = $el.find('input[type=hidden]').val();
            var $fileInput = $el.find('input[type=file]');

            var class_ = (file_url === '') ? '.form-controls' : '.link-controls';
            showControls($el, class_);

            $el.find('.remove').click(function (e) {
                e.preventDefault();
                $el.find('input[type=hidden]').val('');
                showControls($el, '.form-controls');
            });

            attach($fileInput, policy_url, el);

            $el.addClass('initialized');
        };

        $s3Direct('.s3direct').each(function (i, el) {
            setup(el);
        });

        $s3Direct(document).bind('DOMNodeInserted', function (e) {
            var el = $s3Direct(e.target).find('.s3direct').not('.initialized').get(0);
            var yes = $s3Direct(el).length !== 0 && $s3Direct(el);
            if (yes) setup(el);
        })

    });
    $ = jQuery.noConflict();
})();