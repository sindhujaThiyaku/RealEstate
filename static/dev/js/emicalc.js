$(document).ready(function(){
    $("#loangetinfo").click(function(){
	    var p = parseFloat($("#loanAmount").val())
		var r = parseFloat($("#interestRate").val())
		var n= Math.round($("#loanduration").val())
		var duration = $('input:radio[name="tenure"]:checked').val()
		var loanFrom = $('#loanfrom').val()
		data = {'principal':p,'interest':r,'duration':n,'fromemi':loanFrom,'durationType':duration,csrfmiddlewaretoken:getCookie('csrftoken')}
	    resultdata = ajaxCall('get','/emi/emi_result/',data,false)
	    if(resultdata.status=="Success"){
	    	console.log("resultdata===========>",resultdata)
	    }
    });
});


function ajaxCall(type,url,data,async){
	var status;
	$.ajax({
		type:type,
		url:url,
		data:data,
		async:async,
	}).done(function(json_data){
			status = json_data;
	});
	return status;
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}