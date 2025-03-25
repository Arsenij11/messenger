let messages = document.getElementById('messages');
let chats = document.getElementById('chats');
let nonselectedchat = document.getElementById('nonselectedchat');
let everychat = document.querySelectorAll('.chat');
let user_id = document.getElementById('user').textContent; 
let every_chat = document.querySelectorAll('.pchat');

messages.style.width = `${Number(window.innerWidth) - 200}px`;
messages.style.height = `${window.innerHeight}px`;
chats.style.height = `${window.innerHeight}px`;
nonselectedchat.style.top = `${Number(window.innerHeight/2)}px`;

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

