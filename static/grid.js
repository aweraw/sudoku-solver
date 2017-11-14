
function coords() {
    var syms = "abcdefghi";
    var cs = new Array();
    for (y = 0; y < syms.length; y++) {
	for (x = 0; x < syms.length; x++) {
	    cs.push(syms.charAt(y).concat(syms.charAt(x)));
	}
    }
    return cs;
}

function serialize() {
    var s = '';
    $('#grid input[type=text]').each(function () {
	    if (this.value=='') {
		s += '0';
	    } else {
		s += this.value.replace(/^[\s]+|[\s]+$/g, '');
	    }
	});
    $.get('/solve/'+s, update);
}

function update(data) {
    var ids = coords();
    if (data.match(/^[0-9]{81}$/)) {
	for (i = 0; i < ids.length; i++) {
	    document.getElementById(ids[i]).value = data.charAt(i);
	}
    } else {
	alert(data);
    }
}
