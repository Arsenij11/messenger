let messages = document.getElementById('messages');
let chats = document.getElementById('chats');
let nonselectedchat = document.getElementById('nonselectedchat');
let everychat = document.querySelectorAll('a');
let user_id = document.getElementById('user').textContent; 


messages.style.width = `${Number(window.innerWidth) - 200}px`;
messages.style.height = `${window.innerHeight}px`;
chats.style.height = `${window.innerHeight}px`;
nonselectedchat.style.top = `${Number(window.innerHeight/2)}px`;

if (everychat.length > 0){
everychat.forEach((e)=>{
    e.addEventListener('mouseover', (event)=> {
        event.target.style = 'cursor : pointer; background-color: #202b36';
    });
    e.addEventListener('mouseout', (event) => {
        event.target.style = 'cursor : none; background-color: #17212b';
    });
})
};

