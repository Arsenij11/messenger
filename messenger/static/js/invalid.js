const info = document.getElementById('info');
info.style.margin = `${Math.floor(window.innerHeight/2.5)}px 0 0 ${Math.floor(window.innerWidth/2.5)}px`

const time = document.getElementById('time');
let text = time.innerHTML;
let number = 10;
time.innerHTML = text + number;
setInterval(() => {
     if (number === 0) {
         window.location.href = `http://127.0.0.1:8000/main_page/${document.getElementById('username').innerHTML}`;
     }
     else {
         number--;
         time.innerHTML = text + number;
     }
}, 1000);