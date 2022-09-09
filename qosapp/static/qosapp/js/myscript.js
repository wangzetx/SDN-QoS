function displayTopo(data) {
    var nodes = []
    for(var i = 0; i < Object.keys(data['nodes']).length; i++) {
        var nodei = {'id': i, 'name': data['nodes'][i]['node-id'], 'type': data['nodes'][i]['type'], 'label': data['nodes'][i]['node-id']}
        nodes.push(nodei)
    }
    var edges = []
    for(var i = 0; i < Object.keys(data['links']).length; i++) {
        for(var j = 0; j < Object.keys(nodes).length; j++) {
            if(nodes[j]['name'] == data['links'][i]['source-node'])
            sourcei = nodes[j]['id']
            if(nodes[j]['name'] == data['links'][i]['dest-node'])
            desti = nodes[j]['id']
        }
        edges.push({from: sourcei, to: desti})
    }
    console.log("this is displayTopo")
    console.log(nodes)
    console.log(edges)
    for(var i = 0; i < nodes.length; i++) {
        if(nodes[i].type == 'host')
        nodes[i].image = "static/qosapp/images/pc.png"
        else if(nodes[i].type == 'switch')
        nodes[i].image = "static/qosapp/images/switch.png"
    }
    var container = document.getElementById('network')
    var data = {
        nodes: nodes,
        edges: edges
    }
    var options = {
        nodes :{
            shape: 'image'
        }
    }
    var network = new vis.Network(container, data, options);
}
function createtip(message) {
    var tip = document.createElement('div');
    tip.id = "tip";
    tip.style.position = "absolute";
    tip.style.zIndex = "+3";
    tip.style.width = "360px";
    tip.style.height = "40px";
    tip.style.lineHeight = "40px";
    tip.style.textAlign = "center";
    tip.style.fontSize = "17px";
    tip.style.fontWeight = "normal";
    tip.style.backgroundColor = "rgb(239, 222, 171)";
    tip.style.color = "white";
    tip.style.borderRadius = "5px";
    tip.style.left = "50%";
    tip.style.top = "40%";
    tip.style.transform = "translate(-50%, -50%)";
    tip.innerHTML = message;
    return tip;    
}
function showtip(message, type) {
    var tip = createtip(message);
    var wrapper;
    switch(type) {
        case 'login':
            wrapper = document.getElementsByClassName("login-wrapper")[0];
            break;
        case 'register':
            wrapper = document.getElementsByClassName("register-wrapper")[0];
            break;
        case 'flowform':
            wrapper = document.getElementById("flowform");
            break;
        case 'meterform':
            wrapper = document.getElementById("meterform");
            break;
        case 'flowdisplay':
            wrapper = document.getElementById('mainpart');
            break;
        case 'meterdisplay':
            wrapper = document.getElementById('mainpart');
            break;
        case 'deleteflow':
            wrapper = document.getElementById('deleteflow');
            break;
        case 'deletemeter':
            wrapper = document.getElementById('deletemeter');
            break;
        case 'topodisplay':
            wrapper = document.getElementById('displaytopo');
            break;
    }
    if(document.getElementById("tip") == null) {
        wrapper.appendChild(tip);
        setTimeout(function(){
            wrapper.removeChild(tip);
        } ,1300);    
    }
}
function createFlowDataRow(flowdata) {
    var trow = document.createElement('tr');
    trow.className = "trow";
    var idCell = document.createElement('td');
    var basicCell = document.createElement('td');
    var matchCell = document.createElement('td');
    var instructionsCell = document.createElement('td');
    var statisticsCell = document.createElement('td');
    idCell.innerHTML = flowdata.id;
    basicCell.innerHTML = flowdata.basic;
    matchCell.innerHTML = flowdata.match;
    instructionsCell.innerHTML = flowdata.instructions;
    statisticsCell.innerHTML = flowdata.statistics;
    trow.appendChild(idCell);
    trow.appendChild(basicCell);
    trow.appendChild(matchCell);
    trow.appendChild(instructionsCell);
    trow.appendChild(statisticsCell);
    return trow;
}
function createMeterDataRow(meterdata) {
    var trow = document.createElement('tr');
    trow.className = "trow";
    var idCell = document.createElement('td');
    var basicCell = document.createElement('td');
    var meterBandHeadersCell = document.createElement('td');
    var meterStatisticsCell = document.createElement('td');
    idCell.innerHTML = meterdata.id;
    basicCell.innerHTML = meterdata.basic;
    meterBandHeadersCell.innerHTML = meterdata.meterBandHeaders;
    meterStatisticsCell.innerHTML = meterdata.meterStatistics;
    trow.appendChild(idCell);
    trow.appendChild(basicCell);
    trow.appendChild(meterBandHeadersCell);
    trow.appendChild(meterStatisticsCell);
    return trow;
}
function display(datalist, type) { 
    if(type == 'flow')
    var tbody = document.getElementById("tbflowmain");
    else if(type == 'meter')
    var tbody = document.getElementById('tbmetermain')
    var tbodychildnodes = tbody.childNodes;
    for(var i = tbodychildnodes.length - 1; i >= 0 ; i--)
    tbody.removeChild(tbodychildnodes[i]);
    setTimeout(function() {
        var len = Object.keys(datalist).length;
        for(var i = 0; i < len; i++) {
            if(type == 'flow')
            var trow = createFlowDataRow(datalist[i]);
            else if(type == 'meter')
            var trow = createMeterDataRow(datalist[i]);
            tbody.appendChild(trow);
        }
    }, 1200)
}
function refreshflow() {
    $.ajax({
        type: "GET",
        url: "flow/get",
        async: false,
        success: function(result) {
            if(result['status'] == 0)
                showtip("刷新失败", "flowdisplay")
            else if(result['status'] == 1)
            display(result['data'], 'flow')
        }
    })
}
function clearinput() {
    var input = document.getElementsByClassName('input')
    for(var i = 0; i < Object.keys(input).length; i++) {
        var item = input[i];
        item.value = ""
    }
}
function add_flow() {
    var switchID = document.getElementById("switch").value;
    var flowID = document.getElementById("name").value;
    var priority = document.getElementById("priority").value;
    var inport = document.getElementById("in-port").value;
    var ethernetType = document.getElementById("ethernet-type").value;
    var ipv4Source = document.getElementById("ipv4-source").value;
    var ipv4Destination = document.getElementById("ipv4-destination").value;
    var layer4Match = document.getElementById('layer4-match').value
    var sourcePort = document.getElementById("source-port").value;
    var destinationPort = document.getElementById("destination-port").value;
    var matchSet = {};
    if(inport)
    matchSet['in-port'] = inport;
    if(ethernetType)
    matchSet['ethernet-match']['ethernet-type']['type'] = ethernetType;
    if(ipv4Source)
    matchSet['ipv4-source'] = ipv4Source;
    if(ipv4Destination)
    matchSet['ipv4-destination'] = ipv4Destination;
    if(layer4Match == 'TCP') {
        matchSet['ip-match'] = {'ip-protocol': 6};
        matchSet['tcp-source-port'] = sourcePort;
        matchSet['tcp-destination-port'] = destinationPort;
    }
    else if(layer4Match == 'UDP') {
        matchSet['ip-match'] = {'ip-protocol': 17}
        matchSet['udp-source-port'] = sourcePort;
        matchSet['udp-destination-port'] = destinationPort;
    }
    var action = document.getElementById("action").value
    var actionSet = {};
    var instructionsSet = {};
    console.log(action)
    if(action == 'DROP') {
        actionSet = {
            'order': '0',
            'drop-action': {}
        }
        instructionsSet = {
            "instruction": [{
                "order": "0",
                "apply-actions": {
                    "action": [actionSet]
                }
            }]
        }
    }
    else if(action == 'OUTPUT') {
        var outport = document.getElementById("out-port").value;
        actionSet = {
            'order': '0',
            'output-action': {'output-node-connector': outport}
        }
        instructionsSet = {
            "instruction": [{
                "order": "0",
                "apply-actions": {
                    "action": [actionSet]
                }
            }]
        }
    }
    else if(action == "METER") {
        var meterID = document.getElementById("meterID1").value;
        var outport = document.getElementById("out-port").value;
        actionSet = {
            'order': '0',
            'output-action': {"output-node-connector": outport}
        }
        instructionsSet = {
            "instruction": [
                {
                    "order": 0,
                    "meter": {"meter-id": meterID},
                }
                ,
                {
                    "order": 1,
                    "apply-actions": {
                        "action": [actionSet]
                    }
                }
            ]
        }
    }
    var flowSet = {
        "id": flowID,
        "table_id": '0',
        'hard-timeout': '0', 
        'idle-timeout':'0',
        'priority': priority
    }
    flowSet['match'] = matchSet
    flowSet['instructions'] = instructionsSet
    $.ajax({
        type: "POST",
        url: "flow/post",
        async: false,
        data: {"switchID": switchID, "flowSet": JSON.stringify(flowSet)},
        success: function(result) {
            if(result.status == 'success') {
                showtip("下发成功", "flowform")
                setTimeout(function(){clearinput()}, 1300)
            }
            else if(result.status == "failure") {
                showtip("下发失败", 'flowform')
                setTimeout(function(){clearinput()}, 1300)
            }
        }
    })
}
function delete_flow() {
    var deleteID = document.getElementById('deleteID').value;
    var switchID = document.getElementById('switchID2').value;
    $.ajax({
        type: "DELETE",
        url: "flow/delete",
        async: false,
        contentType: "application/json",
        data: {"deleteID": deleteID, "switchID": switchID},
        success: function(result) {
            if(result.status == 1) {
                console.log("showtip")
                showtip("删除成功", "deleteflow")
                setTimeout(function(){clearinput()}, 1300)
            }
            else if(result.status == 0) {
                showtip("删除失败", 'deleteflow')
                setTimeout(function(){clearinput()}, 1300)
            }
        }
    })
}
function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var value = {'username': username, 'password': password};
    $.ajax({
        type: "POST",
        url: "login",
        async: false,
        data: value,
        success: function(msg){
            if(msg["status"] == "NO") {
                showtip(msg["message"], "login");
                var inputitem = document.getElementsByClassName("input-item")[1];
                inputitem.value = "";
            }
            else if(msg["status"] == "YES") {
                var redirectURL = "QoS";
                window.location.href = redirectURL;
            }
        }
    });

}
function register() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var value = {'username': username, 'password': password};
    $.ajax({
        type: "POST",
        url: "register",
        async: false,
        data: value,
        success: function(msg){
            showtip(msg["message"], "register");
            if(msg["status"] == "YES") {
                var redirectURL = "login";
                setTimeout(function(){window.location.href = redirectURL;},1700)
            }
        }
    });
}

function refreshmeter() {
    $.ajax({
        type: "GET",
        url: "meter/get",
        async: false,
        success: function(result) {
            if(result['status'] == 0)
            showtip("刷新失败", "meterdisplay")
            else if(result['status'] == 1)
            display(result['data'], 'meter')
        }
    })
}

function deletemeter() {
    var switchID = document.getElementById('switchID3').value;
    var deleteID = document.getElementById('deleteID1').value;
    $.ajax({
        type: "DELETE",
        url: "meter/delete",
        async: false,
        contentType: "application/json",
        data: {"deleteID": deleteID, "switchID": switchID},
        success: function(result) {
            if(result.status == 1) {
                console.log("showtip")
                showtip("删除成功", "deletemeter")
                setTimeout(function(){clearinput()}, 1300)
            }
            else if(result.status == 0) {
                showtip("删除失败", 'deletemeter')
                setTimeout(function(){clearinput()}, 1300)
            }
        }
    })

    console.log('this is deletemeter')
}

function add_meter() {
    var switchID = document.getElementById('switchID1').value
    var meterBandID = document.getElementById('meterBandID').value
    var burstSize = document.getElementById('burstSize').value
    var limitSize = document.getElementById('limitSize').value
    var meterBandHeader = {
        'band-id': meterBandID,
        'meter-band-types': {'flags': 'ofpmbt-drop'},
        'drop-burst-size': burstSize,
        'drop-rate': limitSize
    }
    var meterSet = {
        'meter-id': '1',
        'meter-name': 'guestMeter',
        'flags': 'meter-kbps',
        'meter-band-headers': {
            'meter-band-header': meterBandHeader
        }
    }
    $.ajax({
        type: "POST",
        url: "meter/post",
        async: false,
        data: {"switchID": switchID, "meterSet": JSON.stringify(meterSet)},
        success: function(result) {
            if(result.status == 'success') {
                showtip("下发成功", "meterform")
                setTimeout(function(){clearinput()}, 1300)
            }
            else if(result.status == 'failure') {
                showtip("下发失败", 'meterform')
                setTimeout(function(){clearinput()}, 1300)
            }
        }
    })
}

function refreshtopo() {
    $.ajax({
        type: "GET",
        url: "topo/get",
        async: false,
        success: function(result) {
            console.log(result)
            if(result['status'] == 0)
            showtip("刷新失败", "topodisplay")
            else if(result['status'] == 1)
            displayTopo(result['data'])
        }
    })
}