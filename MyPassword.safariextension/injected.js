if (window.top === window) {
    showMyPassword = function() {
        var width = '280px';

        var html = document.getElementsByTagName('html')[0];
        if(getComputedStyle(html).position === 'static')
            html.style.position = 'relative';
        var currentLeft = getComputedStyle(html).left;
        if(currentLeft === 'auto') currentLeft = 0;
        else currentLeft = parseFloat(currentLeft);
        html.style.left = currentLeft + parseFloat(width) + 'px';

        var iframeId = 'mypassword_Sidebar';
        if (document.getElementById(iframeId))
            return;
        html.innerHTML += '<iframe id="'+iframeId+'" scrolling="no" \
            frameborder="0" allowtransparency="false" \
            style="position: fixed; width: '+width+';border:none;\
            z-index: 2147483647; top: 0px; height: 100%;left: 0px;"\
            src="' + safari.extension.baseURI + 'iframe.html">\
            </iframe>';

    };

    safari.self.addEventListener("message", function(e){
        if (e.name === "showMyPassword")
            showMyPassword();
    }, false);

}
