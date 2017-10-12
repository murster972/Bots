//TODO: use jquery html to jquery append, so only new content is added or removed, instead
//      instead if everything being refreshed

$(function(){
    updateServerInfo();
    $("#sendCmd").click(function(){
        var updata = {"cmd": $("#command").val(), "clients": []};
        var clients = $("#clientIDs").val().replace(" ", "").split(",");
        updata["clients"] = clients;
        $.ajax({
            url: "/uploadCommand",
            data: JSON.stringify(updata),
            type: "POST",
            success: function(resp){
                r = eval(resp);
                html = r[0] == -1 ? "Command upload unsuccessful: " + r[1] : "Command upload successful"
                $("#sentCmdStatus").text(html);
            }
        })
    })
})

function updateCommandInfo(){
    $.ajax({
        url: "/getCommandInfo",
        data: "",
        type: "GET",
        success: function(resp){
            clientInfo = eval(resp);
            html = "<tr><td>ClientID - HostName</td><td>CommandID</td><td>Command</td><td>Sent</td><td>Result</td></tr>";
            for(var i = 0; i < clientInfo.length; i++){
                c = clientInfo[i];
                html = html + "<tr>" + "<td>" + c[0] + "</td> <td>" + c[1] + "</td><td>" + c[2] + "</td><td>" + c[3] + "</td><td>" + c[4] + "</td></tr>"
            }
            $("#CommandInfo").html(html);
        }
    })
}

function updateServerInfo(){
    $.ajax({
        url: "/activeServers",
        data: "",
        type: "GET",
        success: function(resp){
            var data = eval(resp);
                servers = data[0];
                clients = data[1];

            if(resp == "0"){
                $("#active").html("Active Servers: False");
                $("#serverInfo").html("");
                $("#clientInfo").html("");
            }
            else{
                $("#active").html("Active Servers: True");
                clientHTML = "<tr><td>ClientID</td><td>Host Name</td><td>ServerID</td></tr>";
                serverHTML = "<tr><td>ServerID</td><td>isActive</td><td>IP Address</td><td>Port Number</td></tr>";
                for(var i = 0; i < clients.length; i++){
                    c = clients[i];
                    clientHTML = clientHTML + "<tr>" + "<td>" + c[0]  + "</td>" + "<td>" + c[1]  + "</td>" + "<td>" + c[2]  + "</td>" + "</tr>"
                }
                for(var i = 0; i < servers.length; i++){
                    s = servers[i];
                    serverHTML = serverHTML + "<tr>" + "<td>" + s[0]  + "</td>" + "<td>" + s[1]  + "</td>" + "<td>" + s[2]  + "</td>" + "<td>" + s[3]  + "</td>" + "</tr>"
                }
                $("#clientInfo").html(clientHTML);
                $("#serverInfo").html(serverHTML);
            }
        }
    })
}

window.setInterval(function(){
    updateServerInfo();
    updateCommandInfo();
}, 500);
