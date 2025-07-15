const micBtn = document.getElementById("mic");
const camBtn = document.getElementById("cam");
const speakerBtn = document.getElementById("");
let mydiv=document.getElementById("user_container");
const container=document.getElementById("avatar_container");

let videostream=null;
let micstream=null;
let video=null;

camBtn.addEventListener('click', async ()=>{
    if(!videostream){
        try{
            video = document.createElement("video");
            video.classList.add("user");
            video.autoplay = true;
            video.playsInline = true;


            videostream=await navigator.mediaDevices.getUserMedia({video:true});
            video.srcObject =videostream;

            mydiv.remove();
            container.appendChild(video);
            camBtn.style.backgroundColor="red";
        }
        catch(error){
            alert(`video access error: ${error}`);
            console.error(error);
        }
    }
    else{
        mydiv=document.createElement("div");
        mydiv.classList.add("user");
        const innerdiv=document.createElement("div");
        innerdiv.classList.add("user_avatar");
        const image=document.createElement("img");
        image.src = "/static/images/user_avatar.png";
        image.id="user_photo";

        mydiv.appendChild(innerdiv);
        innerdiv.appendChild(image);

        videostream.getTracks().forEach(track =>track.stop());
        video.srcObject =null;
        videostream =null;
        video.remove();
        container.appendChild(mydiv);
        camBtn.style.backgroundColor="black";
    }  
})

micBtn.addEventListener('click' ,async ()=>{
    if(!micstream){
        try{
            micstream = await navigator.mediaDevices.getUserMedia({audio:true});
            micBtn.style.backgroundColor="red";
            micstream.getAudioTracks()[0].enabled =true; 
        }
        catch(error){
            alert(`microphone access error: ${error}`);
            console.error(error);
        }
    }
    else{
        micstream.getTracks().forEach(track=>track.stop());
        micstream=null;
        micBtn.style.backgroundColor="black";
    }
})
