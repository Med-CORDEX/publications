var _____WB$wombat$assign$function_____ = function(name) {return (self._wb_wombat && self._wb_wombat.local_init && self._wb_wombat.local_init(name)) || self[name]; };
if (!self.__WB_pmw) { self.__WB_pmw = function(obj) { this.__WB_source = obj; return this; } }
{
  let window = _____WB$wombat$assign$function_____("window");
  let self = _____WB$wombat$assign$function_____("self");
  let document = _____WB$wombat$assign$function_____("document");
  let location = _____WB$wombat$assign$function_____("location");
  let top = _____WB$wombat$assign$function_____("top");
  let parent = _____WB$wombat$assign$function_____("parent");
  let frames = _____WB$wombat$assign$function_____("frames");
  let opener = _____WB$wombat$assign$function_____("opener");

function prepara() {		
		if ($(window).width() > 767) {
		    $("#mainmenu").show();
		    $("#mainmenu2").show();
		    $("#mainmenu3").show();
		    $("#mainmenub").show();
		    $("#mainmenub2").show();
		    $("#mainmenub3").show();
		} else {
		    
		    if ($('#content').height()>$(window).height()-100){
			$('#bottom').show();
		    }else{
			$('#bottom').hide();
		    }		  
		    
		    $("#mainmenu").hide();
		    $("#mainmenu2").hide();
		    $("#mainmenu3").hide();
		    $("#mainmenub").hide();
		    $("#mainmenub2").hide();
		    $("#mainmenub3").hide();
		}

}

function optionswitch(myfilter) {
    //            alert("sono optionswitch con myfilter="+myfilter);
    //Populate the optionstore if the first time through
	$("select[id^='sid_']").each(function() {
		var io = this.id;
		//	alert("1="+io);
		if ($('#optionstore_'+io).text() == "") {
		    optionlist = "@%" + "any" + "@%" + "any" + "@%" + "any";
		    $('#optionstore_'+io).text(optionlist)
		    $('select[id^="'+io+'"] option[class^="sub-"]').each(function() {
			    var optvalue = $(this).val();
			    var optclass = $(this).prop('class');
			    var opttext = $(this).text();
			    optionlist = $('#optionstore_'+io).text() + "@%" + optvalue + "@%" + optclass + "@%" + opttext;
			    $('#optionstore_'+io).text(optionlist);
			});
		}
		//alert($('#optionstore_'+io).text());
		//Delete everything
		$('select[id="'+io+'"] option[class^="sub-"]').remove();
		
		// Put the filtered stuff back
		populateoption = rewriteoption(myfilter,io);
		//		alert("popul="+populateoption);
		$('select[id="'+io+'"]').html(populateoption);
	    });
}

function rewriteoption(myfilter,io) {
    //Rewrite only the filtered stuff back into the option
    var options = $('#optionstore_'+io).text().split('@%');
    var resultgood = false;
    var myfilterclass = myfilter;
    var optionlisting = "";
    myfilterclass = (myfilter != "any")?myfilterclass:"any";
    //    alert ("rewrite io="+io+ " myfilter="+myfilter +" myfilterclass="+myfilterclass);
    //First variable is always the value, second is always the class, third is always the text
    for (var i = 3; i < options.length; i = i + 3) {
        if (options[i - 1] == myfilterclass || options[i - 1] == "any" || myfilterclass=="any") {
            resultgood = true;
            optionlisting = optionlisting + '<option value="' + options[i - 2] + '" class="' + options[i - 1] + '">' + options[i] + '</option>';
        }
    }
    if (resultgood) {
        return optionlisting;
    } else {
	alert ("rewrite io="+io+ " myfilter="+myfilter+" errore12");
    }
}

$(document).ready(function(){   

	$("#loading").hide();

	/* PROBLEMA
	  nel search_files se realm è passato come parametro ed è diverso da ANY
	   allora nelle options delle altre select troviamo sia quelle di A che quelle di O
	*/

	/*
	var cattype=$('#sidr_realm').find('option:selected').val();
	if (cattype!="any") {
		alert(cattype);
	optionswitch(cattype);
	}
	*/
	
	$('#sidr_realm').on("change",function() {
		var cattype=$(this).find('option:selected').attr('class');
		//	alert(cattype);
		optionswitch(cattype);
		$('#risultato').hide();
	    });


	$("select[id^='sid_']").on("change",function() {
		//		    alert("io");
		var optclassr = $('#sidr_realm').find('option:selected').prop('class');
		var optclass = $(this).find('option:selected').prop('class');
		var optval = $(this).find('option:selected').val();
		if (optclassr!=optclass) {
		    //    	    alert(this.id+" "+optclass+ " ma realm="+optclassr);
		    optionswitch(optclass);
		$('#sidr_realm option').filter(function() { 
			return ($(this).attr('class') == optclass); 
		    }).prop('selected', true);
		}
		$(this).val(optval);
		$('#risultato').hide();

	    });



	prepara();

	//When btn is clicked
	$(".btn-responsive-menu").click(function() {
		$("#mainmenu").toggleClass("show");
	    });
	/*
	  $(".btn-responsive-menub").click(function() {
	  $("#mainmenub").toggleClass("show");
	  });
	*/
	

	$("p[id^='btn-cap']").click(function() {
		var n=this.id.replace("btn-cap", "");
		$("div[id^='id-cap']").each(function(){
			var n1=this.id.replace("id-cap", "");
			if (n != n1) {
			    var b="#id-cap"+n1;
			    if (n.indexOf(n1) == -1) {
				//				    alert("n1="+n1+" "+n1.length);
				//  alert("n="+n+" "+n.length);
				    if  (n.length == n1.length) {
					//se e' un sottomenu non chiudere il suo "padre"
					$("#char-cap"+n1).html("<img src=\"/img/charapri.jpg\"> ");
					var isVisible = $(b).is(':visible');
					if (isVisible) {
					    //				alert(n+"  "+b);
					    $(b).toggleClass("show");
					};
				    };
			    };
			} else {
			    var a="#id-cap"+n;
			    //		    alert(a);
			    var isVisible = $(a).is(':visible');
			    if (isVisible) {
				$("#char-cap"+n).html("<img src=\"/img/charapri.jpg\"> ");
			    } else {
				//alert(a+"  "+b);
				$("#char-cap"+n).html("<img src=\"/img/charchiudi.jpg\"> ");
			    }
			    $(a).toggleClass("show");
			    window.location.href = "#btn-cap"+n;
			};
		    });
	    });

	/* non mi ricordo a che serve !!!!
	$("a[id^='btn-ind']").click(function() {
		var n=this.id.replace("btn-ind", "");
		$("div[id^='id-cap']").each(function(){
			var n1=this.id.replace("id-cap", "");
			if (n != n1) {
			    var b="#id-cap"+n1;
			    var isVisible = $(b).is(':visible');
			    if (isVisible) {
				//alert(a+"  "+b);
				$(b).toggleClass("show");
			    };
			} else {
			    var a="#id-cap"+n;
			    $(a).toggleClass("show");
			    window.location.href = "#id-cap"+n;
			};
		    });
	    });
	*/	
	$(".btn-responsive-menu2").click(function() {
		$("#mainmenu2").toggleClass("show");
		$("#mainmenub2").toggleClass("show");
	    });
	// When resize
	$(window).resize(function () {
		prepara();
	    });
    });
//Slider
$(window).load(function(){
	prepara();
	/*
	$('.flexslider').flexslider({
		animation: "slide",
		    start: function(slider){
		    $('body').removeClass('loading');
		}
	    });
	*/
   });


}
/*
     FILE ARCHIVED ON 21:56:52 Jun 12, 2024 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 09:53:19 Aug 13, 2025.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 0.964
  exclusion.robots: 0.037
  exclusion.robots.policy: 0.013
  esindex: 0.026
  cdx.remote: 530.798
  LoadShardBlock: 1199.906 (3)
  PetaboxLoader3.datanode: 860.588 (4)
  PetaboxLoader3.resolve: 563.556 (2)
  load_resource: 369.966
*/