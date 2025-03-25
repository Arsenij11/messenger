let button = document.querySelector('button');
const width = button.style.width;


button.addEventListener('mouseover', (event)=>{
    let el = event.target;
    el.style = `cursor: pointer; background-color: #808080; width : ${width}`
});
button.addEventListener('mouseout', (event)=> {
    let el = event.target;
    el.style = `cursor: none; background-color: #0e1621; width : ${width}`;
});