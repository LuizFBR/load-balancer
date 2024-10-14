var fs = require('fs');


function file_system() {
}

file_system.writeObjToFile = function (obj,file_path) {
    serialized_obj = JSON.stringify(obj,null,2)
    fs.writeFileSync(file_path,serialized_obj,
        { encoding: 'utf8', flag: 'w+' }
    )
}

file_system.readObjFromFile = function(file_path){
    let readObj = fs.readFileSync(file_path,
                        { encoding: 'utf8', flag: 'r' });
    let deserializedObj = JSON.parse(readObj)
    return deserializedObj
}

module.exports = {file_system};

// file_system.writeObjToFile({'a':{'b':[{'a':65},[5]] }},'test')
// test = file_system.readObjFromFile('test')
// console.log(test)
