/**
 * Created by Zak on 2016/6/1.
 */
/*
 * jQuery.formFieldValues: Get or Set all of the name/value pairs from child Form input fields.
 * @argument data {array} If included, will populate all child Form input fields.
 * @returns element if data was provided, or array of values if not
 *
 * DEMO: http://codepen.io/jasondavis/pen/jsmya?editors=101
 */
$.fn.formFieldValues = function(data) {
    var els = this.find(':input').get();

    if(arguments.length === 0) {
        // return all data
        data = {};

        $.each(els, function() {
            if (this.name && !this.disabled && (this.checked
                || /select|textarea/i.test(this.nodeName)
                || /text|hidden|password/i.test(this.type))) {
                if(data[this.name] == undefined){
                    data[this.name] = [];
                }
                data[this.name].push($(this).val());
            }
        });
        return data;
    } else {
        $.each(els, function() {
            if (this.name && data[this.name]) {
                var names = data[this.name];
                var $this = $(this);
                if(Object.prototype.toString.call(names) !== '[object Array]'){
                    names = [names]; //backwards compat to old version of this code
                }
                if(this.type == 'checkbox' || this.type == 'radio') {
                    var val = $this.val();
                    var found = false;
                    for(var i = 0; i < names.length; i++){
                        if(names[i] == val){
                            found = true;
                            break;
                        }
                    }
                    $this.attr("checked", found);
                } else {
                    $this.val(names[0]);
                }
            }
        });
        return this;
    }
};