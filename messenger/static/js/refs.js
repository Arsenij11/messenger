let refs = document.querySelectorAll('a');


for (let r of refs){
    r.addEventListener('mouseover', (event)=>{
        let el = event.target;
        el.style = 'color: #808080'
    });

    r.addEventListener('mouseout', (event)=>{
        let el = event.target;
        el.style = 'cursor: none; color: white'
    });
}