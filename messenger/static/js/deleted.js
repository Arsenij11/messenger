setInterval(checkdeletemessage, 2000);

function checkdeletemessage () {
    const chat_id = document.getElementById('chat').innerHTML;
    const token = document.getElementById('token').innerHTML;

    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        },
    }

    fetch(`http://127.0.0.1:8000/api/chat/allmessages/${chat_id}`, options).
    then((response)=> {return response.json()}).
    then((json) => {
        let allmes = document.querySelectorAll('.message');
        // allmes = allmes.filter((a) => {return a.querySelector('.mes_id').innerHTML});

         if (json.length < allmes.length) {
             let existing_messages = [];
             json.forEach((j)=>{
                existing_messages.push(String(j['id']));
             });

             allmes.forEach((a)=> {
                 let exist = false;
                 let mes_id = a.querySelector('.mes_id').innerHTML;
                 for (let e of existing_messages){
                    if (e === mes_id) {
                        exist = true;
                        break;
                    }
                 }
                if (!exist) {
                    removemessage(a);
                }

             });

             }
         }
    )

}

function removemessage (a){
    a.remove();
    setTimeout( ()=>{
        let allchatmessages = document.querySelectorAll('.message');
        let j = 0;
        for (let i = allchatmessages.length - 1; i >= 0 ; i--) {
            if (typeof allchatmessages[i].style !== 'undefined'){
                j++;
                let height = window.innerHeight;
                height -= 60 * j;
                allchatmessages[i].style.top = height + 'px';
            }
        }}, 500);
}