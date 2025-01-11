var chat_id = document.getElementById('chat').innerHTML;
var messages = document.getElementById('messages');


setInterval(()=>{
    const options = {
        method: 'GET', 
        headers: {
          'Content-Type': 'application/json',
          'Authorization' : 'Token ' + token,
        },
}
    fetch(`http://127.0.0.1:8000/api/chat/allmessages/${Number(chat_id)}`, options).
    catch((error) => console.log(error)).
    then((response) => {return response.json()}).
    then((json) => {
        const allmessages = document.querySelectorAll('.message');
        console.log(allmessages.length);
        console.log(json.length);
        if (json.length !== allmessages.length) {
            for (let l = allmessages.length; l < json.length; l++){
                let data = json[l];
                
                let create_new_message = document.createElement('div');
                create_new_message.setAttribute('class', 'message');

                let profile_picture = document.createElement('img');
                profile_picture.setAttribute('class', 'profile_picture');
                profile_picture.setAttribute('src', data['user_photo']);
                profile_picture.addEventListener('mouseover', (event)=>{
                    event.target.style = 'cursor : pointer';
                });
                profile_picture.addEventListener('mouseout', (event)=>{
                    event.target.style = 'cursor : none';
                });
                profile_picture.addEventListener('click', (event) => {
                   window.location.href = `http://127.0.0.1:8000/main_page/${data['username']}`;
                });
                create_new_message.appendChild(profile_picture);

                let from_user = document.createElement('span');
                from_user.innerHTML = data['name'] + '<br>';
                from_user.setAttribute('class', 'name');
                create_new_message.appendChild(from_user);

                let message_text = document.createElement('span');
                message_text.innerHTML = data['message'];
                message_text.setAttribute('class', 'mes');
                create_new_message.appendChild(message_text);


                let send_time = document.createElement('span');
                send_time.setAttribute('class', 'time');
                let time = new Date();
                send_time.innerHTML = `${time.getHours()}:${time.getMinutes()}`;
                create_new_message.appendChild(send_time);

                        

                messages.appendChild(create_new_message);

                setstyles();
            }
                        
        }
    })
}, 3000);

var setstyles = () => {
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
