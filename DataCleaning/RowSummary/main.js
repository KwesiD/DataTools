let table;
let newTable;
let tableRow;
let tableCol;
let maxRow;
let maxCol;
let outwb;
let inputName;
let client = new XMLHttpRequest();
let colName = document.getElementsByName("col_name")[0];

function mod(n, m) {
  return ((n % m) + m) % m;
}

function addElementBuilder(text){
	return function(){
		let summaryText = document.getElementsByName("summarized_text")[0];
		if(summaryText.value == ""){
			summaryText.value += text;
		}
		else{
			summaryText.value += ";"+text;
		}
		newTable[tableRow][tableCol] = summaryText.value;
	}

}

function go(){
	let summaryArea = document.getElementsByName("summarized_text")[0]; 
	let originalArea = document.getElementsByName("original_text")[0];
	let rowNum = document.getElementsByName("rowNum")[0]; 
	let colNum = document.getElementsByName("colNum")[0];
	let row = mod(rowNum.value,maxRow); 
	let col = mod(colNum.value,maxCol);
	rowNum.value = row;
	colNum.value = col;
	originalArea = table[row][col];
	summaryArea.value = newTable[row][col];
}

function onChangeListener(){
	let summaryText = document.getElementsByName("summarized_text")[0];
	newTable[tableRow][tableCol] = summaryText.value;
	console.log(summaryText.value);
}

var sheet2arr = function(sheet){
   var result = [];
   var row;
   var rowNum;
   var colNum;
   var range = XLSX.utils.decode_range(sheet['!ref']);
   for(rowNum = range.s.r; rowNum <= range.e.r; rowNum++){
      row = [];
       for(colNum=range.s.c; colNum<=range.e.c; colNum++){
          var nextCell = sheet[
             XLSX.utils.encode_cell({r: rowNum, c: colNum})
          ];
          if( typeof nextCell === 'undefined' ){
             row.push(void 0);
          } else row.push(nextCell.w);
       }
       result.push(row);
   }
   return result;
};

function arr2sheet(arr){
	return XLSX.utils.aoa_to_sheet(arr);
}


function nextEntry(){
	let summaryArea = document.getElementsByName("summarized_text")[0]; 
	let originalArea = document.getElementsByName("original_text")[0];
	temp1 = tableCol;
	temp2 = tableRow;
	tableCol = mod(tableCol+1,maxCol);
	if(tableCol === 0){
		tableRow = mod(tableRow+1,maxRow);
	}
	if(tableRow === 0){
		tableRow = 1;
	}
	while(table[tableRow][tableCol] == undefined){
		tableCol = mod(tableCol+1,maxCol);
		if(tableCol === 0){
			tableRow = mod(tableRow+1,maxRow);
		}
		if(tableRow === 0){
			tableRow = 1;
		}
	}
/*	if(temp1 != -1){
		newTable[temp2][temp1] = summaryArea.value; 
	}*/
	originalArea.value = table[tableRow][tableCol];
	summaryArea.value = newTable[tableRow][tableCol];
	let rowDiv = document.getElementsByName("rowNum")[0];
	let colDiv = document.getElementsByName("colNum")[0];
	rowDiv.value = /*"Row: " +*/ tableRow;
	colDiv.value = /*"Col: " + */tableCol;
	colName.innerHTML = table[0][tableCol];
}

function prevEntry(){
	let summaryArea = document.getElementsByName("summarized_text")[0]; 
	let originalArea = document.getElementsByName("original_text")[0];
	temp1 = tableCol;
	temp2 = tableRow;
	tableCol = mod(tableCol-1,maxCol);
	if(tableCol === maxCol-1){
		//tableCol = maxCol;
		tableRow = mod(tableRow-1,maxRow);
	}
	if(tableRow === 0){
		tableRow = maxRow;
	}
/*	if(temp1 != -1){
		newTable[temp2][temp1] = summaryArea.value; 
	}*/
	originalArea.value = table[tableRow][tableCol];
	summaryArea.value = newTable[tableRow][tableCol];
	let rowDiv = document.getElementsByName("rowNum")[0];
	let colDiv = document.getElementsByName("colNum")[0];
	rowDiv.value = /*"Row: " +*/ tableRow;
	colDiv.value = /*"Col: " +*/ tableCol;
	colName.innerHTML = table[0][tableCol];
}

function save(){
	outwb.Sheets["Sheet1"] = arr2sheet(newTable);
	console.log(outwb);
	XLSX.writeFile(outwb, "new_"+inputName);
}

var rABS = true; // true: readAsBinaryString ; false: readAsArrayBuffer

function handleInputFile(e) {
  var files = e.target.files, f = files[0];
  inputName = f.name;
  var reader = new FileReader();
  reader.onload = function(e) {
    var data = e.target.result;
    if(!rABS) data = new Uint8Array(data);
    var workbook = XLSX.read(data, {type: rABS ? 'binary' : 'array'});
 	var sheet = workbook.Sheets[Object.keys(workbook.Sheets)[0]];
 	//console.log(sheet);
 	table = sheet2arr(sheet);
 	maxRow = table.length;
	maxCol = table[0].length;
	tableRow = 0;
	tableCol = -1;
	newTable = new Array(maxRow).fill(0).map(() => new Array(maxCol).fill(""));
	newTable[0] = table[0];
	outwb = XLSX.utils.book_new();
	outwb.SheetNames.push("Sheet1");

    /* DO SOMETHING WITH workbook HERE */
  };
  if(rABS) reader.readAsBinaryString(f); else reader.readAsArrayBuffer(f);
}

function handleOutputFile(e) {
  var files = e.target.files, f = files[0];
  var reader = new FileReader();
  reader.onload = function(e) {
    var data = e.target.result;
    if(!rABS) data = new Uint8Array(data);
    var workbook = XLSX.read(data, {type: rABS ? 'binary' : 'array'});
 	var sheet = workbook.Sheets[Object.keys(workbook.Sheets)[0]];
 	//console.log(sheet);
 	newTable = sheet2arr(sheet);
 	newTable[0] = table[0];
	outwb = XLSX.utils.book_new();
	outwb.SheetNames.push("Sheet1");
	outwb.Sheets["Sheet1"] = arr2sheet(newTable);
    /* DO SOMETHING WITH workbook HERE */
  };
  if(rABS) reader.readAsBinaryString(f); else reader.readAsArrayBuffer(f);
}


client.open('GET', "issues.txt",false);
client.onload = function() {
  var list = client.responseText.split("\n"); 
  	var menu = document.getElementsByName("issues_menu")[0];
	list.forEach(function(e){
		var newCard = document.createElement("div")
		newCard.className = "menu_card";
		newCard.innerHTML = e;
		newCard.addEventListener("click",addElementBuilder(e));
		menu.appendChild(newCard);
	});
}
client.send();


client.open('GET',"actions.txt",false);
client.onload = function() {
  var list = client.responseText.split("\n"); 
  	var menu = document.getElementsByName("actions_menu")[0];
	list.forEach(function(e){
		var newCard = document.createElement("div")
		newCard.className = "menu_card";
		newCard.innerHTML = e;
		newCard.addEventListener("click",addElementBuilder(e));
		menu.appendChild(newCard);
	});
}
client.send();

/*client.open('GET', 'actions.txt');
client.onload = function() {
  let actionList = client.responseText.split("\n");
  console.log(actionList);
}
client.send();
*/

input_dom_element = document.getElementsByName("load_sheet_button")[0];
input_dom_element.addEventListener('change', handleInputFile, false);

output_dom_element = document.getElementsByName("load_output_sheet_button")[0];
output_dom_element.addEventListener('change', handleOutputFile, false);

// let summaryArea = document.getElementsByName("summarized_text")[0]; 
// let originalArea = document.getElementsByName("original_area")[0];

let nextButton = document.getElementsByName("next")[0];
nextButton.addEventListener("click",nextEntry);

let prevButton = document.getElementsByName("prev")[0];
prevButton.addEventListener("click",prevEntry);

var summaryText = document.getElementsByName("summarized_text")[0];
summaryText.addEventListener("input",onChangeListener);

let saveButton = document.getElementsByName("save")[0];
saveButton.addEventListener("click",save);

let goButton = document.getElementsByName("go")[0];
goButton.addEventListener("click",go);