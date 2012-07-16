function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};

function load(object, url, loadScript, scriptUrl) {
	object.empty();
	object.append("<div class='homeScreenLoad'><div></div></div>");
    object.load(url, function() { if(loadScript) { $.getScript(scriptUrl); } });
};

function loadApostas() {
	var idJogo = 0;
	var apostas = $(".apostas");
	for(var i=0; i<apostas.length; i++) {
		idJogo = $(apostas[i]).attr("id");
		$(("#"+idJogo)).load('./apostas/', {'idJogo':idJogo});
	}
};

function loadAposta(idJogo) {
	$(("#"+idJogo)).load('./apostas/', {'idJogo':idJogo});
};

$("#inicio").on("click", function() {
	load($("#conteudo-interno"), "./jogo/", false, "");
});
$("#pontuacao").on("click", function() {
	load($("#conteudo-interno"), "./pontuacao/", false, "");
});
$("#ranking").on("click", function() {
	load($("#conteudo-interno"), "./ranking/", false, "");
});

//Evento para persistir agora e no futuro os buttons de apostas
$("body").on("click", ".btnApostar", function() {
	var idJogo = $(this).attr("id");
	$("body").jWindow({content:"./formulario/", params: {"idJogo":idJogo}, loadingText:"<div class='homeScreenLoad'><div></div></div>"});
});