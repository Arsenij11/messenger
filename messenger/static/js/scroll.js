let allmessages = document.getElementById('messages');

allmessages.addEventListener('scroll', (event) => {
    let allmes = document.querySelectorAll('.message');
    let top = allmessages.scrollTop;
    let first_el_top = allmes[0].style.top;
    for (let a of allmes) {
        if (top === 0 && parseInt(first_el_top) < -7){
            a.style.top = `${parseInt(a.style.top) + 60}px`;
        }
        else if (first_el_top === '-7px') {
            allmes.forEach((el) => el.style.top = `${parseInt(el.style.top) + 1}px`);
        }
    }

});
allmessages.addEventListener('click', (event) => {
    let del = document.querySelector('.delete');
    if (event.button === 0 && del !== null) {
        del.remove();
    }
});