let profiles = document.querySelectorAll('.message');


for (let p of profiles){
    let photo = p.querySelector('img');
    let username = p.querySelector('.username').innerHTML;
    photo.addEventListener('mouseover', (event)=>{
        event.target.style = 'cursor : pointer';
    })
    photo.addEventListener('mouseout', (event)=>{
        event.target.style = 'cursor : none';
    })
    photo.addEventListener('click', (event) => {
        window.open(`http://127.0.0.1:8000/main_page/${username}`);
    });
}

