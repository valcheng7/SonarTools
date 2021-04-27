// filter the entries
const filterBtn = document.querySelector('#filter-button')

const converter = {
    "a": "1.0",
    "b": "2.0",
    "c": "3.0",
    "d": "4.0",
    "e": "5.0"
}

const converter2 = {
    "pass": "Passed",
    "fail": "Failed"
}

const previous = eval('('+document.querySelector('#params').innerText+')')

function extractKeyValue(obj, value) {
    return Object.keys(obj)[Object.values(obj).indexOf(value)];
}

if(previous["size"] !== []){
    Array.from(previous["size"]).forEach(i => {
        if(i.length == 1){
            Array.from(document.querySelectorAll('.size')).forEach(element => {   
                if(element.id == "size_"+i[0]){
                    element.checked = true
                }
            })
        }
        else if(i.length == 2){
            Array.from(document.querySelectorAll('.size')).forEach(element => {   
                if(element.id == "size_"+i[0]+"_"+i[1]){
                    element.checked = true
                }
            })
        }
    })   
}

if(previous["coverage"] !== []){
    Array.from(previous["coverage"]).forEach(i => {
        if(i.length == 1){
            Array.from(document.querySelectorAll('.coverage')).forEach(element => {   
                if(element.id == "coverage_"+i[0]){
                    element.checked = true
                }
            })
        }
        else if(i.length == 2){
            Array.from(document.querySelectorAll('.coverage')).forEach(element => {   
                if(element.id == "coverage_"+i[0]+"_"+i[1]){
                    element.checked = true
                }
            })
        }
    })
}

if(previous["duplicatePercentage"] !== []){
    Array.from(previous["duplicatePercentage"]).forEach(i => {
        if(i.length == 1){
            Array.from(document.querySelectorAll('.duplication')).forEach(element => {   
                if(element.id == "duplications_"+i[0]){
                    element.checked = true
                }
            })
        }
        else if(i.length == 2){
            Array.from(document.querySelectorAll('.duplication')).forEach(element => {   
                if(element.id == "duplications_"+i[0]+"_"+i[1]){
                    element.checked = true
                }
            })
        }
    })
}

if(previous["securityReview"] !== []){
    Array.from(previous["securityReview"]).forEach(i=> {
        if(i.length == 1){
            Array.from(document.querySelectorAll('.securityReview')).forEach(element => {   
                if(element.id == "secR_"+i[0]){
                    element.checked = true
                }
            })
        }
        else if(i.length == 2){
            Array.from(document.querySelectorAll('.securityReview')).forEach(element => {   
                if(element.id == "secR_"+i[0]+"_"+i[1]){
                    element.checked = true
                }
            })
        }
    })
}

if(previous["status"] !== []){
    Array.from(previous["status"]).forEach(val => {
        var key = extractKeyValue(converter2, val)
        console.log(key)
        Array.from(document.querySelectorAll('.status1')).forEach(element => {   
            if(element.id == key){
                element.checked = true
            }
        })
    })
}

if(previous["bugs"] !== []){
    Array.from(previous["bugs"]).forEach(val => {
        var key = extractKeyValue(converter, val)
        console.log(key)
        Array.from(document.querySelectorAll('.bugs')).forEach(element => {   
            if(element.id == "bugs_"+key){
                element.checked = true
            }
        })
    })
}

if(previous["vulnerabilities"] !== []){
    Array.from(previous["vulnerabilities"]).forEach(val => {
        var key = extractKeyValue(converter, val)
        console.log(key)
        Array.from(document.querySelectorAll('.security')).forEach(element => {   
            if(element.id == "sec_"+key){
                element.checked = true
            }
        })
    })
}

if(previous["code_smells"] !== []){
    Array.from(previous["code_smells"]).forEach(val => {
        var key = extractKeyValue(converter, val)
        console.log(key)
        Array.from(document.querySelectorAll('.maintability')).forEach(element => {   
            if(element.id == "main_"+key){
                element.checked = true
            }
        })
    })
}

if(previous["languages"] !== []){
    Array.from(previous["languages"]).forEach(val => {
        Array.from(document.querySelectorAll('.languages')).forEach(element => {   
            if(element.id == "languages_"+val){
                element.checked = true
            }
        })
    })
}




filterBtn.addEventListener('click', event=> {
    let checkboxes = document.querySelectorAll('.custom-control-input')
    let conditions = {"status":[], "bugs":[], "vulnerabilities":[], "code_smells":[],"securityReview":[], "coverage":[], "size":[], "languages":[], "duplicatePercentage":[]};
    Array.from(checkboxes).forEach(element => {
        if(element.checked == true){
            if(element.id == "pass" || element.id == "fail"){
                conditions['status'].push(element.id)
            } 
            else if(element.id.includes('bugs')){
                conditions['bugs'].push(element.id.slice(element.id.indexOf('_')+1))
            }
            else if(element.id.includes('secR_')){
                let str = element.id.slice(element.id.indexOf('_')+1)
                if(str.indexOf('_') != -1){
                    conditions['securityReview'].push([str.slice(0, str.indexOf('_')), str.slice(str.indexOf('_')+1)])
                }else{
                conditions['securityReview'].push([str])
                }
            }
            else if(element.id.includes('coverage_')){
                let str = element.id.slice(element.id.indexOf('_')+1)
                if(str.indexOf('_') != -1){
                    conditions['coverage'].push([str.slice(0, str.indexOf('_')), str.slice(str.indexOf('_')+1)])
                }else{
                conditions['coverage'].push([str])
                }
            }
            else if(element.id.includes('size_')){
                let str = element.id.slice(element.id.indexOf('_')+1)
                if(str.indexOf('_') != -1){
                    conditions['size'].push([str.slice(0, str.indexOf('_')), str.slice(str.indexOf('_')+1)])
                }else{
                conditions['size'].push([str])
                }
            }
            else if(element.id.includes('duplications_')){
                let str = element.id.slice(element.id.indexOf('_')+1)
                if(str.indexOf('_') != -1){
                    conditions['duplicatePercentage'].push([str.slice(0, str.indexOf('_')), str.slice(str.indexOf('_')+1)])
                }else{
                    conditions['duplicatePercentage'].push([str])
                }
            }
            else if(element.id.includes('sec_')){
                conditions['vulnerabilities'].push(element.id.slice(element.id.indexOf('_')+1))
            }
            else if(element.id.includes('main_')){
                conditions['code_smells'].push(element.id.slice(element.id.indexOf('_')+1))
            }
            else if(element.id.includes('languages_')){
                conditions['languages'].push(element.id.slice(element.id.indexOf('_')+1))
            }

        }
    })
    console.log(conditions)
    let li1 = [];
    let li2 = [];
    let li3 = [];
    let li4 = [];
    conditions["bugs"].forEach(rating => {
        li1.push(converter[rating])
    })
    conditions["bugs"] = li1

    conditions["vulnerabilities"].forEach(rating => {
        li2.push(converter[rating])
    })
    conditions["vulnerabilities"] = li2

    conditions["code_smells"].forEach(rating => {
        li3.push(converter[rating])
    })
    conditions["code_smells"] = li3

    conditions["status"].forEach(rating => {
        li4.push(converter2[rating])
    })
    conditions["status"] = li4
    console.log(conditions)
    $.ajax({
        "type": "get",
        "url": `/filters?dict=${JSON.stringify(conditions)}`,
        "success": function(data){
            window.location.replace('/projectsfiltering')
        }
    })
})

// reset the filters
const resetFilterBtn = document.querySelector('#reset')

resetFilterBtn.addEventListener('click', event => {
    let checkboxes = document.querySelectorAll('.custom-control-input')
    Array.from(checkboxes).forEach(element => {
        element.checked = false;
    })
})


// Search bar 
const searchBar = document.querySelector('#search')
console.log(searchBar)

searchBar.addEventListener('keyup', event => {
    console.log('fdasf')
    let text = event.target.value
    Array.from(document.querySelectorAll('.projectRows')).forEach(row => {
        console.log(row.children[0].children[0])
        let projectName = row.children[0].children[0].children[0].children[0].innerText
        if(projectName.toLowerCase().indexOf(text.toLowerCase()) == -1){
            row.style.display = 'none'
        }
        else{
            row.style.display = ''
        }
    })
})

// Sorting 
document.querySelector('#exampleFormControlSelect1').addEventListener('change', event => {
    if(event.target.value != 'Select an option'){
    window.location.replace(`/sortprojectsLoading?sort=${event.target.value.toLowerCase()}`)
    }
})
