var initStr = "H4ck_th3_Univ3r5e".split('');
var curStr = "Hack_the_Universe".split('');
var variants = {
	'_': [],
	'G': ['6', 'g'],
	'U': ['u'],
	'n': ['&eta;'],
	'i': ['i', '&iuml;', 'I', '&Iacute;', '&Iuml;'],
	'v': ['v', '&radic;'],
	'r': ['Я', 'я', '&reg;'],
	'H': ['h'],
	'a': ['4', 'A', '&alpha;'],
	'c': ['c', 'C'],
	'e': ['3', 'E', 'ë', '€', '&epsilon;'],
	'h': ['H'],
	'k': ['&kappa;'],
	'l': ['L', '1', '|'],
	't': ['T', '7', '+', '&tau;'],
	'x': ['X', '&chi;'],
	'y': ['Y', '&phi;'],
}

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
function getRandomIntInclusive(min, max) {
	min = Math.ceil(min);
	max = Math.floor(max);
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

function countMutations(){
	var count = 0;
	var mutatedPositions = []
	for(var i = 0; i < curStr.length; i++){
		if(curStr[i] !== initStr[i]){
			count += 1;
			mutatedPositions.push(i);
		}
	}
	return {count: count, pos: mutatedPositions};
}

setInterval(function(){
//window.setInterval(function(){
	// Never allow more than 4 subsitutions
	var mutations = countMutations();
	if(mutations.count > 3){
		// ok, this is too many, let's roll one back.
		mutate_pos = mutations.pos[getRandomIntInclusive(0, mutations.pos.length - 1)];
		curStr[mutate_pos] = initStr[mutate_pos];
	} else {
		// Randomly mutate init str
		var mutate_pos = getRandomIntInclusive(0, initStr.length - 1);
		// Choices for that position:
		var choices = variants[initStr[mutate_pos]];
		if(choices && choices.length > 0){
			curStr[mutate_pos] = choices[getRandomIntInclusive(0, choices.length - 1)];
		}
	}

	//$("#htg").html(curStr.join(""));
	console.log(curStr.join(""))

}, 500);
