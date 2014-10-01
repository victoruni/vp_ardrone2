
// JavaScript Document


// subscribes callback
var get_ros_service=function(msg,nn)
  {
  if(nn<10)  // list files scenarios
    { 
    //alert(msg);
    var arr1=msg.split(";");
    var select_obj=document.getElementById("choice_scenario"+nn);
    for(var i=0;i<arr1.length;i++)
     {var opt=document.createElement("option");
     opt.value=arr1[i];
     opt.innerHTML=arr1[i];
     select_obj.appendChild(opt);
     }
    }
  else  // list commands choice file scenario
    {
    //alert(msg);
    nn=nn-10;
    var arr1=msg.split("&");
    var select_obj=document.getElementById("view_scenario"+nn);
    while(select_obj.length>0)
      select_obj.remove(0); 
    for(var i=0;i<arr1.length;i++)
     {var opt=document.createElement("option");
     opt.value=arr1[i];
     opt.innerHTML=arr1[i];
     select_obj.appendChild(opt);
     }
    }

  }
var get_scenario=function(nn,msg)
  {
  var cback11=function(msg1) {JSON.stringify(msg1),get_ros_service(msg1.answer,nn);}
  var outarr=new Array();outarr[0]=msg;
  switch(nn)
    {
     case 1: con1.callService(cback11,'/vp_ardrone2_get_scenario',outarr);
       break;
     case 2: con2.callService(cback11,'/vp_ardrone2_get_scenario',outarr);
       break;
     case 3: con3.callService(cback11,'/vp_ardrone2_get_scenario',outarr);
       break;
     case 4: con4.callService(cback11,'/vp_ardrone2_get_scenario',outarr);
       break;
     case 11: con1.callService(cback11,'/vp_ardrone2_get_scenario',outarr);
       break;
     case 12: con2.callService(cback11,'/vp_ardrone2_get_scenario',outarr);
       break;
     case 13: con3.callService(cback11,'/vp_ardrone2_get_scenario',outarr);
       break;
     case 14: con4.callService(cback11,'/vp_ardrone2_get_scenario',outarr);
       break;
     default: break;
    }
  }

var get_ros=function(nn,msg)
  {
  //alert(msg);
  if(nn<10)   // messages from /ardrone/navdata
    {
    var states=new Array("Unknown","Inited","Landed","Flying","Hovering","Test","Taking off","Flying","Landing","Looping");
    var colors=new Array("red","yellow","green","blue","blue","yellow","green","blue","green","blue");

    document.getElementById("rotZ"+nn).innerHTML=msg.rotZ;
    document.getElementById("altd"+nn).innerHTML=msg.altd;
    //document.getElementById("ready"+nn).innerHTML=msg.rotZ;
    document.getElementById("ready"+nn).innerHTML=states[msg.state];
    document.getElementById("ready"+nn).style.backgroundColor=colors[msg.state];
    // 
    document.getElementById("battery"+nn).innerHTML=" "+msg.batteryPercent+" % ";
    if(msg.batteryPercent>70)
      document.getElementById("battery"+nn).style.backgroundColor='green';
    else if(msg.batteryPercent>30)
      document.getElementById("battery"+nn).style.backgroundColor='yellow';
    else
      document.getElementById("battery"+nn).style.backgroundColor='red';
    }
  else  // messages from /web_subscriber
    {
    //alert(msg.data);
    nn=nn-10;
    select_options=document.getElementById("view_scenario"+nn).options;
    select_options[msg.data].selected=true;
    if(select_options.length-msg.data<2)
      {
      document.getElementById("button_send").disabled=false;
      // audio pause
      var audio1=document.getElementById("audio1");
      audio1.pause();
      }
    }
  }
// button start
function start_ros(arg,topic)
  {
  //alert(topic);
  var count=0;var data1;
  for(var i=1;i<5;i++)
    {
    if(document.getElementById("check"+i).checked)
      {
      if(arg==1)   // start file scenario
        {
        document.getElementById("button_send").disabled=true;
        file_index=document.getElementById("choice_scenario"+i).selectedIndex;
        select_options=document.getElementById("choice_scenario"+i).options;
        // audio play
        var audio1=document.getElementById("audio1");
        audio1.play();
        data1=select_options[file_index].value;
        //con1.publish(topic, {'data':select_options[file_index].value});
        }
      switch(i)
        {
        case 1: if(arg>0) con1.publish(topic, {'data':data1});
                else con1.publish(topic, {});
          break;
        case 2: if(arg>0) con2.publish(topic, {'data':data1});
                else con2.publish(topic, {});
          break;
        case 3: if(arg>0) con3.publish(topic, {'data':data1});
                else con3.publish(topic, {});
          break;
        case 4: if(arg>0) con4.publish(topic, {'data':data1});
                else con4.publish(topic, {});
          break;
        default:
          break;
        }
      }
    }
  }
//
function stop_ardrone(arg)
  {
  alert(arg);
  switch(arg)
        {
        case 1: con1.publish('/web_publisher2', {});
          break;
        case 2: con2.publish('/web_publisher2', {});
          break;
        case 3: con3.publish('/web_publisher2', {});
          break;
        case 4: con4.publish('/web_publisher2', {});
          break;
        default:
          break;
        }

  }


