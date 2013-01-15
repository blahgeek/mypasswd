g = function(passwd, domain){
    var t = function(s){
        for(var i = 0 ; i < 10 ; i ++){
            var sha = new jsSHA(s, 'TEXT');
            s = sha.getHash('SHA-512', 'HEX');
        }
        return s;
    }
    passwd = t(passwd);
    var ret = t(passwd+domain);
    ret = function(s){
        var b = '';
        var ret = '';
        for(var i = 0 ; i < s.length ; i ++){
            var tmp= parseInt(s.substr(i, 1), 16).toString(2);
            if(i!=0)while(tmp.length < 4) tmp = '0' + tmp;
            b += tmp;
        }
        for(var i = 0 ; i < b.length - b.length%6; i += 6)
            ret += String.fromCharCode(parseInt(b.substr(i, 6), 2) + 63);
        return ret;
    }(ret);
    var ret_lines = '';
    for(var i = 0 ; i < ret.length-ret.length%10; i += 10){
        if(ret_lines.length != 0) ret_lines += '\n';
        ret_lines += ret.substr(i, 10);
    }
    return ret_lines;
}

c = function(){
    var res = g(document.getElementById('password').value, document.getElementById('domain').value);
    var code = '<code>' + res + '</code>';
    document.getElementById('results').innerHTML = code;
}
