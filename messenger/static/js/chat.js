var chat_id = Number(document.getElementById('chat').innerHTML);
var user_id = Number(document.getElementById('user').innerHTML);
var username = document.getElementById('username').innerHTML;
var user_photo = document.getElementById('user_photo').innerHTML;
var token = document.getElementById('token').innerHTML;
var header = document.getElementById('header');

var messages = document.getElementById('messages');
let chats = document.getElementById('chats');

messages.style.width= `${parseInt(header.style.width) - 300}px`;
messages.style.height = `${parseInt(innerHeight) - 20 - 30 - 100}px`
chats.style.height = `${window.innerHeight}px`;


setstyles();

let putmessagefield = document.getElementById('putmessage');
putmessagefield.style.width = `${parseInt(window.innerWidth) - 370}px`;
putmessagefield.style.marginLeft = 300 + 'px';

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
                // console.log(response.json());
                return response.json();
              })
        
        .catch((error) => { console.log(error) })
        .then(
                (json) => {
                        console.log(json)
                        const messages = document.getElementById('messages');

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

                        let usern = document.createElement('span');
                        usern.style.display = 'none';
                        usern.innerHTML = data['user'];
                        usern.setAttribute('class', 'username');
                        create_new_message.appendChild(usern);


                        let mes_id = document.createElement('span');
                        mes_id.style.display = 'none';
                        mes_id.innerHTML = data['id'];
                        mes_id.setAttribute('class', 'mes_id');
                        create_new_message.appendChild(mes_id);

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

