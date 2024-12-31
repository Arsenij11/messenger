const chat_id = Number(document.getElementById('chat').innerHTML);
const user_id = Number(document.getElementById('user').innerHTML);
const token = document.getElementById('token').innerHTML;



let messages = document.getElementById('messages');
let chats = document.getElementById('chats');
let everychat = document.querySelectorAll('.chat');
let allchatmessages = document.querySelectorAll('.message');
// let profile_pictures = document.querySelectorAll('.profile_picture');

messages.style.width = `${Number(window.innerWidth) - 200}px`;
messages.style.height = `${window.innerHeight}px`;
chats.style.height = `${window.innerHeight}px`;

let height = window.innerHeight - 50;
let previous_height = height;


for (let i in allchatmessages) {
        // profile_pictures[i].style.marginTop = height + 'px';
        if (typeof allchatmessages[i].style !== 'undefined'){
                allchatmessages[i].style.top = height + 'px'; 
                height -= 60;
        }
       

}

let putmessagefield = document.getElementById('putmessage');
putmessagefield.style.width = `${1550}px`;
putmessagefield.style.marginLeft = 300 + 'px';
putmessagefield.style.marginRight = 1 + 'px';

let button = document.getElementById('sendmessage');





putmessagefield.addEventListener('keypress' , (event)=>{
button.style.display = 'table-cell';
})

button.addEventListener('mouseover', (event)=>{
        event.target.style = 'cursor : pointer; background-color: #182533; display : table-cell'
});
button.addEventListener('mouseout', (event)=>{
        event.target.style = 'cursor : none; background-color: #0e1621; display : table-cell'
});
button.addEventListener('click', (event) => {
        if (putmessagefield.value !== '') {
                let data = {
                        "chat": chat_id,
                        "user": user_id,
                        "message": putmessagefield.value,
                }
                newmessage(data);
        }
});

function newmessage (data) {
        const options = {
                method: 'POST', 
                headers: {
                  'Accept': 'application/json', 
                  'Content-Type': 'application/json',
                  'Authorization' : token,
                },
                body: JSON.stringify(data), 
        }
        console.log(options);
       fetch('http://127.0.0.1:8000/api/chat/new_message', options)
         .then((response) => {
                console.log('response', response.body);
                return response.json();
              })
        .then(
                (json) =>{ 
                 return json;
                })
        .catch(() => { console.log('error') });
}


