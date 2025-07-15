const display=document.getElementById("stptimer");
let timer=null;
let startTime=0;
let elapsedTime=0;
let isrunning=false;


if(!isrunning){
    startTime=Date.now()-elapsedTime;
    timer=setInterval(update,1000);
    isrunning=true;
}


function update(){

    const currentTime =Date.now();
    elapsedTime= currentTime -startTime;

    let hours=Math.floor(elapsedTime / (1000 * 60 * 60));
    let mins=Math.floor(elapsedTime / (1000 * 60) % 60);
    let sec=Math.floor(elapsedTime / 1000 % 60);

    hours=String(hours).padStart(2,"0");
    mins=String(mins).padStart(2,"0");
    sec=String(sec).padStart(2,"0");

    if(hours=="00"){
    display.textContent=`${mins}:${sec}`;    
    }
    else{
    display.textContent=`${hours}:${mins}:${sec}`;
    }

}