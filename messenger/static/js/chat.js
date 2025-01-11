var chat_id = Number(document.getElementById('chat').innerHTML);
var user_id = Number(document.getElementById('user').innerHTML);
var username = document.getElementById('username').innerHTML;
var user_photo = document.getElementById('user_photo').innerHTML;
var token = document.getElementById('token').innerHTML;



var messages = document.getElementById('messages');
let chats = document.getElementById('chats');
let everychat = chats.children;

messages.style.width = `${Number(window.innerWidth) - 200}px`;
messages.style.height = `${window.innerHeight}px`;
chats.style.height = `${window.innerHeight}px`;


setstyles();

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
                  'Content-Type': 'application/json',
                  'Authorization' : 'Token ' + token,
                },
                body: JSON.stringify(data), 
        }
        console.log(options);
       fetch(`http://127.0.0.1:8000/api/chat/new_message/${data['chat']}/${data['user']}`, options)
        .then((response) => {
                console.log('response', response.body);
                return response.json();
              })
        
        .catch((error) => { console.log(error) })
        .then(
                (json) => {

                        console.log('Всё ок: ', json);

                        let create_new_message = document.createElement('div');
                        create_new_message.setAttribute('class', 'message');

                        let profile_picture = document.createElement('img');
                        profile_picture.setAttribute('class', 'profile_picture');
                        profile_picture.setAttribute('src', user_photo);
                        profile_picture.addEventListener('mouseover', (event)=>{
                            event.target.style = 'cursor : pointer';
                        })
                        profile_picture.addEventListener('mouseout', (event)=>{
                            event.target.style = 'cursor : none';
                        })
                        profile_picture.addEventListener('click', (event) => {
                           window.location.href = `http://127.0.0.1:8000/main_page/${username}`;
                        });
                        create_new_message.appendChild(profile_picture);

                        let from_user = document.createElement('span');
                        from_user.innerHTML = username + '<br>';
                        from_user.setAttribute('class', 'name');
                        create_new_message.appendChild(from_user);

                        let message_text = document.createElement('span');
                        message_text.innerHTML = json['message'];
                        message_text.setAttribute('class', 'mes');
                        create_new_message.appendChild(message_text);


                        let send_time = document.createElement('span');
                        send_time.setAttribute('class', 'time');
                        let time = new Date();
                        send_time.innerHTML = `${time.getHours()}:${time.getMinutes()}`;
                        create_new_message.appendChild(send_time);

                  
                        messages.appendChild(create_new_message);

                        putmessagefield.value = null;

                        setstyles();

                        
                        return json;
                }
        );
}

function setstyles () {
        let allchatmessages = document.querySelectorAll('.message');
        let j = 0;
        for (let i = allchatmessages.length - 1; i >= 0 ; i--) {
                if (typeof allchatmessages[i].style !== 'undefined'){
                        j++;
                        let height = window.innerHeight;
                        height -= 60 * j;
                        allchatmessages[i].style.top = height + 'px';
                }
        }
}

