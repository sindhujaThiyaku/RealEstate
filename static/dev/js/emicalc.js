$(document).ready(function(){
	dataLoan = {'income':50000,'interest':1.5,'duration':2,'durationType':'Y','otherEmi':JSON.stringify(['1000','2000'])}
	resultdata = ajaxCall('post','/emi/emi_result/',dataLoan,false)
    if(resultdata.status=="Success"){
    	console.log("resultdata===========>",resultdata)
    }
    $("#loangetinfo").click(function(){
	    var p = parseFloat($("#loanAmount").val())
		var r = parseFloat($("#interestRate").val())
		var n= Math.round($("#loanduration").val())
		var duration = $('input:radio[name="tenure"]:checked').val()
		var loanFrom = $('#loanfrom').val()
		dataEmi = {'principal':p,'interest':r,'duration':n,'fromemi':loanFrom,'durationType':duration}
	    console.log(dataEmi)
	    resultdata = ajaxCall('post','/emi/emi_result/',dataEmi,false)
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