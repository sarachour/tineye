
function disasm(code) {
  if (!code)
    return code;
  var codes = code.match(/(..?)/g);
  
  var dis = "";
  for(var i = 1; i < codes.length; i++) {
    var opcode = opcodes[codes[i]];
    
    if (!opcode) {
      dis = dis + "Missing opcode \n";
    } else if (opcode.substr(0, 4) === "PUSH") {
      var length = parseInt(opcode.replace("PUSH", ""));
      dis = dis + opcode + " 0x" + codes.slice(i + 1, i + length + 1).join("") + "\n";
      i = i + length;
    } else {
      dis = dis + opcode + "\n" ;
    }    
  }
  
  return dis;
}

