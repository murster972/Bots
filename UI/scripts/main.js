$(document).ready(function(){
    alignServerStatusLabels();
});

$(window).resize(function(){
    alignServerStatusLabels();
})


function alignServerStatusLabels(){
    if(window.innerWidth <= 340){
        console.log(window.innerWidth);
        $(".ServerInfoItem").width("100%");
    }
    else{
        port_width = $(".ServerInfoText.Title.port").width();
        ip_width = $(".ServerInfoText.Title.IP").width();
        status_width = $(".ServerInfoText.Title.status").width();
        console.log(ip_width + (port_width - ip_width));
        console.log(status_width + (port_width - status_width));
    }
}
