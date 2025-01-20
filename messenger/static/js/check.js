//let pchats = document.querySelectorAll('.pchat');
//var chat_id = Number(document.getElementById('chat').innerHTML);
//var token = document.getElementById('token').innerHTML;
//
//for (let p of pchats){
//    if (p.getAttribute('class') === 'nothing'){
//        const options = {
//            method: 'DELETE',
//            headers: {
//              'Content-Type': 'application/json',
//              'Authorization' : 'Token ' + token,
//            },
//        }
//        fetch(`http://127.0.0.1:8000/api/chat/delete_chat/${chat_id}`, options).
//        then((response)=>{
//            return response.json;
//        }).
//        then((json)=>{
//            console.log(json);
//            return json;
//        }).
//        catch((error)=>console.log(error))
//    }
//}