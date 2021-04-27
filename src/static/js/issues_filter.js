// filter the entries
const filterBtn = document.querySelector('#filter-button')

const converter = {
    "Code Smell": "CODE_SMELL",
    "Bug": "BUG",
    "Vulnerability": "VULNERABILITY"
}

const converter2  = {
    "CodeSmell": "CODE_SMELL",
    "Bug": "BUG",
    "Vulnerability": "VULNERABILITY"
}

const previous = eval('('+document.querySelector('#params').innerText+')')

console.log(previous["date"] !== [], previous["date"] == [])

function extractKeyValue(obj, value) {
    return Object.keys(obj)[Object.values(obj).indexOf(value)];
}

if(previous["type"].length != 0){
    Array.from(previous["type"]).forEach(val => {
        Array.from(document.querySelectorAll('.type')).forEach(element => {
            var key = extractKeyValue(converter2, val)
            console.log(element.parentElement.children[1].innerText.replace(/\s+/g, "") == key, element.parentElement.children[1].innerText.replace(/\s+/g, ""), key)
            if(element.parentElement.children[1].innerText.replace(/\s+/g, "") == key){
                element.checked = true
            }
        })
    })
}

if(previous["severity"].length != 0 ){
    Array.from(previous["severity"]).forEach(val => {
        Array.from(document.querySelectorAll('.severity')).forEach(element => {
            if(element.id == val.toLowerCase()){
                element.checked = true
            }
        })
    })
}

if(previous["languages"].length != 0){
    Array.from(previous["languages"]).forEach(val => {
        Array.from(document.querySelectorAll('.languages')).forEach(element => {
            if(element.id == "languages_"+val){
                element.checked = true
            }
        })
    })
}

if(previous["date"].length != 0){
    console.log('fire')
    let str1 = previous["date"][0]
    let li = []
    for(var i in str1){
        if(str1[i] == '-'){
            li.push(i)
        }
    }
    console.log(li)
    let year = str1.slice(0,li[0])
    let month = str1.slice(parseInt(li[0])+1, parseInt(li[1]))
    let day = str1.slice(parseInt(li[1])+1)
    let reformattedDate = `${month}/${day}/${year}`
    document.getElementById('startDate').value = reformattedDate

    let str2 = previous["date"][1]
    let li2 = []
    for(var i in str2){
        if(str2[i] == '-'){
            li2.push(i)
        }
    }
    let year2 = str2.slice(0,li2[0])
    let month2 = str2.slice(parseInt(li2[0])+1, parseInt(li2[1]))
    let day2 = str2.slice(parseInt(li2[1])+1)
    let reformattedDate2 = `${month2}/${day2}/${year2}`
    document.getElementById('endDate').value = reformattedDate2
}

filterBtn.addEventListener('click', e=>{
    let checkBoxes = document.querySelectorAll('.custom-control-input')
    let conditions = {"type":[], "severity":[], "languages":[], "date":[]}
    Array.from(checkBoxes).forEach(element => {
        if(element.checked==true){
            if(element.parentElement.children[1].innerText == "Bug" || element.parentElement.children[1].innerText=="Vulnerability" || element.parentElement.children[1].innerText=="Code Smell"){
                conditions["type"].push(element.parentElement.children[1].innerText)
            }
            else if(element.parentElement.children[1].innerText == "Info" || element.parentElement.children[1].innerText == "Minor" || element.parentElement.children[1].innerText == "Blocker" || element.parentElement.children[1].innerText == "Critical" || element.parentElement.children[1].innerText == "Major"){
                conditions["severity"].push(element.parentElement.children[1].innerText)
            }
            else if(element.id.includes('languages_')){
                conditions['languages'].push(element.id.slice(element.id.indexOf('_')+1))
            }
        }
    })
    if(document.getElementById('startDate').value != ''){
        let str = document.getElementById('startDate').value
        let li = []
        for(var i in str){
        if(str[i] == '/'){
            li.push(i)
        }
        }
        let month = str.slice(0,li[0])
        let day = str.slice(parseInt(li[0])+1, parseInt(li[1]))
        let year = str.slice(parseInt(li[1])+1)
        let reformattedDate = `${year}-${month}-${day}`
        conditions['date'].push(reformattedDate)
    }
    if(document.getElementById('endDate').value != ''){
        let str = document.getElementById('endDate').value
        let li = []
        for(var i in str){
        if(str[i] == '/'){
            li.push(i)
        }
        }
        let month = str.slice(0,li[0])
        let day = str.slice(parseInt(li[0])+1, parseInt(li[1]))
        let year = str.slice(parseInt(li[1])+1)
        let reformattedDate = `${year}-${month}-${day}`
        conditions['date'].push(reformattedDate)
    }
    console.log(conditions)
    let li = []
    let li2 = []
    conditions["type"].forEach(element => {
        li.push(converter[element])
    })
    conditions["severity"].forEach(element => {
        li2.push(element.toUpperCase())
    })
    conditions["type"] = li
    conditions["severity"] = li2
    $.ajax({
        "type": "get",
        "url": `/filters2?dict=${JSON.stringify(conditions)}`,
        "success": function(data){
            console.log(data)
            window.location.replace('/issuesfiltering')
        }
    })    
})

// Hiding the headers if every card was hidden after the filter 
let hideHeader = () => {
    const headers = document.querySelectorAll('.titles')
    Array.from(headers).forEach(header => {
        let count = 0
        let id = header.id
        let errors = document.getElementsByClassName(id)
        let total = errors.length
        Array.from(errors).forEach(element => {
            if(element.style.display == "none"){
                count += 1
            }
        })
        if(count == total){
            header.style.display = "none"
        } 
    })
}


// reset the filters
const resetFilterBtn = document.querySelector('#reset')

resetFilterBtn.addEventListener('click', event => {
    let checkboxes = document.querySelectorAll('.custom-control-input')
    Array.from(checkboxes).forEach(element => {
        element.checked = false;
    })
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
})

