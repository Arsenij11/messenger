let allchatmessages = document.querySelectorAll('.message');
var token = document.getElementById('token').innerHTML;

for (let a of allchatmessages) {
    let current_username = document.getElementById('current_username').innerHTML;
    let author = a.querySelector('.username').innerHTML;
    if (current_username === author) {
        a.addEventListener('dblclick', (event)=> {
                let open_delete = document.querySelector('.delete');
                if (open_delete !== null) {
                    open_delete.remove();
                }
                let span = document.createElement('span');
                span.style.top = `${parseInt(event.target.style.height)/2}px`;
                span.style.left = `${parseInt(event.target.style.width)/2}px`;
                span.textContent = 'Удалить';
                span.setAttribute('class', 'delete');
                span.addEventListener('mouseover', (event)=> {
                   event.target.style.cursor = 'pointer';
                });
                span.addEventListener('mouseout', (event)=> {
                    event.target.style.cursor = 'none';
                });
                span.addEventListener('click', (event) => {
                        let mes_id = a.querySelector('.mes_id').innerHTML;
                        const options = {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': 'Token ' + token,
                            },
                        }

                        fetch(`http://127.0.0.1:8000/api/chat/delete_message/${mes_id}`, options).
                        then((response)=> {return response.json()}).
                        then((json) => {
                             if (typeof json['detail'] === 'undefined') {

                                 a.innerHTML = 'Сообщение удалено';
                                 a.setAttribute('class', 'deleted_message');


                             }
                             else {
                                 console.log(json);
                             }
                         })

                })
            event.target.appendChild(span);
        })
    }
}
setInterval(()=> {
    const alldeletedmessages = document.querySelectorAll('.deleted_message');
    if (alldeletedmessages.length > 0){
        alldeletedmessages.forEach((a)=>a.style.display = 'none');
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
}, 3000);