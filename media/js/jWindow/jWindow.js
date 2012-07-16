(function($) {
    
    var methods = {
        init : function(options) {

            var settings = {
                content:'grupos.html'
                ,loadingText:'<div class="loadingDiv">Carregando...</div>'
                ,params:{}
            };
            // build main options before element iteration
            opts = $.extend(settings, options);

            // iterate and reformat each matched element
            return this.each(function() {
                $this = $(this);
                // build element specific options
                var o = $.meta ? $.extend({}, opts, $this.data()) : opts;

                // Check to see if the modal exists!
                $modal = $this.find('.jWindowModal');
                $content = $this.find('.jWindowContent');
                if($modal.length <= 0 && $content.length <= 0) {
                    // If not exists create de modal and add that to de DOM
                    $this.append(''+
                        '<div class="jWindowModal"></div>'+
                        '<div class="jWindowContent">'+
                                '<div id="jWindowContentDiv"></div>'+
                                '<div id="jWindowContentClose" class="iconBtn orange rounded-border"><div class="imgClose"></div></div>'+
                        '</div>'
                    );
                    // Get the modal!!
                    $modal = $this.find('.jWindowModal');
                    $content = $this.find('.jWindowContent');
                }
                $modal.height($(document).height());
                // Modal opacity is set
                $modal.fadeTo('fast', 0.65);
                // Show the window
                $.fn.jWindow('show');
                $modal.bind('click', function() {
                    $.fn.jWindow('close');
                });
            });
        }

        ,show : function() {
            $modal.fadeIn('slow');
            $content.css("top", ( $(window).height() - $content.height() ) / 2+$(window).scrollTop() + "px");
            $content.find('#jWindowContentDiv').empty();
            $content.find('#jWindowContentDiv').append(opts.loadingText);
            $content.fadeIn('slow', function() {
                $(this).find('#jWindowContentDiv').load(opts.content, opts.params);
            });
            $this.find('#jWindowContentClose').bind('click', function() {
                $.fn.jWindow('close');
            });
        }

        ,close: function() {
            $modal.fadeOut('fast');
            $content.fadeOut('fast', function() {
                $content.find('#jWindowContentDiv').empty();
            });
        }

        ,destroy: function() {
            $modal.remove();
            $content.remove();
        }
    };

    $.fn.jWindow = function(method) {

        if(methods[method]) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            //$.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );
            return methods['init'].apply( this, Array.prototype.slice.call( arguments, 1 ));
        }

    };

})(jQuery);
