let everychat = document.querySelectorAll('.chat');
let every_chat = document.querySelectorAll('.pchat');

if (everychat.length > 0){
    everychat.forEach((e)=>{
        let img = e.querySelector('img');
        let chat_id = e.querySelector('.chat_id').innerHTML;
        img.addEventListener('mouseover', (event)=> {
            event.target.style.cursor = 'pointer';
        });
        img.addEventListener('mouseout', (event) => {
            event.target.style.cursor = 'none';
        });
        img.addEventListener('click', (event)=>{
            let url = `http://127.0.0.1:8000/chat/${chat_id}`;
            window.location.href = url;
        })

    })
}

if (every_chat.length > 0){
    every_chat.forEach((e)=>{
        let img = e.querySelector('img');
        let chat_id = e.querySelector('.chat_id').innerHTML;
        img.addEventListener('mouseover', (event)=> {
            event.target.style.cursor = 'pointer';
        });
        img.addEventListener('mouseout', (event) => {
            event.target.style.cursor = 'none';
        });
        img.addEventListener('click', (event)=>{
            let url = `http://127.0.0.1:8000/chat/${chat_id}`;
            window.location.href = url;
        });
    })
}

