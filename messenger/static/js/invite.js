const chats = document.getElementById('chats');
console.log(window.innerHeight / 2, window.innerWidth);
chats.style.margin = `${window.innerHeight / 2.8}px 0 0 ${window.innerWidth / 2.4}px`;
const chat = document.querySelectorAll('.chat');
for (let c of chat) {
    let ps = c.querySelectorAll('p');
    let chat_id;
    let user_id;
    let token;
    ps.forEach((p) => {
        if (p.getAttribute('class') === 'chat_id') {
            chat_id = p.innerHTML;
        }
        if (p.getAttribute('class') === 'user_id') {
            user_id = p.innerHTML;
        }

        if (p.getAttribute('class') === 'key') {
            token = p.innerHTML;
        }

        if (p.getAttribute('class') === 'chat_to_add') {
            p.addEventListener('mouseover', (event) => {
                event.target.style = 'color : grey; cursor : pointer';
            });
            p.addEventListener('mouseout', (event) => {
                event.target.style = 'color : white; cursor : none';
            })
            p.addEventListener('click', (event) => {
                const options = {
                    method : 'POST',
                    headers: {
                          'Content-Type': 'application/json',
                          'Authorization' : 'Token ' + token,
                    },
                }
                fetch(`http://127.0.0.1:8000/api/chat/add/${chat_id}/${user_id}`, options).
                catch((error) => console.log(error)).
                then((response) => {return response.json()}).
                then((json) => {
                    console.log(json);
                    if (typeof json['detail'] === 'undefined') {
                        event.target.parentNode.style = 'display : none';
                        let num = 0;
                        chat.forEach((c) => {
                            if (c.style.display === 'none') {
                                num++;
                            }
                        });
                        if (chat.length === num) {
                            window.location.reload();
                        }
                    }
                })
            });
        }
    });
}
