const menu = document.querySelector('#add_tarea');
        const burger = document.querySelector('#burger');
        let menuOn = false;
        function muestraMenu(){
            menuOn = !menuOn;
            if(menuOn){
                menu.style.right = "50px";
                burger.innerHTML ="X";
            }else {
                menu.style.right = "-350px";
                burger.innerHTML = "&#9776;"
            }
        }